from pytest import raises

from shield.context import DictContext


def test_dict_context():
    context = DictContext(some=123, another="value")

    assert context.some == 123
    assert context.another == "value"

    with raises(AttributeError):
        _ = context.invalid
