#!/usr/bin/env python3

import sys
import io
import os
import json
from IPython.nbformat.current import read, write

class StripOutput():
    def remove_outputs(nb):
        """remove the outputs from a notebook"""
        for ws in nb.worksheets:
            for cell in ws.cells:
                if cell.cell_type == 'code':
                    cell.outputs = []
    
    def check_outputs(nb):
        for ws in nb.worksheets:
            for cell in ws.cells:
                if cell.cell_type == 'code':
                    if cell.outputs != []:
                        raise Exception("Notebooks contain output. Run make clear_output from the root directory to resolve this.")
        

    def check_notebooks_for_outputs(self, path):
        for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(".ipynb"):
                            file = os.path.join(root, file)
                            with io.open(file, 'r') as f:
                                try:
                                    nb = read(f, 'json')
                                except:
                                    print("%s is broken" % file)
                                    continue
                            self.check_outputs(nb)

    def process_notebooks(self, path):
        print(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".ipynb"):
                    file = os.path.join(root, file)
                    print(file)
                    with io.open(file, 'r') as f:
                        try:
                            nb = read(f, 'json')
                        except:
                            print("%s is broken" % file)
                            continue
                    self.remove_outputs(nb)
                    with io.open(file, 'w', encoding='utf8') as f:
                        write(nb, f, 'json')
                    print("wrote %s" % file)
    