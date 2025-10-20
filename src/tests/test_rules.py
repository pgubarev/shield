from unittest.mock import Mock

from shield.rules import ConstantRuleValue, Rule, rule


def test_constant_rule_value():
    result = bool(ConstantRuleValue(False))
    assert not result, "Invalid result"

    result = bool(ConstantRuleValue(True))
    assert result, "Invalid result"

    result = bool(~ConstantRuleValue(True))
    assert not result, "Invalid result"

    result = bool(~ConstantRuleValue(False))
    assert result, "Invalid result"


def test_rule_decorator():
    mock_function = Mock(return_value=False)

    decorated = rule(mock_function)
    result = decorated(None)

    assert not result
    assert mock_function.called


def test_rule_combination_for_and_operand():
    constant_true = ConstantRuleValue(True)
    constant_false = ConstantRuleValue(False)

    mock_function = Mock(return_value=False)
    rule_with_mock = Rule(mock_function)

    result = constant_true & rule_with_mock
    assert rule_with_mock == result

    result = constant_false & rule_with_mock
    assert constant_false == result
