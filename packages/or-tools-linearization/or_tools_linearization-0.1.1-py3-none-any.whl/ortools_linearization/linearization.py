class PieceWiseLinearization(object):
    def __init__(self):
        self.linearized = None

    def generate_var(self,
                     solver,
                     var_lower,
                     var_upper,
                     var_name,
                     underlying_decision_var,
                     objective_coefficient=None) -> (
            "operations_research::MPVariable *", "operations_research::MPConstraint *"):
        """
        Generates a decision variable `z` that approximates the piece-wise linearized function.
        This function will append multiple constraints to the solver as well as `z` to the objective function.
        :param solver:
        :param var_lower: Decision variable lower bound.
        :param var_upper: Decision variable upper bound.
        :param var_name: The new decision variable's name.
        :param underlying_decision_var: If `f(x)` is the convex function then `underlying_decision_var` is `x`.
        :param objective_coefficient: The coefficient of `z` in the objective function. Defaults to +/-1.0.
        :return: Returns the new decision variable and the list of constraints
        """
        if self.linearized is None:
            raise AssertionError("Linearizer has not been initialized with a function yet. "
                                 "Either call `linearize(..)` or set `linearized`.")

        z = solver.NumVar(
            var_lower,
            var_upper,
            var_name)

        constraints = []
        for linear_piece in self.linearized.pieces:
            constraint = solver.Constraint(linear_piece.c, solver.infinity())
            constraint.SetCoefficient(z, 1.0)
            constraint.SetCoefficient(underlying_decision_var, -linear_piece.a)
            constraints.append(constraint)

        objective = solver.Objective()

        if objective_coefficient is None:
            objective_coefficient = 1.0 if objective.minimization() else -1.0

        if objective.minimization() and objective_coefficient < 0:
            raise AssertionError("Coefficient must be positive for a minimization problem.")
        elif not objective.minimization() and objective_coefficient > 0:
            raise AssertionError("Coefficient must be negative for maximization problem.")

        objective.SetCoefficient(z, objective_coefficient)

        return z, constraints

    def linearize(self, convex_function, lower, upper, step):
        if lower >= upper:
            raise AssertionError("lower must be strictly less than upper.")

        pieces = []

        x = lower
        while x < upper:
            lower_value = convex_function(x)
            upper_value = convex_function(x + step)

            a = (upper_value - lower_value) / step
            c = lower_value - a * x
            pieces.append(LinearPiece(a, c, x, x + step))

            x = x + step

        self.linearized = LinearizedFunction(pieces)

        return self.linearized


class LinearizedFunction(object):
    def __init__(self, pieces):
        self.pieces = pieces

    def compute(self, x):
        piece = next(p for p in self.pieces if p.contains(x))
        return piece.compute(x)


class LinearPiece(object):
    def __init__(self, a, c, lower, upper):
        self.a = a
        self.c = c
        self.lower = lower
        self.upper = upper

    def contains(self, x):
        return self.lower <= x < self.upper

    def compute(self, x):
        return self.a * x + self.c

    def __str__(self) -> str:
        return "{}x + {}    if {} <= x <= {}".format(self.a, self.c, self.lower, self.upper)
