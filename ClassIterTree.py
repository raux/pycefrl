#-- CLASS PROGRAM TO ITERATE ON THE TREE

import ast
import csv
import json
import levels


class IterTree():
    """ Class to iterate tree. """

    def __init__(self, tree, attrib, file, repo):
        """ Class constructor. """
        self.tree = tree
        self.attrib = attrib
        self.name = file
        self.repo = repo
        
        # Instance level storage instead of global/class level
        self.csv_rows = []
        self.json_data = {}
        
        self.locate_Tree()

    def locate_Tree(self):
        """ Method iterating on the tree. """
        for self.node in ast.walk(self.tree):
            #-- Find attributes
            if type(self.node) == eval(self.attrib):
                self.level = ''
                self.clase = ''
                levels.levels(self)
                self.assign_List()
                self.assign_Dict()

    def assign_List(self):
        """ Create object list. """
        if (self.clase != '') and (self.level != ''):
            self.list = [self.repo, self.name, self.clase, self.node.lineno,
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
