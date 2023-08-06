import unittest
from unittest.mock import MagicMock, call

from linearization import PieceWiseLinearization


class LinearizationTest(unittest.TestCase):

    def setUp(self) -> None:
        self.linearization = PieceWiseLinearization()
        self.solver_mock = MagicMock()
        self.objective_mock = MagicMock()
        self.solver_mock.Objective = MagicMock(return_value=self.objective_mock)
        self.objective_mock.minimization = MagicMock(return_value=True)
        self.objective_mock.maximization = MagicMock(return_value=False)

    def test_generate_var_negative_coefficient_with_minimization_throw_exception(self):
        self.linearization.linearized = MagicMock()
        # solver_mock is already setUp to pretend to be a min problem
        self.assertRaises(AssertionError, self.linearization.generate_var,
                          solver=self.solver_mock, var_lower=0, var_upper=1, var_name='name',
                          underlying_decision_var=None, objective_coefficient=-1.0)

    def test_generate_var_positive_coefficient_with_maximization_throw_exception(self):
        self.linearization.linearized = MagicMock()
        self.objective_mock.minimization = MagicMock(return_value=False)
        self.objective_mock.maximization = MagicMock(return_value=True)
        self.assertRaises(AssertionError, self.linearization.generate_var,
                          solver=self.solver_mock, var_lower=0, var_upper=1, var_name='name',
                          underlying_decision_var=None, objective_coefficient=1.0)

    def test_generate_var_without_linearize_call_throw_exception(self):
        self.assertRaises(AssertionError, self.linearization.generate_var,
                          solver=None, var_lower=0, var_upper=1, var_name='name', underlying_decision_var=None)

    def test_generate_var_success_case(self):
        decision_var_mock = MagicMock()
        self.solver_mock.NumVar = MagicMock(return_value=decision_var_mock)
        input_decision_var_mock = MagicMock()

        linearized = self.linearization.linearize(
            lambda x: (x + 3) ** 2,
            lower=0,
            upper=3,
            step=1)

        self.linearization.generate_var(self.solver_mock, 0, 10, 'name_42', input_decision_var_mock, 4.2)

        # assert that constraints are created
        constraint_calls = []
        for piece in linearized.pieces:
            constraint_calls.append(call(piece.c, self.solver_mock.infinity()))
            constraint_calls.append(call().SetCoefficient(decision_var_mock, 1.0))
            constraint_calls.append(call().SetCoefficient(input_decision_var_mock, -piece.a))
        self.solver_mock.Constraint.assert_has_calls(constraint_calls, any_order=True)

        # assert that new decision var is added to the objective function correctly
        self.objective_mock.SetCoefficient.assert_called_once_with(decision_var_mock, 4.2)

    def test_quadratic_linearize(self):
        result = self.linearization.linearize(
            lambda x: (x + 3) ** 2,
            lower=0,
            upper=3,
            step=1)

        self.assertEqual(3, len(result.pieces))

        self.assertEqual(7, result.pieces[0].a)
        self.assertEqual(9, result.pieces[1].a)
        self.assertEqual(11, result.pieces[2].a)

        self.assertEqual(9, result.pieces[0].c)
        self.assertEqual(7, result.pieces[1].c)
        self.assertEqual(3, result.pieces[2].c)

    def test_linearize_lower_equal_to_upper(self):
        self.assertRaises(AssertionError, self.linearization.linearize,
                          convex_function=lambda x: x, lower=1, upper=1, step=0.1)


if __name__ == '__main__':
    unittest.main()
