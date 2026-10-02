import copy
import math
import matplotlib.pyplot as plt

class Noeud:
    def __init__(self, valeur, enfants=None):
        self.valeur = valeur
        self.enfants = enfants if enfants is not None else []
   
    
    def ajouter_noeud(self, noeud):     # Question 2
        """Ajoute un noeud à la liste d'enfants
        Parameters
        ------
        self : Noeud
        noeud actuel
        noeud : Noeud
        
        """
        self.enfants.append(noeud)

    
    def afficher_expression(self):      # Question 3
        if not self.enfants:
            return str(self.valeur)
        else:
            enfants_expressions = [enfant.afficher_expression() for enfant in self.enfants]
            return f"{self.valeur} {' '.join(enfants_expressions)}"

    def evaluer(self, variables):       # Question 5
        if not self.enfants:
            if isinstance(self.valeur, str):
                if self.valeur not in variables:
                    raise ValueError(f"Valeur manquante pour la variable: {self.valeur}")
                return float(variables[self.valeur])
            return float(self.valeur)
        else:
            if self.valeur == '+':
                return sum(enfant.evaluer(variables) for enfant in self.enfants)
            elif self.valeur == '-':
                return self.enfants[0].evaluer(variables) - sum(enfant.evaluer(variables) for enfant in self.enfants[1:])
            elif self.valeur == '*':
                result = 1.0
                for enfant in self.enfants:
                    result *= enfant.evaluer(variables)
                return result
            elif self.valeur == '/':
                result = self.enfants[0].evaluer(variables)
                for enfant in self.enfants[1:]:
                    result /= enfant.evaluer(variables)
                return result
            elif self.valeur == 'sin':
                return math.sin(self.enfants[0].evaluer(variables))
            elif self.valeur == 'cos':
                return math.cos(self.enfants[0].evaluer(variables))
            elif self.valeur == 'exp':
                return math.exp(self.enfants[0].evaluer(variables))
            elif self.valeur == 'log':
                return math.log(self.enfants[0].evaluer(variables))
            else:
                raise ValueError(f"Opérateur inconnu: {self.valeur}")
    
    def tracer(self, variable, valeurs):  # Question 6
        resultats = [self.evaluer({variable: valeur}) for valeur in valeurs]
        plt.plot(valeurs, resultats)
        plt.xlabel(variable)
        plt.title(self.afficher_expression())
        plt.show()

    def contient_variable(self):
        if not self.enfants:
            return isinstance(self.valeur, str)
        return any(enfant.contient_variable() for enfant in self.enfants)

    def est_constante(self, valeur):
        return not self.enfants and not isinstance(self.valeur, str) and self.valeur == valeur

    def simplifiee(self):               # Question 7
        if not self.enfants:
            return Noeud(self.valeur)
        if not self.contient_variable():
            try:
                return Noeud(self.evaluer({}))
            except (ValueError, ZeroDivisionError):
                pass
        enfants = [enfant.simplifiee() for enfant in self.enfants]
        if self.valeur == '*':
            if any(enfant.est_constante(0) for enfant in enfants):
                return Noeud(0)
            enfants = [enfant for enfant in enfants if not enfant.est_constante(1)]
            if not enfants:
                return Noeud(1)
        elif self.valeur == '+':
            enfants = [enfant for enfant in enfants if not enfant.est_constante(0)]
            if not enfants:
                return Noeud(0)
        elif self.valeur == '-':
            enfants = enfants[:1] + [enfant for enfant in enfants[1:] if not enfant.est_constante(0)]
        elif self.valeur == '/':
            if enfants[0].est_constante(0):
                return Noeud(0)
            enfants = enfants[:1] + [enfant for enfant in enfants[1:] if not enfant.est_constante(1)]
        if len(enfants) == 1 and self.valeur in ('*', '+', '-', '/'):
            return enfants[0]
        return Noeud(self.valeur, enfants)

    def derivee(self, variable):        # Question 8
        if not self.enfants:
            return Noeud(1 if self.valeur == variable else 0)
        u = copy.deepcopy(self.enfants[0])
        du = self.enfants[0].derivee(variable)
        if self.valeur in ('+', '-'):
            return Noeud(self.valeur, [enfant.derivee(variable) for enfant in self.enfants])
        elif self.valeur == '*':
            termes = []
            for i, enfant in enumerate(self.enfants):
                facteurs = [copy.deepcopy(autre) for j, autre in enumerate(self.enfants) if j != i]
                termes.append(Noeud('*', [enfant.derivee(variable)] + facteurs))
            return Noeud('+', termes)
        elif self.valeur == '/':
            if len(self.enfants) > 2:
                v = Noeud('*', copy.deepcopy(self.enfants[1:]))
            else:
                v = copy.deepcopy(self.enfants[1])
            dv = v.derivee(variable)
            numerateur = Noeud('-', [Noeud('*', [du, v]), Noeud('*', [u, dv])])
            return Noeud('/', [numerateur, Noeud('*', [copy.deepcopy(v), copy.deepcopy(v)])])
        elif self.valeur == 'sin':
            return Noeud('*', [Noeud('cos', [u]), du])
        elif self.valeur == 'cos':
            return Noeud('-', [Noeud(0), Noeud('*', [Noeud('sin', [u]), du])])
        elif self.valeur == 'exp':
            return Noeud('*', [Noeud('exp', [u]), du])
        elif self.valeur == 'log':
            return Noeud('/', [du, u])
        else:
            raise ValueError(f"Opérateur inconnu: {self.valeur}")