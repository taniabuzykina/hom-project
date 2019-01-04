from sympy import Poly, Symbol
from sympy.solvers.inequalities import reduce_rational_inequalities as reduce
from sympy.solvers.inequalities import solve_rational_inequalities as solve

#result = reduce([[0 <= x + 3]],x)

x, y = Symbol('x'), Symbol('y')

result = solve([[
    ((Poly(x + y), Poly(x**2)), '>=')]])

print(result)


