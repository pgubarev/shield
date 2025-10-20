from shield.resolvers import Resolver
from shield.rules import Rule
from shield.type_annotations import TDefinedRules


class FakeResolver(Resolver[str]):
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


resolver = FakeResolver()
resolver.set_context(instance="some", read_operations_allowed=True)

aa = resolver.instance

## print(aa)
