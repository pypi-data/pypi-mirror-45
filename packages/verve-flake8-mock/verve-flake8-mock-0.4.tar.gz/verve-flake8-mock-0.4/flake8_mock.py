import ast


__version__ = '0.4'

# Method calls which are missing assert_ prefix
NON_EXISTENT_METHOD_CALLS = [
    'assert_calls',
    'called_once',
    'called_with',
    'called_once_with',
    'has_calls',
    'not_called',
]
# Properties which don't exist on mocks
NON_EXISTENT_ASSERTS = [
    'called_once',
    'not_called',
]

MESSAGE_M200 = "M200 {} is a non-existent mock method"
MESSAGE_M201 = "M201 {} is a non-existent mock property"


class MockChecker:
    name = 'verve-flake8-mock'
    version = __version__

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree

    def run(self):
        checks = (self.check_M200, self.check_M201)
        for node in ast.walk(self.tree):
            for check in checks:
                errors = check(node)
                if not errors:
                    continue

                for error in errors:
                    yield error

    def check_M200(self, node):
        """Check for mock functions which are not asserts.

        We want to check for functions which look like mock asserts at first
        glance, but ate not really testing anything e.g.
        some_mock.called_once() should be some_mock.assert_called_once()
        """
        if not isinstance(node, ast.Expr):
            return

        if not isinstance(node.value, ast.Call):
            return

        if not isinstance(node.value.func, ast.Attribute):
            return

        if node.value.func.attr in NON_EXISTENT_METHOD_CALLS:
            yield (
                node.lineno,
                node.col_offset,
                MESSAGE_M200.format(node.value.func.attr),
                type(self)
            )

    def check_M201(self, node):
        """Check for asserts checking attributes which don't exist.

        We want to check if there are no asserts which can look properly
        but don't actually test anything e.g.
        some_mock.assert_once - this is not a boolean attribute
        """
        if not isinstance(node, ast.Assert):
            return

        if not isinstance(node.test, ast.Attribute):
            return

        if node.test.attr in NON_EXISTENT_ASSERTS:
            yield (
                node.lineno,
                node.col_offset,
                MESSAGE_M201.format(node.test.attr),
                type(self)
            )
