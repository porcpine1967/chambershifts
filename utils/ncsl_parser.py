#!/usr/bin/env python

"""
This program generates a csv file of the dominant party in each state
legislature for a given year.

As output it generates a csv file with the columns being the year and rows
being the states. The data should be either "Rep", "Dem", or "Split".
"""

import csv
from collections import defaultdict
import os
from xml.dom.minidom import parse

from state_names import state_names


class State:
    """ Bean for holding and formatting yearly party information."""

    def __init__(self, name):
        self.name = name
        self.data = {}

    @property
    def header(self):
        """ Headers for csv """
        return ["State"] + [k.split()[0] for k in sorted(self.data)]

    @property
    def to_csv(self):
        """ Ordered list of parties based on headers """
        return [self.name] + [self.data[k] for k in sorted(self.data)]


class PdfDoc:
    """ Parser of ncsl pdf documents."""

    def __init__(self, states, path):
        self.states = states
        basename = os.path.basename(path)
        self.year = os.path.splitext(basename)[0]
        self.doc_years = None

        self.doc = parse(path)
        self.lines = defaultdict(Line)
        if "_" in self.year:
            self.parse_years()
        else:
            self.parse_year()

    def parse_years(self):
        """ Adds party info to states for every year in the document."""
        print("parsing years {}".format(self.year))
        for node in self.doc.getElementsByTagName("text"):
            top = int(node.getAttribute("top"))
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
                    if party == "S":
                        party = "Split"
                    self.states[line.state].data[year] = party.replace("*", "")

    def parse_year(self):
        """ Adds party info to states for the year of the document."""
        print("parsing year", self.year)
        for node in self.doc.getElementsByTagName("text"):
            self.lines[node.getAttribute("top")].nodes.append(node)
        for line in self.lines.values():
            if line.state in self.states:
                self.states[line.state].data[self.year] = line.party

    @property
    def years(self):
        """ Property calculated after all the lines assigned."""
        if not self.doc_years:
            start_year = self.year.split("_")[0]
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
        """ All the nodes in the line ordered by left attribute. """
        if not self.sorted_nodes:
            self.sorted_nodes = sorted(
                self.nodes, key=lambda x: int(x.getAttribute("left"))
            )
        return self.sorted_nodes

    @property
    def party(self):
        """ Party indicated in the line.
        Only useful for single-year documents."""
        raw_party = plaintext(self.data[-3])
        if raw_party not in set(["Rep", "Dem", "Split", "Divided"]):
            msg = "No such party {} in {}".format(raw_party, self.state)
            raise Exception(msg)
        if raw_party == "Divided":
            return "Split"
        return raw_party

    @property
    def state(self):
        """ State indicated in the line."""
        return plaintext(self.data[0])

    @property
    def node_values(self):
        """ Text values of all nodes in the line. """
        return [plaintext(node) for node in self.data]


def plaintext(node):
    """ Returns text of node without tags or weirdness"""
    return (
        node.childNodes[0]
        .toxml()
        .strip()
        .replace("*", "")
        .replace("<b>", "")
        .replace("</b>", "")
    )


def run():
    """ Scoped."""
    states = {}
    for name in state_names:
        states[name] = State(name)

    for filename in os.listdir("xml"):
        PdfDoc(states, "xml/{}".format(filename))

    print("writing to file")
    with open("data/state_legislatures.csv", "w") as open_file:
        writer = csv.writer(open_file)
        for idx, state in enumerate(states.values()):
            if idx == 0:
                writer.writerow(state.header)
            writer.writerow(state.to_csv)


if __name__ == "__main__":
    run()
