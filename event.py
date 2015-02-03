from fourmomentum import FourMomentum
from math import *

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

    def filter_highest(self, n):
        """ Only use n highest tranverse momentum. """
        self.momenta = sorted(self.momenta, key=lambda x: x.transverse())[:2]

    def filter_2_angles(self):
        #get all the angles
        diff = []
        for i in range(0, len(self.momenta)):
            for j in range(0, len(self.momenta)):
                #don't need same ones
                if i < j:
                    #will be a small(ish) list
                    diff.append(abs(self.momenta[i].azimuthal() - self.momenta[j].azimuthal()))


        table = [[0, 1],[0, 2],[1,2],[0,3],[1,3],[2,3],[0,4], [1,4], [2,4],[3,4],[0,5],[1,5],[2,5], [3,5], [4,5], [0,6],[1,6],[2,6],[3,6]]
        smallest = sorted(diff)[0]
        print(diff.index(smallest))
        ind = table[diff.index(smallest)]
        momenta = []
        for i in ind:
            momenta.append(self.momenta[i])
        self.momenta = momenta

    def invariant_mass(self):
        """ Calculate the invariant mass from the four momenta. """
        a = FourMomentum([0,0,0], 0)
        for momenta in self.momenta:
            a += momenta
        b = a * a
        return sqrt(abs(b))

    @staticmethod
    def from_text(four_momenta_lines):
        """ Generate Event from looking through the string given
            and turning each line of the string into a four momenta. """

        event = Event()

        # Our list of momenta for this event
        momenta = []

        # Start looping through the rest of the lines
        for momentum_line in four_momenta_lines:
            # Ignore empty lines
            if len(momentum_line.strip()) == 0:
                continue

            momenta.append(FourMomentum.from_line(momentum_line))

        event.momenta = momenta
        return event


