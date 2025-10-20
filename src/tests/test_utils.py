from unittest.mock import Mock

from shield.context import DictContext
from shield.utils import one_call_per_context_cache_decorator


def test_one_call_per_context_cache_decorator():
    stub_function = Mock(return_value=10)
    stub_function.__name__ = "stub_function"

    decorated_function = one_call_per_context_cache_decorator(stub_function)

    context = DictContext()
    decorated_function(context)
    assert stub_function.call_count == 1

    decorated_function(context)
    assert stub_function.call_count == 1

    context = DictContext()
    decorated_function(context)
    assert stub_function.call_count == 2

    decorated_function(context)
    assert stub_function.call_count == 2
