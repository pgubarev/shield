__all__ = ("one_call_per_context_cache_decorator",)

from typing import Any

from shield.type_annotations import TContext, TContextCachableFunction


def one_call_per_context_cache_decorator(
    function: TContextCachableFunction,
) -> TContextCachableFunction:
    """Декоратор позволяет выполнять сложные функции только один раз в рамках
    одного контекста, вне зависимости от того как много раз из вызывали.
    Это позволяет описывать сложные правила для доступа с повторяющимися
    условиями в отрыве друг от друга, что уменьшает их сложность."""

    def wrapper(context: TContext, *args: Any, **kwargs: Any):
        cache_attr = f"_{function.__name__}_cache"
        if not hasattr(context, cache_attr):
            result = function(context, *args, **kwargs)
            setattr(context, cache_attr, result)

        return getattr(context, cache_attr)

    return wrapper
