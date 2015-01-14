#!/usr/bin/env python

import sys

class FourMomentum:
    def __init__(self, momentum=None, energy=0):
        self.momentum = momentum or []
        self.energy = energy

    @staticmethod
    def from_line(line):
        """ Parse line of format "p_x p_y p_z E" into FourMomentum object. """
        line = line.split()
        momentum = [float(line[0]), float(line[1]), float(line[2])]
        energy = float(line[3])
        return FourMomentum(momentum, energy)

class Event:
    def __init__(self, momenta=None):
        self.momenta = momenta or []

    def __str__(self):
        string = ''
        for m in self.momenta:
            string += '{0[0]} {0[1]} {0[2]} {1}\n'.format(m.momentum, m.energy)
        return string

    def __len__(self):
        return len(self.momenta)

    @staticmethod
    def from_text(rest_of_file):
        """ Generate Event from looking through the rest of the file
            and constructing the momenta. """
        # Our list of momenta for this event
        momenta = []

        # Start looping through the rest of the lines
        for momentum_line in rest_of_file:
            # If the line starts with Event, or is empty, don't parse
            if momentum_line.startswith('Event') or momentum_line == '':
                break

            momenta.append(FourMomentum.from_line(momentum_line))

        return Event(momenta)


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'testdata'

    events = []

    with open(filepath) as data_file:
        raw = data_file.read().split('\n')

        for i, line in enumerate(raw):
            # If the line starts with 'Event', begin to process it
            if line.startswith('Event'):
                events.append(Event.from_text(raw[(i+1):]))


    # Only show events with more than 1 four momenta
    for i, event in enumerate(filter(lambda x: len(x) > 1, events)):
        print 'Event {0}'.format(i + 1)
        print event


if __name__ == '__main__':
    main()

