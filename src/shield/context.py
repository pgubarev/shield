from shield.type_annotations import TContextProtocol


class DictContext(TContextProtocol):
    """Простая обертка над словарем, которая позволяет получать доступ
    к элементам словаря в стиле свойств объекта, что в некоторых случаях
    упрощает чтение."""

    def __init__(self, **context_kwargs):
        self._context = context_kwargs

    def __getattr__(self, item: str):
        if item in self._context:
            return self._context[item]

        raise AttributeError(item)
