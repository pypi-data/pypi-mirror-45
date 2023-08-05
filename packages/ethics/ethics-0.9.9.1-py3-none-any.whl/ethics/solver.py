from pysat.solvers import Solver
from ethics.language import *
from ethics.tools import *

def theorySAT(cand_model):
    """ A Solver for Simple Causal Agency Logic
    
    Keyword arguments:
    cand_model --- A list of literals to be checked for consistency
    """
    for m in cand_model:
        if isinstance(m, Good):
            if Bad(m.f1) in cand_model:
                return False
            if Neutral(m.f1) in cand_model:
                return False
        if isinstance(m, Bad):
            if Good(m.f1) in cand_model:
                return False
            if Neutral(m.f1) in cand_model:
                return False
        if isinstance(m, Neutral):
            if Good(m.f1) in cand_model:
                return False
            if Bad(m.f1) in cand_model:
                return False
        if isinstance(m, Causes):
            if Not(m.f1).nnf() in cand_model:
                #print("causes: notf1")
                return False
            if Not(m.f2).nnf() in cand_model:
                #print("causes: notf2")
                return False
            if m.f1 != m.f2 and Causes(m.f2, m.f1) in cand_model:
                #print("causes: symmetry", m)
                return False
            if m == Causes(m.f1, Not(m.f1).nnf()):
                #print("causes: notff")
                return False
            if Causes(m.f1, Not(m.f2).nnf()) in cand_model:
                #print("causes: f1notf2")
                return False
            if Causes(Not(m.f1).nnf(), m.f2) in cand_model:
                #print("causes: notf1nf2")
                return False
        if isinstance(m, Not) and isinstance(m.f1, Causes) and m.f1.f1 == m.f1.f2:
            #print("notcauses", m)
            return False
        if isinstance(m, Not) and isinstance(m.f1, Eq) and m.f1.f1 == m.f1.f2:
            #print("noteq")
            return False
        if isinstance(m, Eq):
            if Gt(m.f1, m.f2) in cand_model:
                #print("eqgt")
                return False
        if isinstance(m, GEq):
            if Gt(m.f2, m.f1) in cand_model:
                #print("geqgt", m)
                return False
        if isinstance(m, Gt):
            if Gt(m.f2, m.f1) in cand_model:
                return False
            if GEq(m.f2, m.f1) in cand_model:
                return False
            if Eq(m.f1, m.f2) in cand_model:
                return False
            if Eq(m.f2, m.f1) in cand_model:
                return False
    
    return True
    
    
def smtAllModels(formula):
    """
    formula --- must be in CNF
    """
    d, m = formula.dimacs()
    s = Solver()
    s.append_formula(d)
    models = []
    for mod in s.enum_models():
        f = mapBackToFormulae(mod, m)
        if theorySAT(f):
            models.append(f)
    s.delete()
    return models
