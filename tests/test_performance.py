import unittest
import ast
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ClassIterTree import IterTree, TYPE_MAP, REVERSE_TYPE_MAP
import levels


class MockIterTree:
    def __init__(self, node, attrib):
        self.node = node
        self.attrib = attrib
        self.level = ''
        self.clase = ''


class TestTypeMap(unittest.TestCase):
    """Tests for the TYPE_MAP that replaces eval() calls."""

    def test_type_map_contains_all_ast_types(self):
        """TYPE_MAP should contain entries for all used AST node types."""
        expected_types = [
            'ast.List', 'ast.Tuple', 'ast.Dict', 'ast.Name',
            'ast.Call', 'ast.IfExp', 'ast.Attribute',
            'ast.ListComp', 'ast.GeneratorExp', 'ast.DictComp',
            'ast.Assign', 'ast.AugAssign', 'ast.Raise', 'ast.Assert', 'ast.Pass',
            'ast.Import', 'ast.ImportFrom',
            'ast.If', 'ast.For', 'ast.While', 'ast.Break', 'ast.Continue',
            'ast.Try', 'ast.With',
            'ast.FunctionDef', 'ast.Lambda', 'ast.Return', 'ast.Yield',
            'ast.ClassDef',
        ]
        for type_str in expected_types:
            self.assertIn(type_str, TYPE_MAP, f"{type_str} missing from TYPE_MAP")

    def test_type_map_values_are_ast_types(self):
        """TYPE_MAP values should be actual AST node classes."""
        for key, value in TYPE_MAP.items():
            self.assertTrue(
                isinstance(value, type) and issubclass(value, ast.AST),
                f"TYPE_MAP['{key}'] = {value} is not an AST type"
            )

    def test_reverse_type_map_consistency(self):
        """REVERSE_TYPE_MAP should be the inverse of TYPE_MAP."""
        for key, value in TYPE_MAP.items():
            self.assertIn(value, REVERSE_TYPE_MAP)
            self.assertEqual(REVERSE_TYPE_MAP[value], key)

    def test_type_map_matches_eval(self):
        """TYPE_MAP lookup should produce same result as eval() for each key."""
        for key, expected_type in TYPE_MAP.items():
            self.assertIs(expected_type, eval(key))


class TestSinglePassTraversal(unittest.TestCase):
    """Tests that single-pass traversal produces the same results as multi-pass."""

    def _get_results_single_pass(self, code, repo='test_repo', file='test.py'):
        """Process code using single-pass mode (pre-collected nodes)."""
        tree = ast.parse(code)

        # Collect all attribute strings
        from pycerfl import SetClass
        all_attribs = set()
        for group in SetClass:
            for attrib in group:
                all_attribs.add(attrib)

        # Single walk to collect nodes
        nodes_by_attrib = {}
        for node in ast.walk(tree):
            node_type = type(node)
            if node_type in REVERSE_TYPE_MAP:
                attrib_str = REVERSE_TYPE_MAP[node_type]
                if attrib_str in all_attribs:
                    if attrib_str not in nodes_by_attrib:
                        nodes_by_attrib[attrib_str] = []
                    nodes_by_attrib[attrib_str].append(node)

        all_csv = []
        all_json = {}
        for group in SetClass:
            for attrib in group:
                nodes = nodes_by_attrib.get(attrib)
                if nodes:
                    obj = IterTree(tree, attrib, file, repo, nodes=nodes)
                    csv_rows, json_data = obj.get_results()
                    all_csv.extend(csv_rows)
                    for rk, files in json_data.items():
                        if rk not in all_json:
                            all_json[rk] = {}
                        for fk, dl in files.items():
                            if fk not in all_json[rk]:
                                all_json[rk][fk] = []
                            all_json[rk][fk].extend(dl)
        return all_csv, all_json

    def _get_results_multi_pass(self, code, repo='test_repo', file='test.py'):
        """Process code using legacy multi-pass mode (one walk per attribute)."""
        tree = ast.parse(code)

        from pycerfl import SetClass
        all_csv = []
        all_json = {}
        for group in SetClass:
            for attrib in group:
                obj = IterTree(tree, attrib, file, repo)
                csv_rows, json_data = obj.get_results()
                all_csv.extend(csv_rows)
                for rk, files in json_data.items():
                    if rk not in all_json:
                        all_json[rk] = {}
                    for fk, dl in files.items():
                        if fk not in all_json[rk]:
                            all_json[rk][fk] = []
                        all_json[rk][fk].extend(dl)
        return all_csv, all_json

    def test_single_pass_matches_multi_pass_simple(self):
        """Single-pass should produce same results as multi-pass for simple code."""
        code = """
x = [1, 2, 3]
y = {'a': 1}
for i in range(10):
    print(i)
"""
        single_csv, single_json = self._get_results_single_pass(code)
        multi_csv, multi_json = self._get_results_multi_pass(code)

        self.assertEqual(len(single_csv), len(multi_csv))
        self.assertEqual(single_json, multi_json)

    def test_single_pass_matches_multi_pass_complex(self):
        """Single-pass should produce same results as multi-pass for complex code."""
        code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

class MyClass:
    def __init__(self):
        self.data = [1, 2, 3]

    def process(self):
        return [x * 2 for x in self.data]

try:
    result = fibonacci(10)
except Exception:
    pass
"""
        single_csv, single_json = self._get_results_single_pass(code)
        multi_csv, multi_json = self._get_results_multi_pass(code)

        self.assertEqual(len(single_csv), len(multi_csv))
        self.assertEqual(single_json, multi_json)

    def test_pre_collected_nodes_mode(self):
        """IterTree should work when receiving pre-collected nodes."""
        code = "[1, 2, 3]"
        tree = ast.parse(code)

        # Collect nodes manually
        list_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.List)]
        self.assertTrue(len(list_nodes) > 0)

        obj = IterTree(tree, 'ast.List', 'test.py', 'test_repo', nodes=list_nodes)
        csv_rows, json_data = obj.get_results()

        self.assertTrue(len(csv_rows) > 0)
        self.assertEqual(csv_rows[0][6], 'A1')  # Level should be A1 for simple list


class TestIsinstanceChecks(unittest.TestCase):
    """Tests that isinstance-based checks work correctly."""

    def test_list_with_nested_list(self):
        """isinstance check should detect nested lists correctly."""
        code = "[[1, 2], [3, 4]]"
        tree = ast.parse(code)
        list_node = tree.body[0].value

        mock = MockIterTree(list_node, 'ast.List')
        levels.level_List(mock)

        self.assertEqual(mock.level, 'A2')
        self.assertIn('Nested List', mock.clase)

    def test_list_with_dict(self):
        """isinstance check should detect dicts inside lists."""
        code = "[{'a': 1}, {'b': 2}]"
        tree = ast.parse(code)
        list_node = tree.body[0].value

        mock = MockIterTree(list_node, 'ast.List')
        levels.level_List(mock)

        self.assertEqual(mock.level, 'B1')
        self.assertIn('Dictionary List', mock.clase)

    def test_for_nested_isinstance(self):
        """isinstance check should detect nested for loops."""
        code = "for i in range(10):\n    for j in range(5): pass"
        tree = ast.parse(code)
        for_node = tree.body[0]

        mock = MockIterTree(for_node, 'ast.For')
        levels.type_ElemLoop(mock)

        self.assertEqual(mock.level, 'A2')
        self.assertIn('Nested For Loop', mock.clase)

    def test_assign_with_binop_isinstance(self):
        """isinstance check should detect BinOp in assignments."""
        code = "total = total + 1"
        tree = ast.parse(code)
        assign_node = tree.body[0]

        mock = MockIterTree(assign_node, 'ast.Assign')
        levels.level_Assign(mock)

        self.assertIn('sum', mock.clase)

    def test_augassign_add_isinstance(self):
        """isinstance check should detect Add operator in augmented assignments."""
        code = "x += 1"
        tree = ast.parse(code)
        assign_node = tree.body[0]

        mock = MockIterTree(assign_node, 'ast.AugAssign')
        levels.level_Assign(mock)

        self.assertIn('increase amount', mock.clase)

    def test_try_nested_isinstance(self):
        """isinstance check should detect nested try statements."""
        code = "try:\n    try: pass\n    except: pass\nexcept: pass"
        tree = ast.parse(code)
        try_node = tree.body[0]

        mock = MockIterTree(try_node, 'ast.Try')
        levels.level_Try(mock)

        self.assertIn('/try', mock.clase)

    def test_recursive_function_isinstance(self):
        """isinstance check should detect recursive function calls."""
        code = "def factorial(n):\n    if n <= 1: return 1\n    return factorial(n-1) * n"
        tree = ast.parse(code)
        func_node = tree.body[0]

        mock = MockIterTree(func_node, 'ast.FunctionDef')
        levels.level_FunctionDef(mock)

        self.assertIn('Recursive', mock.clase)


if __name__ == '__main__':
    unittest.main()
