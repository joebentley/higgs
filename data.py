#!/usr/bin/env python

import sys

class FourMomentum:
    def __init__(self, momentum=None, energy=0):
        self.momentum = momentum or []
        self.energy = energy

    #Define addition of 2 4-vectors, replaces + with this function.
    def __add__(self, other):
        E3 = self.energy + other.energy
        p3 = []
        for i in range(0, 2):
            p3.append(self.momentum[i] + other.momentum[i])
        p = FourMomentum(p3, E3)
        return p

    __radd__ = __add__

    #Dot product between 2 4-vectors (in Minkowski geometry, signature (+, -, -,-) )
    #p_1 and p_2 are FourMomentum objects replaces *
    def __mul__(self, other):
        res = 0
        g = [1, 1, 1, -1]
        for i in range(0, 3):
            res += self.momentum[i] * other.momentum[i] 
        res -= self.energy * other.energy
        return -res
    
    __rmul__ = __mul__
    
    #@staticmethod
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
            until another event is found. """
        # Our list of momenta for this event
        momenta = []

        # Start looping through the rest of the lines
        for momentum_line in rest_of_file:
            # If the line starts with Event, stop parsing
            if momentum_line.startswith('Event'):
                break

            # Ignore empty lines
            if len(momentum_line.strip()) == 0:
                continue

            momenta.append(FourMomentum.from_line(momentum_line))

        return Event(momenta)

events = []




def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'Signal10Events.txt'

    #events = []

    with open(filepath) as data_file:
        raw = data_file.read().split('\n')

        for i, line in enumerate(raw):
            # If the line starts with 'Event', begin to process it
            if line.startswith('Event'):
                events.append(Event.from_text(raw[(i+1):]))


    # Only show events with more than 1 four momenta
    #for i, event in enumerate(filter(lambda x: len(x) > 1, events)):
        #print('Event {0}'.format(i + 1))
        #print(event)


if __name__ == '__main__':
    main()

def number_threshold(n):
    new_events=[]
    for i in range(0, len(events)):
        if len(events[i].momenta) > n:
            new_events.append(events[i])
    return new_events

def energy_threshold(E_m):
    new_events = []
    #Every event
    for i in range(0, len(events)):
        #every photon
        #set a dummy variable, reset to 0 for each event
        dum = 0
        for j in range(0, len(events[i].momenta)):
            if events[i].momenta[j].energy >= E_m:
                dum += 1
                #dummy variable increases if each photon reaches energy threshold
        #only accepts if all photons reach threshold
        if dum == len(events[i].momenta):
            new_events.append(events[i])
    return new_events


