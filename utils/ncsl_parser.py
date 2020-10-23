#!/usr/bin/env python

"""
This program generates a csv file of the dominant party in each state legislature for a given year.

As input it takes a directory of xml files generated by pdftohtml from pdfs from the NCSL website.

As output it generates a csv file with the columns being the year and rows being the states. The data
should be either "Rep", "Dem", or "Divided".
"""

from collections import defaultdict
import os
from xml.dom.minidom import parse

from state_names import state_names

class State:
    def __init__(self, name):
        self.name = name
        self.data = {}

    @property
    def header(self):
        return 'State,' + ','.join([k.split()[0] for k in sorted(self.data)])
    @property
    def to_csv(self):
        return self.name + ',' + ','.join([self.data[k] for k in sorted(self.data)])
    
class PdfDoc:
    def __init__(self, states, path):
        self.states = states
        basename = os.path.basename(path)
        self.year = os.path.splitext(basename)[0]
        self.doc_years = None
        
        self.doc = parse(path)
        self.lines = defaultdict(lambda: Line())
        if '_' in self.year:
            self.parse_years()
        else:
            self.parse_year()

    def parse_years(self):
        print('parsing years')
        for node in self.doc.getElementsByTagName('text'):
            top = int(node.getAttribute('top'))
            line = None
            if top in self.lines:
                line = self.lines[top]
            elif top - 1 in self.lines:
                line = self.lines[top - 1]
            elif top + 1 in self.lines:
                line = self.lines[top + 1]
            else:
                line = Line()
                self.lines[top] = line
            line.nodes.append(node)
            
        for line in self.lines.values():
            if line.state in self.states:
                for idx, year in enumerate(self.years):
                    party = line.node_values[idx + 1]
                    if party == 'S':
                        party = 'Split'
                    states[line.state].data[year] = party.replace('*', '')
        
    def parse_year(self):
        print('parsing year', self.year)
        for node in self.doc.getElementsByTagName('text'):
            self.lines[node.getAttribute('top')].nodes.append(node)
        for line in self.lines.values():
            if line.state in self.states:
                states[line.state].data[self.year] = line.party

    @property
    def years(self):
        if not self.doc_years:
            start_year = self.year.split('_')[0]
            for line in self.lines.values():
                if line.state == start_year:
                    self.doc_years = line.node_values
        return self.doc_years
    
class Line:
    def __init__(self):
        self.nodes = []
        self.sorted_nodes = None

    @property
    def data(self):
        if not self.sorted_nodes:
            self.sorted_nodes = sorted(self.nodes, key = lambda x: int(x.getAttribute('left')))
        return self.sorted_nodes
    
    @property
    def party(self):
        p = self.data[-3].childNodes[0].toxml().strip().replace('*', '')
        if p not in set(['Rep', 'Dem', 'Split', 'Divided',]):
            raise Exception("No such party {} in {}".format(p, self.state))
        if p == 'Divided':
            return 'Split'
        return p

    @property
    def state(self):
        return self.data[0].childNodes[0].toxml().strip().replace('*', '').replace('<b>', '').replace('</b>', '')

    @property
    def node_values(self):
        return [v.childNodes[0].toxml().replace('<b>', '').replace('</b>', '') for v in self.data]
if __name__ == '__main__':
    states = {}
    for n in state_names:
        states[n] = State(n)
    
    for fn in os.listdir('xml'):
        PdfDoc(states, 'xml/{}'.format(fn))

    for idx, state in enumerate(states.values()):
        if idx == 0:
            print(state.header)
        print(state.to_csv)
