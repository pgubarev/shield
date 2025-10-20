__all__ = ("Rule", "ConstantRuleValue", "as_constant", "rule")

from typing import Any

from shield.type_annotations import TContext, TRuleFunction


class Rule:
    """Класс для описания условия. """

    def __init__(self, function: TRuleFunction):
        self._function: TRuleFunction = function

    def __call__(self, instance: Any, context: TContext) -> bool:
        return self._function(instance, context)

    def __and__(
        self,
        other: "Rule | ConstantRuleValue",
    ) -> "Rule | ConstantRuleValue":
        if isinstance(other, ConstantRuleValue):
            # Если other это False, то нет смысла выполнять условие,
            # общий результат всегда будет False.
            # Если other это True, то нет смысла производить комбинирование,
            # общий результат будет зависеть от результата выполнения
            # текущего условия
            if other:
                return self

            return other

        new_rule = lambda instance, context: (
            self(instance, context) and other(instance, context)
        )
        return self.__class__(new_rule)

    def __or__(
        self,
        other: "Rule | ConstantRuleValue",
    ) -> "Rule | ConstantRuleValue":
        if isinstance(other, ConstantRuleValue):
            # Если other это True, то нет смысла выполнять условие,
            # общий результат всегда будет True.
            # Если other это Fa;se, то нет смысла производить комбинирование,
            # общий результат будет зависить от результата выполнения
            # текущего условия
            if not other:
                return self

            return other

        new_rule = lambda instance, context: (
            self(instance, context) or other(instance, context)
        )
        return self.__class__(new_rule)

    def __invert__(self):
        new_rule = lambda instance, context: not self(instance, context)
        return self.__class__(new_rule)


class ConstantRuleValue:
    """Класс обертка над bool значениями, которая позволяет комбинировать
    bool и Rule, в случаях если bool значение находится слева."""

    def __init__(self, value: bool):
        self._value: bool = value

    def __call__(self, instance: Any, context: TContext) -> bool:
        return self._value

    def __and__(
        self,
        other: "Rule | ConstantRuleValue",
    ) -> "Rule | ConstantRuleValue":
        if not self._value:
            # Для AND операций нет смысла производить комбинацию,
            # если текущее значение False
            return self

        # Если текущее значение True, то результат зависит от
        # правого операнда, вне зависимости от его типа
        return other

    def __or__(
        self,
        other: "Rule | ConstantRuleValue",
    ) -> "Rule | ConstantRuleValue":
        if self._value:
            # Для OR операций нет смысла производить комбинацию,
            # если текущее значение True
            return self

        # Если текущее значение False, то результат зависит от
        # правого операнда, вне зависимости от его типа
        return other

    def __invert__(self):
        self._value = not self._value
        return self

    def __bool__(self) -> bool:
        return self._value

def rule(function: TRuleFunction):
    return Rule(function)


as_constant = ConstantRuleValue
