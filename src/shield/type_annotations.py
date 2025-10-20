__all__ = ("TContext", "TRuleFunction", "TDefinedRules", "TResolvedRulesSet",
           "TContextProtocol")

from collections.abc import Callable
from typing import Any, Protocol, TypeVar


class TContextProtocol(Protocol):
    """Базовый протокол который должен наследовать каждый класс контекста
    для корректной работы аннотации типов"""


TContext = TypeVar("TContext", bound=TContextProtocol)

TRuleFunction = Callable[[Any, TContext], bool]
TDefinedRules = dict[str, TRuleFunction | bool]
TResolvedRulesSet = list[str]


class TContextCachableFunction(Protocol):
    __name__: str

    def __call__(self, context: TContext, *args: Any, **kwargs: Any) -> Any: ...
