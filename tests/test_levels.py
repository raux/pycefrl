import unittest
import ast
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import levels

class MockIterTree:
    def __init__(self, node, attrib):
        self.node = node
        self.attrib = attrib
        self.level = ''
        self.clase = ''

class TestLevels(unittest.TestCase):
    def test_list_simple(self):
        code = "[1, 2, 3]"
        tree = ast.parse(code)
        # Find the List node: Module -> Expr -> List
        list_node = tree.body[0].value
        
        mock = MockIterTree(list_node, 'ast.List')
        levels.level_List(mock)
        
        self.assertEqual(mock.level, 'A1')
        self.assertIn('Simple List', mock.clase)

    def test_list_nested(self):
        code = "[[1, 2], [3, 4]]"
        tree = ast.parse(code)
        list_node = tree.body[0].value
        
        mock = MockIterTree(list_node, 'ast.List')
        levels.level_List(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertIn('Nested List', mock.clase)

    def test_if_simple(self):
        code = "if True: pass"
        tree = ast.parse(code)
        if_node = tree.body[0]
        
        mock = MockIterTree(if_node, 'ast.If')
        levels.level_If(mock)
        
        self.assertEqual(mock.level, 'A1')
        self.assertIn('Simple If statements', mock.clase)

    def test_if_expression(self):
        code = "x = 1 if True else 2"
        tree = ast.parse(code)
        # Module -> Assign -> IfExp
        if_exp_node = tree.body[0].value
        
        mock = MockIterTree(if_exp_node, 'ast.IfExp')
        levels.level_If(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('If statements expression', mock.clase)

    def test_function_simple(self):
        code = "def foo(): pass"
        tree = ast.parse(code)
        func_node = tree.body[0]
        
        mock = MockIterTree(func_node, 'ast.FunctionDef')
        levels.level_FunctionDef(mock)
        
        self.assertEqual(mock.level, 'A1')
        self.assertEqual(mock.clase, 'Function')

    def test_function_args_default(self):
        code = "def foo(a=1): pass"
        tree = ast.parse(code)
        func_node = tree.body[0]
        
        mock = MockIterTree(func_node, 'ast.FunctionDef')
        levels.level_FunctionDef(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertIn('with Default argument', mock.clase)

    def test_function_args_vararg(self):
        code = "def foo(*args): pass"
        tree = ast.parse(code)
        func_node = tree.body[0]
        
        mock = MockIterTree(func_node, 'ast.FunctionDef')
        levels.level_FunctionDef(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('with * argument', mock.clase)

    def test_class_simple(self):
        code = "class A: pass"
        tree = ast.parse(code)
        class_node = tree.body[0]
        
        mock = MockIterTree(class_node, 'ast.ClassDef')
        levels.level_Class(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('Simple Class', mock.clase)

    def test_class_inherited(self):
        code = "class A(B): pass"
        tree = ast.parse(code)
        class_node = tree.body[0]
        
        mock = MockIterTree(class_node, 'ast.ClassDef')
        levels.level_Class(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('Inherited Class', mock.clase)

    def test_list_comp_simple(self):
        code = "[x for x in range(10)]"
        tree = ast.parse(code)
        # Module -> Expr -> ListComp
        comp_node = tree.body[0].value
        
        mock = MockIterTree(comp_node, 'ast.ListComp')
        levels.level_ListComp(mock)
        
        self.assertEqual(mock.level, 'C1')
        self.assertIn('Simple List Comprehension', mock.clase)

    def test_dict_simple(self):
        code = "{'a': 1}"
        tree = ast.parse(code)
        dict_node = tree.body[0].value
        
        mock = MockIterTree(dict_node, 'ast.Dict')
        levels.level_Dict(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertIn('Simple Dictionary', mock.clase)

    def test_while_simple(self):
        code = "while True: pass"
        tree = ast.parse(code)
        while_node = tree.body[0]
        
        mock = MockIterTree(while_node, 'ast.While')
        levels.type_ElemLoop(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('Simple While Loop', mock.clase)

    def test_while_else(self):
        code = "while True: pass\nelse: pass"
        tree = ast.parse(code)
        while_node = tree.body[0]
        
        mock = MockIterTree(while_node, 'ast.While')
        levels.type_ElemLoop(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('While with Else Loop', mock.clase)

    def test_list_false_positive_string(self):
        # A list containing a string that looks like an AST node type
        code = "['ast.List']"
        tree = ast.parse(code)
        # Module -> Expr -> List
        list_node = tree.body[0].value
        
        mock = MockIterTree(list_node, 'ast.List')
        levels.level_List(mock)
        
        # Should be simple list (A1), not nested list (A2)
        self.assertEqual(mock.level, 'A1')
        self.assertIn('Simple List', mock.clase)

    def test_for_simple(self):
        code = "for i in range(10): pass"
        tree = ast.parse(code)
        for_node = tree.body[0]
        
        mock = MockIterTree(for_node, 'ast.For')
        levels.type_ElemLoop(mock)
        
        self.assertEqual(mock.level, 'A1')
        self.assertIn('Simple For Loop', mock.clase)

    def test_for_nested(self):
        code = "for i in range(10):\n    for j in range(5): pass"
        tree = ast.parse(code)
        for_node = tree.body[0]
        
        mock = MockIterTree(for_node, 'ast.For')
        levels.type_ElemLoop(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertIn('Nested For Loop', mock.clase)

    def test_try_except(self):
        code = "try: pass\nexcept: pass"
        tree = ast.parse(code)
        try_node = tree.body[0]
        
        mock = MockIterTree(try_node, 'ast.Try')
        levels.level_Try(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('Exception --> try/except', mock.clase)

    def test_try_finally(self):
        code = "try: pass\nfinally: pass"
        tree = ast.parse(code)
        try_node = tree.body[0]
        
        mock = MockIterTree(try_node, 'ast.Try')
        levels.level_Try(mock)
        
        self.assertEqual(mock.level, 'B2')
        self.assertIn('Exception --> try/finally', mock.clase)

    def test_import_simple(self):
        code = "import os"
        tree = ast.parse(code)
        import_node = tree.body[0]
        
        mock = MockIterTree(import_node, 'ast.Import')
        levels.level_Module(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertEqual('Import', mock.clase)

    def test_from_import(self):
        code = "from os import path"
        tree = ast.parse(code)
        import_node = tree.body[0]
        
        mock = MockIterTree(import_node, 'ast.ImportFrom')
        levels.level_Module(mock)
        
        self.assertEqual(mock.level, 'A2')
        self.assertEqual('From', mock.clase)

    def test_generator_expression(self):
        code = "(x for x in range(10))"
        tree = ast.parse(code)
        gen_node = tree.body[0].value
        
        mock = MockIterTree(gen_node, 'ast.GeneratorExp')
        levels.level_GeneratorExpr(mock)
        
        self.assertEqual(mock.level, 'C1')
        self.assertIn('Generator Expression', mock.clase)

    def test_with_statement(self):
        code = "with open('file') as f: pass"
        tree = ast.parse(code)
        with_node = tree.body[0]
        
        mock = MockIterTree(with_node, 'ast.With')
        levels.level_With(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('With', mock.clase)

    def test_lambda(self):
        code = "lambda x: x+1"
        tree = ast.parse(code)
        lambda_node = tree.body[0].value
        
        mock = MockIterTree(lambda_node, 'ast.Lambda')
        levels.level_Lambda(mock)
        
        self.assertEqual(mock.level, 'B1')
        self.assertIn('Lambda', mock.clase)
