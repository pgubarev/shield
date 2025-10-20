from shield.resolvers import Resolver
from shield.rules import Rule
from shield.type_annotations import TDefinedRules


class FakeResolver(Resolver):

    def define_rules(self) -> TDefinedRules:
        is_staff_or_superuser = Rule(
            lambda context: context.is_staff or context.is_superuser,
        )
        can_read_documentation = (
            is_staff_or_superuser |
            Rule(lambda context: context.read_operations_allowed)
        )

        return {
            "documents.read": can_read_documentation,
            "documents.create": is_staff_or_superuser,
        }

    def define_attributes(self) -> TDefinedRules:
        return {}


def test_has_permission():
    resolver = FakeResolver()
    resolver.set_context(read_operations_allowed=True, is_staff=False,
                         is_superuser=False)

    has_permission = resolver.has_permission("documents.read")
    assert has_permission

    has_permission = resolver.has_permission("documents.create")
    assert not has_permission
