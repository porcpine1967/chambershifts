#!/usr/bin/env python

""" Outputs graphs of shifts in legislative dominance over time. """

from collections import Counter
import csv

import matplotlib.pyplot as plt

from state_names import southern_states


class Year:
    """ Bean for holding year information """

    def __init__(self, year):
        self.year = year
        self.data = Counter()
        self.southern_data = Counter()


class StateLegislatureManager:
    """ Parses and plots state legislature data """

    def __init__(self, path):
        self.parse_file(path)

    def parse_file(self, path):
        """ Builds data from information in file from path """
        self.years = []
        with open(path) as open_file:
            reader = csv.reader(open_file)
            for idx, row in enumerate(reader):
                if idx == 0:
                    for year_name in row[1:]:
                        self.years.append(Year(year_name))
                    continue
                for idx, party in enumerate(row[1:]):
                    self.years[idx].data[party] += 1
                    if row[0] in southern_states:
                        self.years[idx].southern_data[party] += 1

    def graph(self):
        """ Generates matplotlib graphs """
        years = []
        reps = []
        dems = []
        splits = []
        southern_reps = []
        southern_dems = []
        southern_splits = []
        for year in self.years:
            years.append(year.year)
            reps.append(year.data["Rep"])
            dems.append(year.data["Dem"])
            splits.append(year.data["Split"])
            southern_reps.append(year.southern_data["Rep"])
            southern_dems.append(year.southern_data["Dem"])
            southern_splits.append(year.southern_data["Split"])
            print(year.year, year.data)
        plt.plot(years, reps, "r")
        plt.plot(years, dems, "b")
        plt.plot(years, splits, "y")
        plt.plot(years, southern_reps, "r")
        plt.plot(years, southern_dems, "b")
        plt.plot(years, southern_splits, "y")

        plt.show()


def run():
    manager = StateLegislatureManager("data/state_legislatures.csv")
    manager.graph()


if __name__ == "__main__":
    run()
