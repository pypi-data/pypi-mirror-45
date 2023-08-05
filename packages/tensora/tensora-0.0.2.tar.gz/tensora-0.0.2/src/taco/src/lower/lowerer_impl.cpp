#include "taco/lower/lowerer_impl.h"

#include "taco/index_notation/index_notation.h"
#include "taco/index_notation/index_notation_nodes.h"
#include "taco/index_notation/index_notation_visitor.h"
#include "taco/ir/ir.h"
#include "ir/ir_generators.h"
#include "taco/ir/ir_visitor.h"
#include "taco/ir/simplify.h"
#include "taco/lower/iterator.h"
#include "taco/lower/merge_lattice.h"
#include "mode_access.h"
#include "taco/util/collections.h"

using namespace std;
using namespace taco::ir;
using taco::util::combine;

namespace taco {

class LowererImpl::Visitor : public IndexNotationVisitorStrict {
public:
  Visitor(LowererImpl* impl) : impl(impl) {}
  Stmt lower(IndexStmt stmt) {
    this->stmt = Stmt();
    IndexStmtVisitorStrict::visit(stmt);
    return this->stmt;
  }
  Expr lower(IndexExpr expr) {
    this->expr = Expr();
    IndexExprVisitorStrict::visit(expr);
    return this->expr;
  }
private:
  LowererImpl* impl;
  Expr expr;
  Stmt stmt;
  using IndexNotationVisitorStrict::visit;
  void visit(const AssignmentNode* node) { stmt = impl->lowerAssignment(node); }
  void visit(const ForallNode* node)     { stmt = impl->lowerForall(node); }
  void visit(const WhereNode* node)      { stmt = impl->lowerWhere(node); }
  void visit(const MultiNode* node)      { stmt = impl->lowerMulti(node); }
  void visit(const SequenceNode* node)   { stmt = impl->lowerSequence(node); }
  void visit(const AccessNode* node)     { expr = impl->lowerAccess(node); }
  void visit(const LiteralNode* node)    { expr = impl->lowerLiteral(node); }
  void visit(const NegNode* node)        { expr = impl->lowerNeg(node); }
  void visit(const AddNode* node)        { expr = impl->lowerAdd(node); }
  void visit(const SubNode* node)        { expr = impl->lowerSub(node); }
  void visit(const MulNode* node)        { expr = impl->lowerMul(node); }
  void visit(const DivNode* node)        { expr = impl->lowerDiv(node); }
  void visit(const SqrtNode* node)       { expr = impl->lowerSqrt(node); }
  void visit(const ReductionNode* node)  {
    taco_ierror << "Reduction nodes not supported in concrete index notation";
  }
};

LowererImpl::LowererImpl() : visitor(new Visitor(this)) {
}


/// Convert index notation tensor variables to IR pointer variables.
static vector<Expr> createVars(const vector<TensorVar>& tensorVars,
                               map<TensorVar, Expr>* vars) {
  taco_iassert(vars != nullptr);
  vector<Expr> irVars;
  for (auto& var : tensorVars) {
    Expr irVar = Var::make(var.getName(),
                           var.getType().getDataType(),
                           true, true);
    irVars.push_back(irVar);
    vars->insert({var, irVar});
  }
  return irVars;
}

static void createCapacityVars(const map<TensorVar, Expr>& tensorVars,
                               map<Expr, Expr>* capacityVars) {
  for (auto& tensorVar : tensorVars) {
    Expr tensor = tensorVar.second;
    Expr capacityVar = Var::make(util::toString(tensor) + "_capacity", Int());
    capacityVars->insert({tensor, capacityVar});
  }
}

static void createReducedValueVars(const vector<Access>& inputAccesses,
                                   map<Access, Expr>* reducedValueVars) {
  for (const auto& access : inputAccesses) {
    const TensorVar inputTensor = access.getTensorVar();
    const std::string name = inputTensor.getName() + "_val";
    const Datatype type = inputTensor.getType().getDataType();
    reducedValueVars->insert({access, Var::make(name, type)});
  }
}

/// Replace scalar tensor pointers with stack scalar for lowering
static Stmt declareScalarArgumentVar(TensorVar var, bool zero,
                                     map<TensorVar, Expr>* tensorVars) {
  Datatype type = var.getType().getDataType();
  Expr varValueIR = Var::make(var.getName() + "_val", type, false, false);
  Expr init = (zero) ? ir::Literal::zero(type)
                     : Load::make(GetProperty::make(tensorVars->at(var),
                                                    TensorProperty::Values));
  tensorVars->find(var)->second = varValueIR;
  return VarDecl::make(varValueIR, init);
}

/// Returns true iff `stmt` modifies an array
static bool hasStores(Stmt stmt) {
  struct FindStores : IRVisitor {
    bool hasStore;

    using IRVisitor::visit;

    void visit(const Store* stmt) {
      hasStore = true;
    }

    bool hasStores(Stmt stmt) {
      hasStore = false;
      stmt.accept(this);
      return hasStore;
    }
  };
  return stmt.defined() && FindStores().hasStores(stmt);
}

Stmt LowererImpl::lower(IndexStmt stmt, string name, bool assemble,
                        bool compute) {
  this->assemble = assemble;
  this->compute = compute;

  // Create result and parameter variables
  vector<TensorVar> results = getResultTensorVars(stmt);
  vector<TensorVar> arguments = getInputTensorVars(stmt);
  vector<TensorVar> temporaries = getTemporaryTensorVars(stmt);

  // Convert tensor results, arguments and temporaries to IR variables
  map<TensorVar, Expr> resultVars;
  vector<Expr> resultsIR = createVars(results, &resultVars);
  tensorVars.insert(resultVars.begin(), resultVars.end());
  vector<Expr> argumentsIR = createVars(arguments, &tensorVars);
  vector<Expr> temporariesIR = createVars(temporaries, &tensorVars);

  // Create variables for keeping track of result values array capacity
  createCapacityVars(resultVars, &capacityVars);

  // Create iterators
  iterators = Iterators::make(stmt, tensorVars, &indexVars);

  const vector<Access> inputAccesses = getInputAccesses(stmt);
  const vector<Access> resultAccesses = getResultAccesses(stmt);

  // Create variables that represent the reduced values of duplicated tensor 
  // components
  createReducedValueVars(inputAccesses, &reducedValueVars);

  map<TensorVar, Expr> scalars;
  vector<Stmt> headerStmts;
  vector<Stmt> footerStmts;

  // Declare and initialize dimension variables
  vector<IndexVar> indexVars = getIndexVars(stmt);
  for (auto& ivar : indexVars) {
    Expr dimension;
    match(stmt,
      function<void(const AssignmentNode*,Matcher*)>([&](
          const AssignmentNode* n, Matcher* m) {
        m->match(n->rhs);
        if (!dimension.defined()) {
          auto ivars = n->lhs.getIndexVars();
          int loc = (int)distance(ivars.begin(),
                                  find(ivars.begin(),ivars.end(), ivar));
          dimension = GetProperty::make(tensorVars.at(n->lhs.getTensorVar()),
                                        TensorProperty::Dimension, loc);
        }
      }),
      function<void(const AccessNode*)>([&](const AccessNode* n) {
        auto ivars = n->indexVars;
        int loc = (int)distance(ivars.begin(),
                                find(ivars.begin(),ivars.end(), ivar));
        dimension = GetProperty::make(tensorVars.at(n->tensorVar),
                                      TensorProperty::Dimension, loc);
      })
    );
    dimensions.insert({ivar, dimension});
  }

  // Declare and initialize scalar results and arguments
  if (generateComputeCode()) {
    for (auto& result : results) {
      if (isScalar(result.getType())) {
        taco_iassert(!util::contains(scalars, result));
        taco_iassert(util::contains(tensorVars, result));
        scalars.insert({result, tensorVars.at(result)});
        headerStmts.push_back(declareScalarArgumentVar(result, true,
                                                       &tensorVars));
      }
    }
    for (auto& argument : arguments) {
      if (isScalar(argument.getType())) {
        taco_iassert(!util::contains(scalars, argument));
        taco_iassert(util::contains(tensorVars, argument));
        scalars.insert({argument, tensorVars.at(argument)});
        headerStmts.push_back(declareScalarArgumentVar(argument, false,
                                                       &tensorVars));
      }
    }
  }

  // Allocate memory for scalar results
  if (generateAssembleCode()) {
    for (auto& result : results) {
      if (result.getOrder() == 0) {
        Expr resultIR = resultVars.at(result);
        Expr vals = GetProperty::make(resultIR, TensorProperty::Values);
        headerStmts.push_back(Allocate::make(vals, 1));
      }
    }
  }

  // Allocate and initialize append and insert mode indices
  Stmt initializeResults = initResultArrays(resultAccesses, inputAccesses);

  // Declare, allocate, and initialize temporaries
  Stmt declareTemporaries = declTemporaries(temporaries, scalars);

  // Lower the index statement to compute and/or assemble
  Stmt body = lower(stmt);

  // Post-process result modes and allocate memory for values if necessary
  Stmt finalizeResults = finalizeResultArrays(resultAccesses);

  // Store scalar stack variables back to results
  if (generateComputeCode()) {
    for (auto& result : results) {
      if (isScalar(result.getType())) {
        taco_iassert(util::contains(scalars, result));
        taco_iassert(util::contains(tensorVars, result));
        Expr resultIR = scalars.at(result);
        Expr varValueIR = tensorVars.at(result);
        Expr valuesArrIR = GetProperty::make(resultIR, TensorProperty::Values);
        footerStmts.push_back(Store::make(valuesArrIR, 0, varValueIR));
      }
    }
  }

  // Create function
  Stmt header = headerStmts.empty() ? Stmt() : Block::make(headerStmts);
  Stmt footer = footerStmts.empty() ? Stmt() : Block::make(footerStmts);
  return Function::make(name, resultsIR, argumentsIR,
                        Block::blanks(header,
                                      declareTemporaries,
                                      initializeResults,
                                      body,
                                      finalizeResults,
                                      footer));
}


Stmt LowererImpl::lowerAssignment(Assignment assignment) {
  TensorVar result = assignment.getLhs().getTensorVar();

  if (generateComputeCode()) {
    Expr var = getTensorVar(result);
    Expr rhs = lower(assignment.getRhs());

    // Assignment to scalar variables.
    if (isScalar(result.getType())) {
      if (!assignment.getOperator().defined()) {
        return Assign::make(var, rhs);
      }
      else {
        taco_iassert(isa<taco::Add>(assignment.getOperator()));
        return compoundAssign(var, rhs);
      }
    }
    // Assignments to tensor variables (non-scalar).
    else {
      Expr values = GetProperty::make(var, TensorProperty::Values);
      Expr capacity = getCapacityVar(var);
      Expr loc = generateValueLocExpr(assignment.getLhs());

      // When we're assembling while computing we need to allocate more
      // value memory as we write to the values array.
      Iterator lastIterator = getIterators(assignment.getLhs()).back();
      Stmt resizeValueArray;
      if (generateAssembleCode() && lastIterator.hasAppend()) {
        resizeValueArray = doubleSizeIfFull(values, capacity, loc);
      }

      Stmt computeStmt = Store::make(values, loc, rhs);

      return resizeValueArray.defined()
             ? Block::make(resizeValueArray, computeStmt)
             : computeStmt;
    }
  }
  // We're only assembling so defer allocating value memory to the end when
  // we'll know exactly how much we need.
  else if (generateAssembleCode()) {
    // TODO
    return Stmt();
  }
  // We're neither assembling or computing so we emit nothing.
  else {
    return Stmt();
  }
  taco_unreachable;
  return Stmt();
}


static pair<vector<Iterator>, vector<Iterator>>
splitAppenderAndInserters(const vector<Iterator>& results) {
  vector<Iterator> appenders;
  vector<Iterator> inserters;

  // TODO: Choose insert when the current forall is nested inside a reduction
  for (auto& result : results) {
    taco_iassert(result.hasAppend() || result.hasInsert())
        << "Results must support append or insert";

    if (result.hasAppend()) {
      appenders.push_back(result);
    }
    else {
      taco_iassert(result.hasInsert());
      inserters.push_back(result);
    }
  }

  return {appenders, inserters};
}


Stmt LowererImpl::lowerForall(Forall forall)
{
  MergeLattice lattice = MergeLattice::make(forall, iterators);

  // Pre-allocate/initialize memory of value arrays that are full below this
  // loops index variable
  Stmt preInitValues = initResultArrays(forall.getIndexVar(),
                                        getResultAccesses(forall),
                                        getInputAccesses(forall));

  Stmt loops;
  // Emit a loop that iterates over over a single iterator (optimization)
  if (lattice.points().size() == 1 && lattice.iterators().size() == 1 &&
      lattice.iterators()[0].isUnique()) {
    MergePoint point = lattice.points()[0];
    Iterator iterator = lattice.iterators()[0];

    vector<Iterator> locaters = point.locators();
    vector<Iterator> appenders;
    vector<Iterator> inserters;
    tie(appenders, inserters) = splitAppenderAndInserters(point.results());

    // Emit dimension coordinate iteration loop
    if (iterator.isDimensionIterator()) {
      loops = lowerForallDimension(forall, point.locators(),
                                  inserters, appenders);
    }
    // Emit position iteration loop
    else if (iterator.hasPosIter()) {
      loops = lowerForallPosition(forall, iterator, locaters,
                                 inserters, appenders);
    }
    // Emit coordinate iteration loop
    else {
      taco_iassert(iterator.hasCoordIter());
      taco_not_supported_yet;
      loops = Stmt();
    }
  }
  // Emit general loops to merge multiple iterators
  else {
    loops = lowerMergeLattice(lattice, getCoordinateVar(forall.getIndexVar()),
                              forall.getStmt());
  }
  taco_iassert(loops.defined());

  if (!generateComputeCode() && !hasStores(loops)) {
    // If assembly loop does not modify output arrays, then it can be safely 
    // omitted.
    loops = Stmt();
  }

  return Block::blanks(preInitValues,
                       loops);
}


Stmt LowererImpl::lowerForallDimension(Forall forall,
                                       vector<Iterator> locators,
                                       vector<Iterator> inserters,
                                       vector<Iterator> appenders)
{
  Expr coordinate = getCoordinateVar(forall.getIndexVar());

  Stmt body = lowerForallBody(coordinate, forall.getStmt(),
                              locators, inserters, appenders);

  Stmt posAppend = generateAppendPositions(appenders);

  // Emit loop with preamble and postamble
  Expr dimension = getDimension(forall.getIndexVar());
  return Block::blanks(For::make(coordinate, 0, dimension, 1, body,
                                 LoopKind::Serial, false),
                       posAppend);
}


Stmt LowererImpl::lowerForallCoordinate(Forall forall, Iterator iterator,
                                        vector<Iterator> locaters,
                                        vector<Iterator> inserters,
                                        vector<Iterator> appenders) {
  taco_not_supported_yet;
  return Stmt();
}

Stmt LowererImpl::lowerForallPosition(Forall forall, Iterator iterator,
                                      vector<Iterator> locators,
                                      vector<Iterator> inserters,
                                      vector<Iterator> appenders)
{
  Expr coordinate = getCoordinateVar(forall.getIndexVar());
  Expr coordinateArray= iterator.posAccess(iterator.getPosVar(), 
                                           coordinates(iterator)).getResults()[0];
  Stmt declareCoordinate = VarDecl::make(coordinate, coordinateArray);

  Stmt body = lowerForallBody(coordinate, forall.getStmt(),
                              locators, inserters, appenders);

  // Code to append positions
  Stmt posAppend = generateAppendPositions(appenders);

  // Code to compute iteration bounds
  Stmt boundsCompute;
  Expr startBound, endBound;
  Expr parentPos = iterator.getParent().getPosVar();
  if (iterator.getParent().isRoot() || iterator.getParent().isUnique()) {
    // E.g. a compressed mode without duplicates
    ModeFunction bounds = iterator.posBounds(parentPos);
    boundsCompute = bounds.compute();
    startBound = bounds[0];
    endBound = bounds[1];
  } else {
    taco_iassert(iterator.isOrdered() && iterator.getParent().isOrdered());
    taco_iassert(iterator.isCompact() && iterator.getParent().isCompact());

    // E.g. a compressed mode with duplicates. Apply iterator chaining
    Expr parentSegend = iterator.getParent().getSegendVar();
    ModeFunction startBounds = iterator.posBounds(parentPos);
    ModeFunction endBounds = iterator.posBounds(ir::Sub::make(parentSegend, 1));
    boundsCompute = Block::make(startBounds.compute(), endBounds.compute());
    startBound = startBounds[0];
    endBound = endBounds[1];
  }

  // Loop with preamble and postamble
  return Block::blanks(boundsCompute,
                       For::make(iterator.getPosVar(), startBound, endBound, 1,
                                 Block::make(declareCoordinate, body),
                                 LoopKind::Serial, false),
                       posAppend);

}

Stmt LowererImpl::lowerMergeLattice(MergeLattice lattice, Expr coordinate,
                                    IndexStmt statement)
{
  vector<Iterator> appenders = filter(lattice.results(),
                                      [](Iterator it){return it.hasAppend();});

  Stmt iteratorVarInits = codeToInitializeIteratorVars(lattice.iterators());

  vector<Stmt> mergeLoopsVec;
  for (MergePoint point : lattice.points()) {
    // Each iteration of this loop generates a while loop for one of the merge
    // points in the merge lattice.
    IndexStmt zeroedStmt = zero(statement, getExhaustedAccesses(point,lattice));
    MergeLattice sublattice = lattice.subLattice(point);
    Stmt mergeLoop = lowerMergePoint(sublattice, coordinate, zeroedStmt);
    mergeLoopsVec.push_back(mergeLoop);
  }
  Stmt mergeLoops = Block::make(mergeLoopsVec);

  // Append position to the pos array
  Stmt appendPositions = generateAppendPositions(appenders);

  return Block::blanks(iteratorVarInits,
                       mergeLoops,
                       appendPositions);
}

Stmt LowererImpl::lowerMergePoint(MergeLattice pointLattice,
                                  ir::Expr coordinate, IndexStmt statement)
{
  MergePoint point = pointLattice.points().front();

  vector<Iterator> iterators = point.iterators();
  vector<Iterator> mergers = point.mergers();
  vector<Iterator> rangers = point.rangers();
  vector<Iterator> locators = point.locators();

  taco_iassert(iterators.size() > 0);
  taco_iassert(mergers.size() > 0);
  taco_iassert(rangers.size() > 0);

  // Load coordinates from position iterators
  Stmt loadPosIterCoordinates;
  if (iterators.size() > 1) {
    vector<Stmt> loadPosIterCoordinateStmts;
    auto posIters = filter(iterators, [](Iterator it){return it.hasPosIter();});
    for (auto& posIter : posIters) {
      taco_tassert(posIter.hasPosIter());
      ModeFunction posAccess = posIter.posAccess(posIter.getPosVar(), 
                                                 coordinates(posIter));
      loadPosIterCoordinateStmts.push_back(posAccess.compute());
      loadPosIterCoordinateStmts.push_back(VarDecl::make(posIter.getCoordVar(),
                                                          posAccess[0]));
    }
    loadPosIterCoordinates = Block::make(loadPosIterCoordinateStmts);
  }

  // Merge iterator coordinate variables
  Stmt resolveCoordinate;
  if (mergers.size() == 1) {
    Iterator merger = mergers[0];
    if (merger.hasPosIter()) {
      // Just one position iterator so it is the resolved coordinate
      ModeFunction posAccess = merger.posAccess(merger.getPosVar(), 
                                                coordinates(merger));
      resolveCoordinate = Block::make(posAccess.compute(),
                                          VarDecl::make(coordinate,
                                                        posAccess[0]));
    }
    else if (merger.hasCoordIter()) {
      taco_not_supported_yet;
    }
    else if (merger.isDimensionIterator()) {
      // Just one dimension iterator so resolved coordinate already exist and we
      // do nothing
    }
    else {
      taco_ierror << "Unexpected type of single iterator " << merger;
    }
  }
  else {
    // Multiple position iterators so the smallest is the resolved coordinate
    resolveCoordinate = VarDecl::make(coordinate,
                                      Min::make(coordinates(mergers)));
  }

  // Locate positions
  Stmt loadLocatorPosVars = declLocatePosVars(locators);

  // Deduplication loops
  auto dupIters = filter(iterators, [](Iterator it){return !it.isUnique() && 
                                                           it.hasPosIter();});
  Stmt deduplicationLoops = reduceDuplicateCoordinates(coordinate, dupIters, 
                                                       mergers.size() == 1);

  // One case for each child lattice point lp
  Stmt caseStmts = lowerMergeCases(coordinate, statement, pointLattice);

  // Increment iterator position variables
  Stmt incIteratorVarStmts = codeToIncIteratorVars(coordinate, iterators);

  /// While loop over rangers
  return While::make(checkThatNoneAreExhausted(rangers),
                     Block::make(loadPosIterCoordinates,
                                 resolveCoordinate,
                                 loadLocatorPosVars,
                                 deduplicationLoops,
                                 caseStmts,
                                 incIteratorVarStmts));
}

Stmt LowererImpl::lowerMergeCases(ir::Expr coordinate, IndexStmt stmt,
                                  MergeLattice lattice)
{
  vector<Stmt> result;

  vector<Iterator> appenders;
  vector<Iterator> inserters;
  tie(appenders, inserters) = splitAppenderAndInserters(lattice.results());

  // Just one iterator so no conditionals
  if (lattice.iterators().size() == 1) {
    Stmt body = lowerForallBody(coordinate, stmt, {}, inserters, appenders);
    result.push_back(body);
  }
  else {
    vector<pair<Expr,Stmt>> cases;
    for (MergePoint point : lattice.points()) {

      // Construct case expression
      vector<Expr> coordComparisons;
      for (Iterator iterator : point.rangers()) {
        coordComparisons.push_back(Eq::make(iterator.getCoordVar(),coordinate));
      }

      // Construct case body
      IndexStmt zeroedStmt = zero(stmt, getExhaustedAccesses(point, lattice));
      Stmt body = lowerForallBody(coordinate, zeroedStmt, {},
                                  inserters, appenders);

      cases.push_back({conjunction(coordComparisons), body});
    }
    result.push_back(Case::make(cases, lattice.exact()));
  }

  return Block::make(result);
}


Stmt LowererImpl::lowerForallBody(Expr coordinate, IndexStmt stmt,
                                  vector<Iterator> locators,
                                  vector<Iterator> inserters,
                                  vector<Iterator> appenders) {
  // Inserter positions
  Stmt declInserterPosVars = declLocatePosVars(inserters);

  // Locate positions
  Stmt declLocatorPosVars = declLocatePosVars(locators);

  // Code of loop body statement
  Stmt body = lower(stmt);

  // Code to append coordinates
  Stmt appendCoords = appendCoordinate(appenders, coordinate);

  // TODO: Emit code to insert coordinates

  return Block::make(declInserterPosVars,
                     declLocatorPosVars,
                     body,
                     appendCoords);
}


Stmt LowererImpl::lowerWhere(Where where) {
  // TODO: Either initialise or re-initialize temporary memory
  Stmt producer = lower(where.getProducer());
  Stmt consumer = lower(where.getConsumer());
  return Block::make(producer, consumer);
}


Stmt LowererImpl::lowerSequence(Sequence sequence) {
  Stmt definition = lower(sequence.getDefinition());
  Stmt mutation = lower(sequence.getMutation());
  return Block::make(definition, mutation);
}


Stmt LowererImpl::lowerMulti(Multi multi) {
  Stmt stmt1 = lower(multi.getStmt1());
  Stmt stmt2 = lower(multi.getStmt2());
  return Block::make(stmt1, stmt2);
}


Expr LowererImpl::lowerAccess(Access access) {
  TensorVar var = access.getTensorVar();
  Expr varIR = getTensorVar(var);

  if (isScalar(var.getType())) {
    return varIR;
  }
  
  return getIterators(access).back().isUnique()
         ? Load::make(GetProperty::make(varIR, TensorProperty::Values),
                      generateValueLocExpr(access))
         : getReducedValueVar(access);
}


Expr LowererImpl::lowerLiteral(Literal) {
  taco_not_supported_yet;
  return Expr();
}


Expr LowererImpl::lowerNeg(Neg neg) {
  return ir::Neg::make(lower(neg.getA()));
}


Expr LowererImpl::lowerAdd(Add add) {
  return ir::Add::make(lower(add.getA()), lower(add.getB()));
}


Expr LowererImpl::lowerSub(Sub sub) {
  return ir::Sub::make(lower(sub.getA()), lower(sub.getB()));
}


Expr LowererImpl::lowerMul(Mul mul) {
  return ir::Mul::make(lower(mul.getA()), lower(mul.getB()));
}


Expr LowererImpl::lowerDiv(Div div) {
  return ir::Div::make(lower(div.getA()), lower(div.getB()));
}


Expr LowererImpl::lowerSqrt(Sqrt sqrt) {
  return ir::Sqrt::make(lower(sqrt.getA()));
}


Stmt LowererImpl::lower(IndexStmt stmt) {
  return visitor->lower(stmt);
}


Expr LowererImpl::lower(IndexExpr expr) {
  return visitor->lower(expr);
}


bool LowererImpl::generateAssembleCode() const {
  return this->assemble;
}


bool LowererImpl::generateComputeCode() const {
  return this->compute;
}


Expr LowererImpl::getTensorVar(TensorVar tensorVar) const {
  taco_iassert(util::contains(this->tensorVars, tensorVar)) << tensorVar;
  return this->tensorVars.at(tensorVar);
}


Expr LowererImpl::getCapacityVar(Expr tensor) const {
  taco_iassert(util::contains(this->capacityVars, tensor)) << tensor;
  return this->capacityVars.at(tensor);
}


Expr LowererImpl::getDimension(IndexVar indexVar) const {
  taco_iassert(util::contains(this->dimensions, indexVar)) << indexVar;
  return this->dimensions.at(indexVar);
}


std::vector<Iterator> LowererImpl::getIterators(Access access) const {
  vector<Iterator> result;
  TensorVar tensor = access.getTensorVar();
  for (int i = 0; i < tensor.getOrder(); i++) {
    int mode = tensor.getFormat().getModeOrdering()[i];
    result.push_back(iterators.levelIterator(ModeAccess(access, mode+1)));
  }
  return result;
}


set<Access> LowererImpl::getExhaustedAccesses(MergePoint point,
                                              MergeLattice lattice) const
{
  set<Access> exhaustedAccesses;
  for (auto& iterator : lattice.exhausted(point)) {
    exhaustedAccesses.insert(iterators.modeAccess(iterator).getAccess());
  }
  return exhaustedAccesses;
}


Expr LowererImpl::getReducedValueVar(Access access) const {
  return this->reducedValueVars.at(access);
}


Expr LowererImpl::getCoordinateVar(IndexVar indexVar) const {
  return this->iterators.modeIterator(indexVar).getCoordVar();
}


Expr LowererImpl::getCoordinateVar(Iterator iterator) const {
  if (iterator.isDimensionIterator()) {
    return iterator.getCoordVar();
  }
  taco_iassert(util::contains(this->indexVars, iterator))
      << "Could not find a coordinate for " << iterator << " from "
      << util::join(this->indexVars);
  auto& indexVar = this->indexVars.at(iterator);
  return this->getCoordinateVar(indexVar);
}


vector<Expr> LowererImpl::coordinates(Iterator iterator) const {
  taco_iassert(iterator.defined());

  vector<Expr> coords;
  do {
    coords.push_back(getCoordinateVar(iterator));
    iterator = iterator.getParent();
  } while (!iterator.isRoot());
  auto reverse = util::reverse(coords);
  return vector<Expr>(reverse.begin(), reverse.end());
}


vector<Expr> LowererImpl::coordinates(vector<Iterator> iterators)
{
  taco_iassert(all(iterators, [](Iterator iter){ return iter.defined(); }));
  vector<Expr> result;
  for (auto& iterator : iterators) {
    result.push_back(iterator.getCoordVar());
  }
  return result;
}


/// Returns true iff a result mode is assembled by inserting a sparse set of 
/// result coordinates (e.g., compressed to dense).
static 
bool hasSparseInserts(const std::vector<Iterator>& resultIterators,
                      const std::multimap<IndexVar, Iterator>& inputIterators) {
  for (const auto& resultIterator : resultIterators) {
    if (resultIterator.hasInsert()) {
      const auto indexVar = resultIterator.getIndexVar();
      const auto accessedInputs = inputIterators.equal_range(indexVar);
      for (auto inputIterator = accessedInputs.first; 
           inputIterator != accessedInputs.second; ++inputIterator) {
        if (!inputIterator->second.isFull()) {
          return true;
        }
      }
    }
  }
  return false;
}


Stmt LowererImpl::initResultArrays(vector<Access> writes, 
                                   vector<Access> reads) {
  multimap<IndexVar, Iterator> readIterators;
  for (auto& read : reads) {
    for (auto& readIterator : getIterators(read)) {
      readIterators.insert({readIterator.getIndexVar(), readIterator});
    }
  }

  std::vector<Stmt> result;
  for (auto& write : writes) {
    if (write.getTensorVar().getOrder() == 0) continue;

    std::vector<Stmt> initArrays;

    const auto iterators = getIterators(write);
    taco_iassert(!iterators.empty());

    Expr tensor = getTensorVar(write.getTensorVar());
    Expr valuesArr = GetProperty::make(tensor, TensorProperty::Values);

    Expr parentSize = 1;
    if (generateAssembleCode()) {
      for (const auto& iterator : iterators) {
        Expr size;
        Stmt init;
        // Initialize data structures for storing levels
        if (iterator.hasAppend()) {
          size = 0;
          init = iterator.getAppendInitLevel(parentSize, size);
        } else if (iterator.hasInsert()) {
          size = simplify(ir::Mul::make(parentSize, iterator.getWidth()));
          init = iterator.getInsertInitLevel(parentSize, size);
        } else {
          taco_ierror << "Write iterator supports neither append nor insert";
        }
        initArrays.push_back(init);

        // Declare position variable of append modes that are not above a 
        // branchless mode (if mode below is branchless, then can share same 
        // position variable)
        if (iterator.hasAppend() && (iterator.isLeaf() || 
            !iterator.getChild().isBranchless())) {
          initArrays.push_back(VarDecl::make(iterator.getPosVar(), 0));
        }

        parentSize = size;
      }

      // Pre-allocate memory for the value array if computing while assembling
      if (generateComputeCode()) {
        taco_iassert(!iterators.empty());
        
        Expr capacityVar = getCapacityVar(tensor);
        Expr allocSize = isValue(parentSize, 0) 
                         ? DEFAULT_ALLOC_SIZE : parentSize;
        initArrays.push_back(VarDecl::make(capacityVar, allocSize));
        initArrays.push_back(Allocate::make(valuesArr, capacityVar));
      }

      taco_iassert(!initArrays.empty());
      result.push_back(Block::make(initArrays));
    }
    else if (generateComputeCode()) {
      Iterator lastAppendIterator;
      // Compute size of values array
      for (auto& iterator : iterators) {
        if (iterator.hasAppend()) {
          lastAppendIterator = iterator;
          parentSize = iterator.getSize(parentSize);
        } else if (iterator.hasInsert()) {
          parentSize = ir::Mul::make(parentSize, iterator.getWidth());
        } else {
          taco_ierror << "Write iterator supports neither append nor insert";
        }
        parentSize = simplify(parentSize);
      }

      // Declare position variable for the last append level
      if (lastAppendIterator.defined()) {
        result.push_back(VarDecl::make(lastAppendIterator.getPosVar(), 0));
      }
    }

    // TODO: Check for scatter code
    if (generateComputeCode() && iterators.back().hasInsert() && 
        !isValue(parentSize, 0) && hasSparseInserts(iterators, readIterators)) {
      // Zero-initialize values array if size statically known and might not 
      // assign to every element in values array during compute
      Expr size = generateAssembleCode() ? getCapacityVar(tensor) : parentSize;
      result.push_back(zeroInitValues(tensor, 0, size));
    }
  }
  return result.empty() ? Stmt() : Block::blanks(result);
}


ir::Stmt LowererImpl::finalizeResultArrays(std::vector<Access> writes) {
  if (!generateAssembleCode()) {
    return Stmt();
  }

  std::vector<Stmt> result;
  for (auto& write : writes) {
    if (write.getTensorVar().getOrder() == 0) continue;

    const auto iterators = getIterators(write);
    taco_iassert(!iterators.empty());
      
    Expr parentSize = 1;
    for (const auto& iterator : iterators) {
      Expr size;
      Stmt finalize;
      // Post-process data structures for storing levels
      if (iterator.hasAppend()) {
        size = iterator.getPosVar();
        finalize = iterator.getAppendFinalizeLevel(parentSize, size);
      } else if (iterator.hasInsert()) {
        size = simplify(ir::Mul::make(parentSize, iterator.getWidth()));
        finalize = iterator.getInsertFinalizeLevel(parentSize, size);
      } else {
        taco_ierror << "Write iterator supports neither append nor insert";
      }
      result.push_back(finalize);
      parentSize = size;
    }

    if (!generateComputeCode()) {
      // Allocate memory for values array after assembly if not also computing
      Expr tensor = getTensorVar(write.getTensorVar());
      Expr valuesArr = GetProperty::make(tensor, TensorProperty::Values);
      result.push_back(Allocate::make(valuesArr, parentSize));
    }
  }
  return result.empty() ? Stmt() : Block::blanks(result);
}


Stmt LowererImpl::declTemporaries(vector<TensorVar> temporaries,
                                  map<TensorVar, Expr> scalars) {
  vector<Stmt> result;
  if (generateComputeCode()) {
    for (auto& temporary : temporaries) {
      if (isScalar(temporary.getType())) {
        taco_iassert(!util::contains(scalars, temporary)) << temporary;
        taco_iassert(util::contains(tensorVars, temporary));
        scalars.insert({temporary, tensorVars.at(temporary)});
        result.push_back(declareScalarArgumentVar(temporary,true,&tensorVars));
      }
    }
  }
  return result.empty() ? Stmt() : Block::make(result);
}


static
vector<Iterator> getIteratorsFrom(IndexVar var, 
                                  const vector<Iterator>& iterators) {
  vector<Iterator> result;
  bool found = false;
  for (Iterator iterator : iterators) {
    if (var == iterator.getIndexVar()) found = true;
    if (found) {
      result.push_back(iterator);
    }
  }
  return result;
}


Stmt LowererImpl::initResultArrays(IndexVar var, vector<Access> writes, 
                                   vector<Access> reads) {
  if (!generateAssembleCode()) {
    return Stmt();
  }

  multimap<IndexVar, Iterator> readIterators;
  for (auto& read : reads) {
    for (auto& readIterator : getIteratorsFrom(var, getIterators(read))) {
      readIterators.insert({readIterator.getIndexVar(), readIterator});
    }
  }

  vector<Stmt> result;
  for (auto& write : writes) {
    Expr tensor = getTensorVar(write.getTensorVar());
    Expr values = GetProperty::make(tensor, TensorProperty::Values);

    vector<Iterator> iterators = getIteratorsFrom(var, getIterators(write));

    if (iterators.empty()) {
      continue;
    }

    Iterator resultIterator = iterators.front();

    // Initialize begin var
    if (resultIterator.hasAppend() && !resultIterator.isBranchless()) {
      Expr begin = resultIterator.getBeginVar();
      result.push_back(VarDecl::make(begin, resultIterator.getPosVar()));
    }

    const bool isTopLevel = (iterators.size() == write.getIndexVars().size());
    if (resultIterator.getParent().hasAppend() || isTopLevel) {
      Expr resultParentPos = resultIterator.getParent().getPosVar();
      Expr resultParentPosNext = simplify(ir::Add::make(resultParentPos, 1));
      Expr initBegin = resultParentPos;
      Expr initEnd = resultParentPosNext;
      Expr stride = 1;

      Iterator initIterator;
      for (Iterator iterator : iterators) {
        if (!iterator.hasInsert()) {
          initIterator = iterator;
          break;
        }

        stride = simplify(ir::Mul::make(stride, iterator.getWidth()));
        initBegin = simplify(ir::Mul::make(resultParentPos, stride));
        initEnd = simplify(ir::Mul::make(resultParentPosNext, stride));

        // Initialize data structures for storing insert mode
        result.push_back(iterator.getInsertInitCoords(initBegin, initEnd));
      }

      if (initIterator.defined()) {
        // Initialize data structures for storing edges of next append mode
        taco_iassert(initIterator.hasAppend());
        result.push_back(initIterator.getAppendInitEdges(initBegin, initEnd));
      } else if (generateComputeCode() && !isTopLevel) {
        if (isa<ir::Mul>(stride)) {
          Expr strideVar = Var::make(util::toString(tensor) + "_stride", Int());
          result.push_back(VarDecl::make(strideVar, stride));
          stride = strideVar;
        } 

        // Resize values array if not large enough
        Expr capacityVar = getCapacityVar(tensor);
        Expr size = simplify(ir::Mul::make(resultParentPosNext, stride));
        result.push_back(atLeastDoubleSizeIfFull(values, capacityVar, size));

        if (hasSparseInserts(iterators, readIterators)) {
          // Zero-initialize values array if might not assign to every element 
          // in values array during compute
          result.push_back(zeroInitValues(tensor, resultParentPos, stride));
        }
      }
    }
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Stmt LowererImpl::zeroInitValues(Expr tensor, Expr begin, Expr size) {
  Expr lower = simplify(ir::Mul::make(begin, size));
  Expr upper = simplify(ir::Mul::make(ir::Add::make(begin, 1), size));
  Expr p = Var::make("p" + util::toString(tensor), Int());
  Expr values = GetProperty::make(tensor, TensorProperty::Values);
  Stmt zeroInit = Store::make(values, p, ir::Literal::zero(tensor.type()));
  LoopKind parallel = (isa<ir::Literal>(size) && 
                       to<ir::Literal>(size)->getIntValue() < (1 << 10))
                      ? LoopKind::Serial : LoopKind::Static;
  return For::make(p, lower, upper, 1, zeroInit, parallel, false);
}


Stmt LowererImpl::declLocatePosVars(vector<Iterator> locaters) {
  vector<Stmt> result;
  for (Iterator& locateIterator : locaters) {
    ModeFunction locate = locateIterator.locate(coordinates(locateIterator));
    taco_iassert(isValue(locate.getResults()[1], true));
    Stmt declarePosVar = VarDecl::make(locateIterator.getPosVar(),
                                       locate.getResults()[0]);
    result.push_back(declarePosVar);
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Stmt LowererImpl::reduceDuplicateCoordinates(Expr coordinate, 
                                             vector<Iterator> iterators,
                                             bool alwaysReduce) {
  vector<Stmt> result;
  for (Iterator& iterator : iterators) {
    taco_iassert(!iterator.isUnique() && iterator.hasPosIter());

    Access access = this->iterators.modeAccess(iterator).getAccess();
    Expr iterVar = iterator.getIteratorVar();
    Expr segendVar = iterator.getSegendVar();
    Expr reducedVal = iterator.isLeaf() ? getReducedValueVar(access) : Expr();
    Expr tensorVar = getTensorVar(access.getTensorVar());
    Expr tensorVals = GetProperty::make(tensorVar, TensorProperty::Values);

    // Initialize variable storing reduced component value.
    if (reducedVal.defined()) {
      Expr reducedValInit = alwaysReduce 
                          ? Load::make(tensorVals, iterVar)
                          : ir::Literal::zero(reducedVal.type());
      result.push_back(VarDecl::make(reducedVal, reducedValInit));
    }

    if (iterator.isLeaf() && alwaysReduce) {
      // If iterator is over bottommost coordinate hierarchy level and will 
      // always advance (i.e., not merging with another iterator), then we don't 
      // need a separate segend variable.
      segendVar = iterVar;
      result.push_back(compoundAssign(segendVar, 1));
    } else {
      Expr segendInit = alwaysReduce ? ir::Add::make(iterVar, 1) : iterVar;
      result.push_back(VarDecl::make(segendVar, segendInit));
    }
    
    vector<Stmt> dedupStmts;
    if (reducedVal.defined()) {
      Expr partialVal = Load::make(tensorVals, segendVar);
      dedupStmts.push_back(compoundAssign(reducedVal, partialVal));
    }
    dedupStmts.push_back(compoundAssign(segendVar, 1));
    Stmt dedupBody = Block::make(dedupStmts);

    ModeFunction posAccess = iterator.posAccess(segendVar, 
                                                coordinates(iterator));
    // TODO: Support access functions that perform additional computations 
    //       and/or might access invalid positions.
    taco_iassert(!posAccess.compute().defined());
    taco_iassert(to<ir::Literal>(posAccess.getResults()[1])->getBoolValue());
    Expr nextCoord = posAccess.getResults()[0];
    Expr withinBounds = Lt::make(segendVar, iterator.getEndVar());
    Expr isDuplicate = Eq::make(posAccess.getResults()[0], coordinate);
    result.push_back(While::make(And::make(withinBounds, isDuplicate),
                                 Block::make(dedupStmts)));
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Stmt LowererImpl::codeToInitializeIteratorVars(vector<Iterator> iterators) {
  vector<Stmt> result;
  for (Iterator iterator : iterators) {
    taco_iassert(iterator.hasPosIter() || iterator.hasCoordIter() ||
                 iterator.isDimensionIterator());

    Expr iterVar = iterator.getIteratorVar();
    Expr endVar = iterator.getEndVar();
    if (iterator.hasPosIter()) {
      Expr parentPos = iterator.getParent().getPosVar();
      if (iterator.getParent().isRoot() || iterator.getParent().isUnique()) {
        // E.g. a compressed mode without duplicates
        ModeFunction bounds = iterator.posBounds(parentPos);
        result.push_back(bounds.compute());
        result.push_back(VarDecl::make(iterVar, bounds[0]));
        result.push_back(VarDecl::make(endVar, bounds[1]));
      } else {
        taco_iassert(iterator.isOrdered() && iterator.getParent().isOrdered());
        taco_iassert(iterator.isCompact() && iterator.getParent().isCompact());

        // E.g. a compressed mode with duplicates. Apply iterator chaining
        Expr parentSegend = iterator.getParent().getSegendVar();
        ModeFunction startBounds = iterator.posBounds(parentPos);
        ModeFunction endBounds = iterator.posBounds(ir::Sub::make(parentSegend, 1));
        result.push_back(startBounds.compute());
        result.push_back(VarDecl::make(iterVar, startBounds[0]));
        result.push_back(endBounds.compute());
        result.push_back(VarDecl::make(endVar, endBounds[1]));
      }
    }
    else if (iterator.hasCoordIter()) {
      // E.g. a hasmap mode
      vector<Expr> coords = coordinates(iterator);
      coords.erase(coords.begin());
      ModeFunction bounds = iterator.coordBounds(coords);
      result.push_back(bounds.compute());
      result.push_back(VarDecl::make(iterVar, bounds[0]));
      result.push_back(VarDecl::make(endVar, bounds[1]));
    }
    else if (iterator.isDimensionIterator()) {
      // A dimension
      Expr coord = coordinates(vector<Iterator>({iterator}))[0];
      result.push_back(VarDecl::make(coord, 0));
    }
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Stmt LowererImpl::codeToIncIteratorVars(Expr coordinate, vector<Iterator> iterators) {
  if (iterators.size() == 1) {
    Expr ivar = iterators[0].getIteratorVar();

    if (iterators[0].isUnique()) {
      return compoundAssign(ivar, 1); 
    }

    // If iterator is over bottommost coordinate hierarchy level with 
    // duplicates and iterator will always advance (i.e., not merging with 
    // another iterator), then deduplication loop will take care of 
    // incrementing iterator variable.
    return iterators[0].isLeaf() 
           ? Stmt()
           : Assign::make(ivar, iterators[0].getSegendVar());
  }

  vector<Stmt> result;

  // We emit the level iterators before the mode iterator because the coordinate
  // of the mode iterator is used to conditionally advance the level iterators.

  auto levelIterators =
      filter(iterators, [](Iterator it){return !it.isDimensionIterator();});
  for (auto& iterator : levelIterators) {
    Expr ivar = iterator.getIteratorVar();
    if (iterator.isUnique()) {
      Expr increment = iterator.isFull()
                     ? 1
                     : Cast::make(Eq::make(iterator.getCoordVar(), coordinate),
                                  ivar.type());
      result.push_back(compoundAssign(ivar, increment));
    } else {
      result.push_back(Assign::make(ivar, iterator.getSegendVar()));
    }
  }

  auto modeIterators =
      filter(iterators, [](Iterator it){return it.isDimensionIterator();});
  for (auto& iterator : modeIterators) {
    taco_iassert(iterator.isFull());
    Expr ivar = iterator.getIteratorVar();
    result.push_back(compoundAssign(ivar, 1));
  }

  return Block::make(result);
}


static
bool isLastAppender(Iterator iter) {
  taco_iassert(iter.hasAppend());
  while (!iter.isLeaf()) {
    iter = iter.getChild();
    if (iter.hasAppend()) {
      return false;
    }
  }
  return true;
}


Stmt LowererImpl::appendCoordinate(vector<Iterator> appenders, Expr coord) {
  vector<Stmt> result;
  for (auto& appender : appenders) {
    Expr pos = appender.getPosVar();
    Iterator appenderChild = appender.getChild();

    if (appenderChild.defined() && appenderChild.isBranchless()) {
      // Already emitted assembly code for current level when handling 
      // branchless child level, so don't emit code again.
      continue;
    }

    vector<Stmt> appendStmts;

    if (generateAssembleCode()) {
      appendStmts.push_back(appender.getAppendCoord(pos, coord));
      while (!appender.isRoot() && appender.isBranchless()) {
        // Need to append result coordinate to parent level as well if child 
        // level is branchless (so child coordinates will have unique parents).
        appender = appender.getParent();
        if (!appender.isRoot()) {
          taco_iassert(appender.hasAppend()) << "Parent level of branchless, "
              << "append-capable level must also be append-capable";
          taco_iassert(!appender.isUnique()) << "Need to be able to insert " 
              << "duplicate coordinates to level, but level is declared unique";

          Expr coord = getCoordinateVar(appender);
          appendStmts.push_back(appender.getAppendCoord(pos, coord));
        }
      }
    } 
    
    if (generateAssembleCode() || isLastAppender(appender)) {
      appendStmts.push_back(compoundAssign(pos, 1));

      Stmt appendCode = Block::make(appendStmts);
      if (appenderChild.defined() && appenderChild.hasAppend()) {
        // Emit guard to avoid appending empty slices to result.
        // TODO: Users should be able to configure whether to append zeroes.
        Expr shouldAppend = Lt::make(appenderChild.getBeginVar(), 
                                     appenderChild.getPosVar());
        appendCode = IfThenElse::make(shouldAppend, appendCode);
      }
      result.push_back(appendCode);
    }
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Stmt LowererImpl::generateAppendPositions(vector<Iterator> appenders) {
  vector<Stmt> result;
  if (generateAssembleCode()) {
    for (Iterator appender : appenders) {
      if (!appender.isBranchless()) {
        Expr pos = [](Iterator appender) {
          // Get the position variable associated with the appender. If a mode 
          // is above a branchless mode, then the two modes can share the same 
          // position variable.
          while (!appender.isLeaf() && appender.getChild().isBranchless()) {
            appender = appender.getChild();
          }
          return appender.getPosVar();
        }(appender);
        Expr beginPos = appender.getBeginVar();
        Expr parentPos = appender.getParent().getPosVar();
        result.push_back(appender.getAppendEdges(parentPos, beginPos, pos));
      }
    }
  }
  return result.empty() ? Stmt() : Block::make(result);
}


Expr LowererImpl::generateValueLocExpr(Access access) const {
  if (isScalar(access.getTensorVar().getType())) {
    return ir::Literal::make(0);
  }
  Iterator it = getIterators(access).back();
  return it.getPosVar();
}


Expr LowererImpl::checkThatNoneAreExhausted(std::vector<Iterator> iterators)
{
  taco_iassert(!iterators.empty());
  if (iterators.size() == 1 && iterators[0].isFull()) {
    Expr dimension = getDimension(iterators[0].getIndexVar());
    return Lt::make(iterators[0].getIteratorVar(), dimension);
  }

  vector<Expr> result;
  for (const auto& iterator : iterators) {
    taco_iassert(!iterator.isFull()) << iterator
        << " - full iterators do not need to partake in merge loop bounds";
    Expr iterUnexhausted = Lt::make(iterator.getIteratorVar(),
                                    iterator.getEndVar());
    result.push_back(iterUnexhausted);
  }

  return (!result.empty())
         ? conjunction(result)
         : Lt::make(iterators[0].getIteratorVar(), iterators[0].getEndVar());
}

}
