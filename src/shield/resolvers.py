__all__ = ("Resolver",)

from typing import cast

from shield.context import DictContext
from shield.exceptions import ShieldPermissionDenied
from shield.type_annotations import (
    TContext,
    TDefinedRules,
    TResolvedRulesSet,
)


class Resolver[TResolverInstanceObject]:
    """Базовый класс для всех пользовательских Resolver-классов.
    При описании пользовательского Resolver-класса нужно Resolver как родителя,
    с указанием типа для instance, а также переопределить метод define_rules.
    """

    # Переопределение context_class может быть полез в случаях,
    # когда нужно определить свою логику для получения информации
    # о пользователи или объекте для которого нужно вычислить
    # доступные действия.
    context_class: type[TContext] = DictContext

    # Переопределение permission_denied_class может быть полезно,
    # если можно создавать автоматически ответ сервера на основании
    # выброшенного исключения. Например, можно выбрасывать исключение из пакета
    # django_rest_framework, в таком случае ответ сервера будет сгенерирован
    # автоматически.
    permission_denied_class: type[Exception] = ShieldPermissionDenied

    def __init__(self):
        self._rules: TDefinedRules = self.define_rules()
        self._instance: TResolverInstanceObject | None = None
        self._context: TContext = None

    @property
    def instance(self) -> TResolverInstanceObject:
        return cast(TResolverInstanceObject, self._instance)

    def set_context(self, instance: TResolverInstanceObject = None,
                    context_provider: TContext = None, **context_init_kwargs):
        if context_provider is None:
            context_provider = self.context_class(**context_init_kwargs)

        self._context = context_provider
        self._instance = instance

    def define_rules(self) -> TDefinedRules:
        raise NotImplementedError

    def has_permission(self, permission: str) -> bool:
        self._ensure_context_provided()

        if permission not in self._rules:
            raise ValueError(f"Unknown permission: {permission}")

        rule = self._rules[permission]

        if not isinstance(rule, bool):
            return rule(self._instance, self._context)

        return rule

    def ensure_has_permission(self, permission: str) -> None:
        has_permission = self.has_permission(permission)
        if not has_permission:
            raise self.permission_denied_class(permission)

    def resolve_all(self) -> TResolvedRulesSet:
        self._ensure_context_provided()

        permissions: list[str] = []
        for permission, rule in self._rules.items():
            has_permission = (
                rule(self._instance, self._context)
                if not isinstance(rule, bool)
                else bool(rule)
            )

            if has_permission:
                permissions.append(permission)

        return permissions

    def _ensure_context_provided(self):
        if self._context is None:
            raise RuntimeError("context is not provided")
