class Formula(object):
    """
    Classes to programmatically build
    and represent formulae and terms of the language
    specified in Definition 1.
    """
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def nnf(self):
        if(isinstance(self, str)):
            return self
        if(isinstance(self, Not)):
            if(isinstance(self.f1, Not)):
                return self.f1.f1 if isinstance(self.f1.f1, str) else self.f1.f1.nnf()
            if(isinstance(self.f1, And)):
                return Or(Not(self.f1.f1).nnf(), Not(self.f1.f2).nnf())
            if(isinstance(self.f1, Or)):
                return And(Not(self.f1.f1).nnf(), Not(self.f1.f2).nnf())
            if(isinstance(self.f1, Impl)):
                return Not(Or(Not(self.f1.f1), self.f1.f2)).nnf()
            if(isinstance(self.f1, BiImpl)):
                return Not(Or(And(self.f1.f1, self.f1.f2), And(Not(self.f1.f1), Not(self.f1.f2)))).nnf()
            if(isinstance(self.f1, GEq)):
                return Gt(self.f1.f2, self.f1.f1)
            return self
        if(isinstance(self, And)):
            return And(self.f1 if isinstance(self.f1, str) else self.f1.nnf(), self.f2 if isinstance(self.f2, str) else self.f2.nnf())
        if(isinstance(self, Or)):
            return Or(self.f1 if isinstance(self.f1, str) else self.f1.nnf(), self.f2 if isinstance(self.f2, str) else self.f2.nnf())
        if(isinstance(self, Impl)):
            return Or(Not(self.f1), self.f2).nnf()
        if(isinstance(self, BiImpl)):
            return Or(And(self.f1, self.f2), And(Not(self.f1), Not(self.f2))).nnf()
        return self
        
    def dnf(self, model, principle, mode = "Normal"):
        f = self.nnf()
        while(True):
            fdnf = f.dnf_it(model, principle, mode)
            if(f == fdnf):
                return fdnf
            f = fdnf
        return None
        
    def dnf_it(self, model, principle, mode):
        # (b v c) & a
        if(isinstance(self, And) and isinstance(self.f1, Or)):
            if mode == "Abstract":
                if(model.models(principle.mapSymbolToFormula(Not(self.f1))) or model.models(principle.mapSymbolToFormula(Not(self.f2)))):
                    return "BOTTOM"
                elif(model.models(principle.mapSymbolToFormula(Not(self.f1.f1))) and model.models(principle.mapSymbolToFormula(self.f2)) and model.models(principle.mapSymbolToFormula(self.f1.f2))):
                    return And(self.f1.f2, self.f2).dnf_it(model, principle, mode)
                elif(model.models(principle.mapSymbolToFormula(Not(self.f1.f2))) and model.models(principle.mapSymbolToFormula(self.f2)) and model.models(principle.mapSymbolToFormula(self.f1.f1))):
                    return And(self.f1.f1, self.f2).dnf_it(model, principle, mode)
            else:
                if(model.models(Not(self.f1)) or model.models(Not(self.f2))):
                    return "BOTTOM"
                elif(model.models(Not(self.f1.f1)) and model.models(self.f2) and model.models(self.f1.f2)):
                    return And(self.f1.f2, self.f2).dnf_it(model, principle, mode)
                elif(model.models(Not(self.f1.f2)) and model.models(self.f2) and model.models(self.f1.f1)):
                    return And(self.f1.f1, self.f2).dnf_it(model, principle, mode)
            return Or(And(self.f1.f1, self.f2).dnf_it(model, principle, mode), And(self.f1.f2, self.f2).dnf_it(model, principle, mode))
        # a & (b v c)
        if(isinstance(self, And) and isinstance(self.f2, Or)):
            if mode == "Abstract":
                if(model.models(principle.mapSymbolToFormula(Not(self.f1))) or model.models(principle.mapSymbolToFormula(Not(self.f2)))):
                    return "BOTTOM"
                elif(model.models(principle.mapSymbolToFormula(Not(self.f2.f1))) and model.models(principle.mapSymbolToFormula(self.f1)) and model.models(principle.mapSymbolToFormula(self.f2.f2))):
                    return And(self.f1, self.f2.f2).dnf_it(model, principle, mode)
                elif(model.models(principle.mapSymbolToFormula(Not(self.f2.f2))) and model.models(principle.mapSymbolToFormula(self.f1)) and model.models(principle.mapSymbolToFormula(self.f2.f1))):
                    return And(self.f1, self.f2.f1).dnf_it(model, principle, mode)
            else:
                if(model.models(Not(self.f1)) or model.models(Not(self.f2))):
                    return "BOTTOM"
                elif(model.models(Not(self.f2.f1)) and model.models(self.f1) and model.models(self.f2.f2)):
                    return And(self.f1, self.f2.f2).dnf_it(model, principle, mode)
                elif(model.models(Not(self.f2.f2)) and model.models(self.f1) and model.models(self.f2.f1)):
                    return And(self.f1, self.f2.f1).dnf_it(model, principle, mode)
            return Or(And(self.f1, self.f2.f1).dnf_it(model, principle, mode), And(self.f1, self.f2.f2).dnf_it(model, principle, mode))
        if(isinstance(self, And)):
            return And(self.f1 if isinstance(self.f1, str) else self.f1.dnf_it(model, principle, mode), self.f2 if isinstance(self.f2, str) else self.f2.dnf_it(model, principle, mode))
        if(isinstance(self, Or)):
            return Or(self.f1 if isinstance(self.f1, str) else self.f1.dnf_it(model, principle, mode), self.f2 if isinstance(self.f2, str) else self.f2.dnf_it(model, principle, mode))
        return self   
    
    def cnf(self):
        f = self.nnf()
        while(True):
            fcnf = f.cnf_it()
            if(f == fcnf):
                return fcnf
            f = fcnf
        return None
        
    def cnf_it(self):
        # (b v c) & a
        if(isinstance(self, Or) and isinstance(self.f1, And)):
            return And(Or(self.f1.f1, self.f2).cnf_it(), Or(self.f1.f2, self.f2).cnf_it())
        # a & (b v c)
        if(isinstance(self, Or) and isinstance(self.f2, And)):
            return And(Or(self.f1, self.f2.f1).cnf_it(), Or(self.f1, self.f2.f2).cnf_it())
        if(isinstance(self, And)):
            return And(self.f1 if isinstance(self.f1, str) else self.f1.cnf_it(), self.f2 if isinstance(self.f2, str) else self.f2.cnf_it())
        if(isinstance(self, Or)):
            return Or(self.f1 if isinstance(self.f1, str) else self.f1.cnf_it(), self.f2 if isinstance(self.f2, str) else self.f2.cnf_it())
        return self

    def writeDimacs(self):
        dlist, dmap = self.dimacs()
        d = "p cnf "+str(len(dmap))+" "+str(len(dlist))
        for c in dlist:
            d += "\n"
            if(type(c) is list):
                for cc in c:
                    d += cc + " "
            else:
                d += c + " " 
            d += "0"
        return d, dlist, dmap                 

    def dimacs(self):
        clauses = self.asClauseList()
        dimacs_map = dict()
        counter = 0
        dimacs_list = []
        for c in clauses:
            if type(c) is list:
                clause = []
                for cc in c:
                    if str(cc) in dimacs_map:
                        clause.append(dimacs_map[str(cc)])
                    elif str(Not(cc) if isinstance(cc, str) else cc.getNegation()) in dimacs_map:
                        clause.append(-1*dimacs_map[str(Not(cc)) if isinstance(cc, str) else str(cc.getNegation())])
                    else:
                        counter = counter + 1
                        dimacs_map[str(cc)] = counter
                        clause.append(dimacs_map[str(cc)])
                dimacs_list.append(clause)
            else:
                if str(c) in dimacs_map:
                    dimacs_list.append([dimacs_map[c]])
                elif str(Not(c) if isinstance(c, str) else c.getNegation()) in dimacs_map:
                    dimacs_list.append([-1*dimacs_map[str(Not(c)) if isinstance(c, str) else str(c.getNegation())]])
                else:
                    counter = counter + 1
                    dimacs_map[str(c)] = counter
                    dimacs_list.append([dimacs_map[str(c)]])
        return dimacs_list, dimacs_map

    def asClauseList(self):
        #f = self.cnf()
        f = self
        if(isinstance(f, Or)):
            #print("new clause")
            return [f.getClause()]
        elif(isinstance(f, And)):
            return ([f.f1] if isinstance(f.f1, str) else f.f1.asClauseList()) + ([f.f2] if isinstance(f.f2, str) else f.f2.asClauseList())
        else:
            #print("new clause")
            return [f.getClause()]
            
    def getClause(self):
        if(isinstance(self, Or)):
            return ([self.f1] if isinstance(self.f1, str) else self.f1.getClause()) + ([self.f2] if isinstance(self.f2, str) else self.f2.getClause())
        else:
            return [self]


    def asConjList(self):
        #f = self.dnf()
        f = self
        if(isinstance(f, And)):
            #print("new clause")
            return [f.getConj()]
        elif(isinstance(f, Or)):
            return ([f.f1] if isinstance(f.f1, str) else f.f1.asConjList()) + ([f.f2] if isinstance(f.f2, str) else f.f2.asConjList())
        else:
            #print("new clause")
            return [f.getConj()]
            
    def getConj(self):
        if(isinstance(self, And)):
            return ([self.f1] if isinstance(self.f1, str) else self.f1.getConj()) + ([self.f2] if isinstance(self.f2, str) else self.f2.getConj())
        else:
            return [self]


    def makeConjunction(s):
        """
        >>> Formula.makeConjunction(["a"])
        'a'
        >>> Formula.makeConjunction(["a", "b", "c"])
        And("c", And("b", "a"))
        """
        if isinstance(s, str):
            return s
        f = None
        for e in s:
            if f == None:
                f = e
            else:
                f = And(f, e)
        return f

    def makeDisjunction(s):
        """
        >>> Formula.makeDisjunction(["a"])
        'a'
        >>> Formula.makeDisjunction(["a", "b", "c"])
        Or("c", Or("b", "a"))
        """
        if isinstance(s, str):
            return s
        f = None
        for e in s:
            if f == None:
                f = e
            else:
                f = Or(f, e)
        return f
        
    def substituteVariable(var, new, formula):
        newFormula = repr(formula)
        if isinstance(new, Not):
            newFormula = newFormula.replace("'"+var+"'", ""+repr(new)+"")
        else:
            newFormula = newFormula.replace(var, "'"+new+"'").replace("''","'")
        return eval(newFormula)

    def __eq__(self, other):
        return self.f1 == other.f1 and self.f2 == other.f2 if self.__class__ == other.__class__ else False

    def __hash__(self):
        return hash((self.f1, self.f2))

    def __repr__(self):
        if isinstance(self.f1, str):
            f1 = "'"+self.f1+"'"
        else:
            f1 = str(self.f1)
        if isinstance(self.f2, str):
            f2 = "'"+self.f2+"'"
        else:
            f2 = str(self.f2)

        if isinstance(self, Atom):
            return "Atom("+str(f1)+")"
        if isinstance(self, Good):
            return "Good("+str(f1)+")"
        if isinstance(self, Bad):
            return "Bad("+str(f1)+")"
        if isinstance(self, Neutral):
            return "Neutral("+str(f1)+")"
        if isinstance(self, Not):
            return "Not("+str(f1)+")"
        if isinstance(self, Or):
            return "Or("+str(f1)+", "+str(f2)+")"
        if isinstance(self, And):
            return "And("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Impl):
            return "Impl("+str(f1)+", "+str(f2)+")"
        if isinstance(self, BiImpl):
            return "BiImpl("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Affects):
            return "Affects("+str(f1)+", "+str(f2)+")"
        if isinstance(self, AffectsPos):
            return "AffectsPos("+str(f1)+", "+str(f2)+")"
        if isinstance(self, AffectsNeg):
            return "AffectsNeg("+str(f1)+", "+str(f2)+")"
        if isinstance(self, I):
            return "I("+str(f1)+")"
        if isinstance(self, End):
            return "End("+str(f1)+")"
        if isinstance(self, Means):
            return "Means("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Causes):
            return "Causes("+str(f1)+", "+str(f2)+")"
        if isinstance(self, PCauses):
            return "PCauses("+str(f1)+", "+str(f2)+")"
        if isinstance(self, SCauses):
            return "SCauses("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Explains):
            return "Explains("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Prevents):
            return "Prevents("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Because):
            return "Because("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Intervention):
            return "Intervention("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Exists):
            return "Exists("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Forall):
            return "Forall("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Gt):
            return "Gt("+str(f1)+", "+str(f2)+")"
        if isinstance(self, GEq):
            return "GEq("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Eq):
            return "Eq("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Must):
            return "Must("+str(f1)+")"
        if isinstance(self, May):
            return "May("+str(f1)+")"
        if isinstance(self, K):
            return "K("+str(f1)+")"
        if isinstance(self, Consequence):
            return "Consequence("+str(f1)+")"
        if isinstance(self, Goal):
            return "Goal("+str(f1)+")"
        if isinstance(self, Choice):
            return "Choice("+str(f1)+")"
        if isinstance(self, Patient):
            return "Patient("+str(f1)+")"

    def getPosLiteralsEvent(self):
        """ 
        For Event Formula Only. 
        Make sure that event formulae are 
        conjunctions of literals!
        """
        r = []
        l = self.getAllLiteralsEvent()
        for e in l:
            if isinstance(e, Not):
                r.append(e.f1)
            else:
                r.append(e)
        return r

    def getAllLiteralsEvent(self):
        """ 
        For Event Formula Only. 
        Make sure that event formulae are 
        conjunctions of literals!
        """
        if isinstance(self, Not):
            return [self]
        if isinstance(self, And):
            f1 = []
            f2 = []
            if isinstance(self.f1, str):
                f1 = f1 + [self.f1]
            else:
                f1 = f1 + self.f1.getAllLiteralsEvent()
            if isinstance(self.f2, str):
                f2 = f2 + [self.f2]
            else:
                f2 = f2 + self.f2.getAllLiteralsEvent()
            return f1 + f2

    def stripParentsFromMechanism(self):
        """ Only for preprocessing the mechanisms. """
        if self.f2 is None:
            if isinstance(self.f1, str):
                return [self.f1]
            return self.f1.stripParentsFromMechanism()
        if isinstance(self.f1, str) and isinstance(self.f2, str):
            return [self.f1, self.f2]
        if isinstance(self.f1, str) and not isinstance(self.f2, str):
            return [self.f1] + self.f2.stripParentsFromMechanism()
        if not isinstance(self.f1, str) and isinstance(self.f2, str):
            return [self.f2] + self.f1.stripParentsFromMechanism()
        
        #else:
        #    return self.f1.stripParentsFromMechanism() + self.f2.stripParentsFromMechanism()

    def getNegation(self, c = None):
        if c == None:
            c = self
        if isinstance(c, str):
            return Not(c)
        if isinstance(c, GEq):
            return Gt(c.f2, c.f1)
        if isinstance(c, Not):
            if isinstance(c.f1, Not):
                return self.getNegation(c.f1.f1)
            else:
                return c.f1
        return Not(c)

class Atom(Formula):
    def __init__(self, f1):
        super(Atom, self).__init__(f1, None)
        
class Good(Formula):
    def __init__(self, f1):
        super(Good, self).__init__(f1, None)
        
class Bad(Formula):
    def __init__(self, f1):
        super(Bad, self).__init__(f1, None)
        
class Neutral(Formula):
    def __init__(self, f1):
        super(Neutral, self).__init__(f1, None)

        
class Not(Formula):
    def __init__(self, f1):
        super(Not, self).__init__(f1, None)


class And(Formula):
    def __init__(self, f1, f2):
        super(And, self).__init__(f1, f2)


class Or(Formula):
    def __init__(self, f1, f2):
        super(Or, self).__init__(f1, f2)


class Impl(Formula):
    def __init__(self, f1, f2):
        super(Impl, self).__init__(f1, f2)
        
        
class BiImpl(Formula):
    def __init__(self, f1, f2):
        super(BiImpl, self).__init__(f1, f2)


class Affects(Formula):
    def __init__(self, f1, f2):
        super(Affects, self).__init__(f1, f2)
        
        
class AffectsPos(Formula):
    def __init__(self, f1, f2):
        super(AffectsPos, self).__init__(f1, f2)
        
        
class AffectsNeg(Formula):
    def __init__(self, f1, f2):
        super(AffectsNeg, self).__init__(f1, f2)
        
        
class I(Formula):
    def __init__(self, f1):
        super(I, self).__init__(f1, None)
        
        
class Goal(Formula):
    def __init__(self, f1):
        super(Goal, self).__init__(f1, None)
        
        
class Choice(Formula):
    def __init__(self, f1):
        super(Choice, self).__init__(f1, None)
        
class Patient(Formula):
    def __init__(self, f1):
        super(Patient, self).__init__(f1, None)
        
        
class End(Formula):
    def __init__(self, f1):
        super(End, self).__init__(f1, None)

        
class Means(Formula):
    def __init__(self, f1, f2):
        super(Means, self).__init__(f1, f2)


class K(Formula):
    def __init__(self, f1):
        super(K, self).__init__(f1, None)
        
        
class Consequence(Formula):
    def __init__(self, f1):
        super(Consequence, self).__init__(f1, None)


class May(Formula):
    def __init__(self, f1):
        super(May, self).__init__(f1, None)


class Must(Formula):
    def __init__(self, f1):
        super(Must, self).__init__(f1, None)


class Causes(Formula):
    def __init__(self, f1, f2):
        super(Causes, self).__init__(f1, f2)


class PCauses(Formula):
    def __init__(self, f1, f2):
        super(PCauses, self).__init__(f1, f2)


class SCauses(Formula):
    def __init__(self, f1, f2):
        super(SCauses, self).__init__(f1, f2)


class Explains(Formula):
    def __init__(self, f1, f2):
        super(Explains, self).__init__(f1, f2)


class Prevents(Formula):
    def __init__(self, f1, f2):
        super(Prevents, self).__init__(f1, f2)


class Intervention(Formula):
    def __init__(self, f1, f2):
        super(Intervention, self).__init__(f1, f2)
        
        
class Exists(Formula):
    def __init__(self, f1, f2):
        super(Exists, self).__init__(f1, f2)
        
        
class Forall(Formula):
    def __init__(self, f1, f2):
        super(Forall, self).__init__(f1, f2)


class Eq(Formula):
    def __init__(self, f1, f2):
        super(Eq, self).__init__(f1, f2)


class Gt(Formula):
    def __init__(self, f1, f2):
        super(Gt, self).__init__(f1, f2)


class GEq(Formula):
    def __init__(self, f1, f2):
        super(GEq, self).__init__(f1, f2)


class Because(Formula):
    def __init__(self, f1, f2):
        super(Because, self).__init__(f1, f2)

class Term(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2 if self.__class__ == other.__class__ else False

    def __hash__(self):
        return hash((self.t1, self.t2))

    def __repr__(self):
        if isinstance(self.t1, str):
            t1 = "'"+self.t1+"'"
        else:
            t1 = str(self.t1)
        if isinstance(self.t2, str):
            t2 = "'"+self.t2+"'"
        else:
            t2 = str(self.t2)

        if isinstance(self, U):
            return "U("+str(t1)+")"
        if isinstance(self, DR):
            return "DR("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, DB):
            return "DB("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, Minus):
            return "Minus("+str(t1)+")"
        if isinstance(self, Sub):
            return "Sub("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, Add):
            return "Add("+str(t1)+", +"+str(t2)+")"

class U(Term):
    def __init__(self, t1):
        super(U, self).__init__(t1, None)

        
class DR(Term):
    def __init__(self, t1, t2):
        super(DR, self).__init__(t1, t2)
        
        
class DB(Term):
    def __init__(self, t1, t2):
        super(DB, self).__init__(t1, t2)


class Minus(Term):
    def __init__(self, t1):
        super(Minus, self).__init__(t1, None)


class Sub(Term):
    def __init__(self, t1, t2):
        super(Sub, self).__init__(t1, t2)


class Add(Term):
    def __init__(self, t1, t2):
        super(Add, self).__init__(t1, t2)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

