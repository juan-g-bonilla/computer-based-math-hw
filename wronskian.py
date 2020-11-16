import sympy as sp

def wronskian(var, *funcs):
    """
    Computes the Wroskian for a set a functions 'funcs' that depend on 'var'

    Returns an expression
    """
    M = sp.zeros(0) # Initialize

    for i in range(len(funcs)):
        der = sp.Matrix([sp.diff(f, var, i) for f in funcs]).transpose()
        M = M.row_insert(i, der)

    return M.det().simplify()

def is_linearly_indep(var, *funcs):
    """
    Returns True iff the functions 'funcs' are linearly independant
    """
    return not wronskian(var, *funcs).equals(0) # Numerically check equality

def test():
    x= sp.symbols('x')
    # Check wronskian returns expected expressions
    assert wronskian(x, 2*x, 3*x**2, x**3 + x**2) == 12*x**3
    assert wronskian(x, sp.cos(x), sp.sin(x), sp.sin(2*x)) == -3*sp.sin(2*x)
    assert wronskian(x, sp.exp(2*x), sp.exp(x)) == - sp.exp(3*x)

    # Check is_linearly_indep returns expected results
    assert is_linearly_indep(x, 2*x, 3*x**2, x**3 + x**2)
    assert is_linearly_indep(x, sp.cos(x), sp.sin(x), sp.sin(2*x))
    assert not is_linearly_indep(x, 2*x, 3*x, x**3 + x**2)
    assert not is_linearly_indep(x, sp.cos(x), 5 + 3*sp.cos(x), sp.pi)

def main():
    x= sp.symbols('x')
    set_funcs = [2*x, 3*x**2, x**3 + x**2]
    indep = is_linearly_indep(x, *set_funcs)
    print("Functions " + str(set_funcs) + " are linearly independent: {}".format(indep)) 

if __name__ == "__main__":
    test() # Uncomment to unit-test functions
    main()