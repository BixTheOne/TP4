from noeud import Noeud

addition = Noeud("+")
addition.ajouter_noeud(Noeud(2))
addition.ajouter_noeud(Noeud("y"))

expression = Noeud("exp")
expression.ajouter_noeud(addition)

print(expression.afficher_expression())
print(expression.evaluer({"y": 1}))

try:
    expression.evaluer({})
except ValueError as erreur:
    print(erreur)

a_simplifier = Noeud("+", [Noeud("*", [Noeud(1), Noeud("x")]), Noeud("+", [Noeud(1), Noeud("exp", [Noeud(0)])])])
print(a_simplifier.afficher_expression())
print(a_simplifier.simplifiee().afficher_expression())

a_deriver = Noeud("*", [Noeud(3), Noeud("sin", [Noeud("x")])])
print(a_deriver.derivee("x").afficher_expression())
print(a_deriver.derivee("x").simplifiee().afficher_expression())

expression.tracer("y", [i / 10 for i in range(-50, 21)])
