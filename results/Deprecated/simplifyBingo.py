"""
Created on Sat Oct 17 22:30:57 2020

@author: u1117676
"""

from sympy.parsing.sympy_parser import parse_expr, standard_transformations
import re
from sympy import simplify

Eq1 = "(-10.000253596203713 + -10.000253596203713 - ((-10.000253596203713)(-10.000253596203713) - ((X_0 + -10.000253596203713)(X_0))) + (-10.000253596203713 + -10.000253596203713)/(-10.000253596203713)  - (-10.000253596203713) - ((-10.000253596203713)(-10.000253596203713) - ((X_0 + -10.000253596203713)(X_0))) + (-10.000253596203713 + -10.000253596203713)/(-10.000253596203713) )((1.0241858250175548e-06)((X_0 + -10.000253596203713)(X_0) + ((-10.000253596203713 + -10.000253596203713)/(-10.000253596203713) )(((X_0 + X_0 + X_0)(X_0 + X_0 + X_0))(1.0241858250175548e-06))))"
Equations = [Eq1]
EquationsIndex = ['Eq1']


def bingosimplify(expression, XType='X_0'):
    if isinstance(expression, str):
        # finds all the floats inside of the string output. It will prioritize the earlier or's. (Seperated by | )
        V = re.findall('[0-9]+\.[0-9]+[e]...|\-[0-9]+\.[0-9]+[e]...|[0-9]+\.[0-9]+|\-[0-9]+\.[0-9]+', expression);
        # Find all gives us all of the numbers, including repeats. VFilters out all the repeat values.
        VFiltered = list(set(V))

        # Bit of a hard code to change later. Sets a list of letters for variables to be assigned to.
        Variables = ['A', 'B', 'C', 'D', 'F', 'G', 'H']

        # All of the bellow are clean up methods to make sure that sympy can understand the string. I could have them iterate everytime, but assigning individual variables made debugging easier.
        ExpressionV1 = re.sub(XType, 'x', expression)  # Replaces input XType with x
        ExpressionV2 = re.sub('[)][(]', ')*(', ExpressionV1)  # Adds asterisks where ever parentheses face eachother.
        ExpressionV3 = re.sub('\^', '**', ExpressionV2)  # Replaces all ^ with the more standard **
        ExpressionV4 = ExpressionV3

        # The loop bellow cycles through the equation replacing every number with its corresponding variable.
        for i in range(0, len(VFiltered)):
            ExpressionV4 = re.sub(VFiltered[i], Variables[i], ExpressionV4)
            replacements = [(Variables[j], VFiltered[j]) for j in
                            range(len(VFiltered))]  # Logs what replacements were made, so they can be reinserted later.

        # Parse expresssion simplifies all of the common letter variables out by giving it the imput standard_transformations
        try:
            ExpressionV5 = parse_expr(ExpressionV4, transformations=standard_transformations)
        except:
            raise ValueError('Expression has notation not accounted for in bingosimplify')
        ExpressionV6 = ExpressionV5.subs(replacements)  # Reinserting the numbers back into the equation.
        ExpressionV7 = simplify(
            ExpressionV6)  # Giving sympy simplify another go at it, this time with numbers. Hopefully with alot less truncation.
        return ExpressionV7
    else:
        return ValueError('Input not string')


for j in range(0, len(Equations)):
    sol = bingosimplify(Equations[j])
    print(sol)
