from shield import (
    Resolver,
    Rule,
    TContextProtocol,
    one_call_per_context_cache_decorator,
)


# Определяем класс заглушку, для реализации некоторой сущности
class Article:
    def __init__(self, author: str, deleted: bool):
        self.author = author
        self.deleted = deleted


# Определяем пользовательский класс для управления контекстом
class CustomContextProvider(TContextProtocol):
    def __init__(self, username: str, is_staff: bool, is_superuser: bool):
        self.username = username
        self.is_staff = is_staff
        self.is_superuser = is_superuser


# Определяем правила, которые не зависят от конкретной сущности и могут быть
# использованы в других частях приложения
is_staff_or_superuser = Rule(
    lambda _, context: (
        context.is_staff or context.is_superuser
    ),
)


# Определяем какую-то тяжелую функцию которая должна выполняться только один
# раз в рамках одного контекста, например функция получения информации о
# доступных объектах. Такая функция может отправлять запросы к базе данных и
# в то же время, использоваться в разных функция-правилах. Мы используем
# декоратор one_call_per_context_cache_decorator, который позволяет сохранить
# результат выполнения функции на уровне контекста и предотвратит повторный
# вызов тяжелой функции.
@one_call_per_context_cache_decorator
def very_heavy_function_to_check_access(
    instance: Article,
    context: CustomContextProvider,
) -> bool:
    return True

# При описании класс SimpleResolver используем указание на то,
# какой тип объектов будет передан в качестве instance. Это позволит
# использовать подсказки в IDE и автоматическую проверку типов.
class SimpleResolver(Resolver[Article]):
    context_class = CustomContextProvider

    def define_rules(self):
        has_access_to_article = Rule(very_heavy_function_to_check_access)
        is_author = Rule(
            lambda instance, context: instance.author == context.username,
        )
        is_not_deleted = Rule(lambda instance, _: not instance.deleted)

        return {
            "article.read": is_not_deleted and has_access_to_article,
            "article.change": is_not_deleted and is_author,
            "article.delete": (
                is_not_deleted and (
                    is_author or is_staff_or_superuser
                )
            ),
        }


article = Article(author="p.gubarev", deleted=False)

resolver = SimpleResolver()

# При установке контекста можно передать как уже созданный объект контекста,
# так и просто набор keyword-аргументов, которые автоматически будут переданы
# в конструктор класса, заданный свойством context_class
resolver.set_context(instance=article, username="tester", is_staff=True,
                     is_superuser=False)

# Проверка доступа. Проверка не будет пройдена, так как статья уже удалена
resolver.has_permission("article.delete")  # False
