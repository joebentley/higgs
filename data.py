#!/usr/bin/env python3

import sys, math

class FourMomentum:
    """ 4-momentum class with the z-component (momentum[2]) assumed to
        be aligned with the beam axis.

        Attributes:
        self.momentum = [p_x, p_y, p_z] -- 3 item list of momentum components
        self.energy                     -- energy """

    def __init__(self, momentum=None, energy=0):
        self.momentum = momentum or []
        self.energy = energy


    def __add__(self, other):
        """ Returns the addition of 2 4-vectors. """
        E3 = self.energy + other.energy
        p3 = []
        for i in range(0, 3):
            p3.append(self.momentum[i] + other.momentum[i])
        p = FourMomentum(p3, E3)
        return p

    __radd__ = __add__

    def __mul__(self, other):
        """ Returns the dot product between 2 4-vectors (in Minkowski
            geometry, signature (+, -, -,-)). """
        res = 0
        g = [1, 1, 1, -1]
        for i in range(0, 3):
            res += self.momentum[i] * other.momentum[i]
        res -= self.energy * other.energy
        return -res

    __rmul__ = __mul__

    def transverse(self):
        """ Return the transverse momentum of a 4-momentum, calculated
            from the x and y components of the 4-momentum. """
        p_T2 = self.momentum[0]**2 + self.momentum[1]**2
        return math.sqrt(p_T2)

    def eta(self):
        """ Return the pseudorapidity of the 4-vector. """
        sinheta = self.momentum[2]/self.transverse()
        return math.asinh(sinheta)

    def azimuthal(self):
        """ Return the azimuthal angle of the 4-vector. """
        pass

    @staticmethod
    def from_line(line):
        """ Parse line of format "p_x p_y p_z E" into FourMomentum object. """
        line = line.split()
        momentum = [float(line[0]), float(line[1]), float(line[2])]
        energy = float(line[3])
        return FourMomentum(momentum, energy)



class Event:
    def __init__(self, id=0, momenta=None):
        self.id = id
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
            until another event is found. """

        event = Event()

        # Our list of momenta for this event
        momenta = []

        # Start looping through the rest of the lines
        for line_num, momentum_line in enumerate(rest_of_file):
            # If the line starts with Event and we aren't on line 1, stop parsing
            if momentum_line.startswith('Event'):
                if line_num == 0:
                    event.id = momentum_line.split()[1]
                    continue
                else:
                    break

            # Ignore empty lines
            if len(momentum_line.strip()) == 0:
                continue

            momenta.append(FourMomentum.from_line(momentum_line))

        event.momenta = momenta
        return event



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

#Energy filter
def energy_threshold(events, E):
    for event in events:
        event.momenta = list(filter(lambda x: x.energy > E, event.momenta))
    return events

def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'Signal10Events.txt'

    events = []

    with open(filepath) as data_file:
        raw = data_file.read().split('\n')

        for i, line in enumerate(raw):
            # If the line starts with 'Event', begin to process it
            if line.startswith('Event'):
                events.append(Event.from_text(raw[i:]))

    #Filtering events
    events = energy_threshold(events, 40)
    #More than 2
    events = number_threshold(events, 1)
    #One photon with transverse momentum > 20GeV
    events = transverse_threshold(events, 20)
    #The other photon with p_T >40GeV
    events = transverse_threshold(events, 40)

    # only show events with at least 1 momenta
    events = number_threshold(events, 0)

    #Prints out events + invariant mass of system
    for event in events:
        a = FourMomentum([0,0,0], 0)
        print('Event', event.id)
        for momenta in event.momenta:
            a += momenta
            print('Energy:', momenta.energy)
            print('p_T:', momenta.transverse())
        b = a * a
        b = math.sqrt(b)
        print('Invariant mass:', b)


if __name__ == '__main__':
    main()


