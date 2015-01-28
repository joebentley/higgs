#!/usr/bin/env python3

import sys, argparse
import matplotlib.pyplot as plt

from fourmomentum import FourMomentum
from event import Event


#Number filter (more than n events)
def number_threshold(events, n):
    """ Filters events so that only events with more than
        n momenta are returned. """
    return list(filter(lambda x: len(x) > n, events))

#Transverse momentum filter
def transverse_threshold(events, p_T):
    for event in events:
        event.momenta = list(filter(lambda x: x.transverse() > p_T, event.momenta))
    return events

#Keeps the 20GeV transverse momentum
def transverse_threshold_2(events, p_T):
    events2 = []
    for event in events:
        for momenta in event.momenta:
            if momenta.transverse() > p_T:
                events2.append(event)
    return events2

#Energy filter
def energy_threshold(events, E):
    for event in events:
        event.momenta = list(filter(lambda x: x.energy > E, event.momenta))
    return events

def main():
    parser = argparse.ArgumentParser(description='Generate histogram from Higgs event data')
    parser.add_argument('-f', nargs=1, default='Higgs_1e4.txt', metavar='path_to_data',
                        dest='filepath', help='Relative path to simulated data')
    parser.add_argument('--print', action='store_true',
                        help='Whether to print the calculated invariant masses to stdout.')
    parser.add_argument('--parsed', action='store_true',
                        help='Print parsing information to stdout.')
    parser.add_argument('--hist', action='store_false',
                        help="Don't show histogram")
    args = parser.parse_args()


    events = []

    with open(args.filepath) as data_file:
        raw = data_file.read().split('\n')

        for i, line in enumerate(raw):
            # If the line starts with 'Event', begin to process it
            if line.startswith('Event'):
                events.append(Event.from_text(raw[i:]))


    #Filtering events
    events = energy_threshold(events, 40)
    #One photon with transverse momentum > 20GeV
    events = transverse_threshold(events, 20)
    #The other photon with p_T >40GeV
    events = transverse_threshold_2(events, 40)

    # only show events with at least 2 momenta
    events = number_threshold(events, 1)

    for event in events:
        event.filter_highest(2)

    for event in events:
        if len(event) > 2:
            raise ValueError

    # Calculate all the invariant masses and save them
    invariant_masses = []
    for event in events:
        invariant_masses.append(event.invariant_mass())

    if args.print:
        for mass in invariant_masses:
            print(mass)

    if args.parsed:
        for event in events:
            print(event.momenta)
            print('Event', event.id)
            for momenta in event.momenta:
                print('Energy:', momenta.energy)
                print('p_T:', momenta.transverse())

            print('Invariant mass:', invariant_mass)


    if args.hist:
        weights = list(map(lambda x: 0.1, invariant_masses))

        n, bins, patches = plt.hist(invariant_masses, 1000, normed=True,
                weights=weights, facecolor='b', alpha=0.75)
        plt.xlabel('Invariant Mass (GeV/c^2)')
        plt.ylabel('Frequency')
        plt.title('Histogram of invariant masses')
        plt.axis([100, 200, 0, 0.1])
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    main()


