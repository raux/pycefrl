#-- CLASS PROGRAM TO ITERATE ON THE TREE

import ast
import csv
import json
import levels

#-- Static type map to avoid eval() calls
TYPE_MAP = {
    'ast.List': ast.List,
    'ast.Tuple': ast.Tuple,
    'ast.Dict': ast.Dict,
    'ast.Name': ast.Name,
    'ast.Call': ast.Call,
    'ast.IfExp': ast.IfExp,
    'ast.Attribute': ast.Attribute,
    'ast.ListComp': ast.ListComp,
    'ast.GeneratorExp': ast.GeneratorExp,
    'ast.DictComp': ast.DictComp,
    'ast.Assign': ast.Assign,
    'ast.AugAssign': ast.AugAssign,
    'ast.Raise': ast.Raise,
    'ast.Assert': ast.Assert,
    'ast.Pass': ast.Pass,
    'ast.Import': ast.Import,
    'ast.ImportFrom': ast.ImportFrom,
    'ast.If': ast.If,
    'ast.For': ast.For,
    'ast.While': ast.While,
    'ast.Break': ast.Break,
    'ast.Continue': ast.Continue,
    'ast.Try': ast.Try,
    'ast.With': ast.With,
    'ast.FunctionDef': ast.FunctionDef,
    'ast.Lambda': ast.Lambda,
    'ast.Return': ast.Return,
    'ast.Yield': ast.Yield,
    'ast.ClassDef': ast.ClassDef,
}

#-- Reverse map: AST type -> attribute string (built once at import time)
REVERSE_TYPE_MAP = {v: k for k, v in TYPE_MAP.items()}


class IterTree():
    """ Class to iterate tree. """

    def __init__(self, tree, attrib, file, repo, abs_path=None, nodes=None):
        """ Class constructor. """
        self.tree = tree
        self.attrib = attrib
        self.name = file
        self.repo = repo
        self.abs_path = abs_path if abs_path else repo
        
        # Instance level storage instead of global/class level
        self.csv_rows = []
        self.json_data = {}
        
        if nodes is not None:
            self._process_nodes(nodes)
        else:
            self.locate_Tree()

    def locate_Tree(self):
        """ Method iterating on the tree. """
        target_type = TYPE_MAP.get(self.attrib)
        if target_type is None:
            return
        for self.node in ast.walk(self.tree):
            #-- Find attributes using direct type comparison
            if type(self.node) is target_type:
                self._process_single_node()

    def _process_nodes(self, nodes):
        """ Process pre-collected nodes (single-pass mode). """
        for self.node in nodes:
            self._process_single_node()

    def _process_single_node(self):
        """ Process a single matching node. """
        self.level = ''
        self.clase = ''
        levels.levels(self)
        self.assign_List()
        self.assign_Dict()

    def assign_List(self):
        """ Create object list. """
        if (self.clase != '') and (self.level != ''):
            self.list = [self.repo, self.abs_path, self.name, self.clase, self.node.lineno,
                        self.node.end_lineno, self.node.col_offset, self.level]
            # Accumulate instead of writing immediately
            self.csv_rows.append(self.list)

    def assign_Dict(self):
        """ Create object dictionary. """
        if (self.clase != '') and (self.level != ''):
            if not self.repo in self.json_data:
                self.json_data[self.repo] = {}

            if not self.name in self.json_data[self.repo]:
                self.json_data[self.repo][self.name] = []

            self.json_data[self.repo][self.name].append({
                'Class'       : str(self.clase),
                'Start Line'  : str(self.node.lineno),
                'End Line'    : str(self.node.end_lineno),
                'Displacement': str(self.node.col_offset),
                'Level'       : str(self.level)})

    def get_results(self):
        """ Return collected data """
        return self.csv_rows, self.json_data
