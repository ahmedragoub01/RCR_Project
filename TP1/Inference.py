from pysat.formula import CNF
from pysat.solvers import Solver


class KnowledgeBase:
    def __init__(self):
        self.clauses = []


    def add_clause(self, clause):
        self.clauses.append(clause)


    def add_formula(self, formula):
        for clause in formula:
            self.add_clause(clause)


    def to_cnf(self):
        cnf = CNF()
        for clause in self.clauses:
            cnf.append(clause)
        return cnf


def is_satisfiable(cnf):
    solver = Solver(name='g3')
    solver.append_formula(cnf)
    result = solver.solve()
    solver.delete()
    return result


def infers(kb, formula):
    kb_copy = KnowledgeBase()
    for clause in kb.clauses:
        kb_copy.add_clause(clause)


    if isinstance(formula, list):
        for literal in formula:
            kb_copy.add_clause([-literal])
    else:
        kb_copy.add_clause([-formula])


    cnf = kb_copy.to_cnf()
    satisfiable = is_satisfiable(cnf)
    return not satisfiable


def main():
    kb = KnowledgeBase()
    kb.add_clause([1, 2])
    kb.add_clause([-2, 3])


    formula = [1, 3]
    result = infers(kb, formula)
    print(f"La base de connaissances infère-t-elle (A ∨ C) ? {result}")


    result = infers(kb, 3)
    print(f"La base de connaissances infère-t-elle C ? {result}")


if __name__ == "__main__":
    main()