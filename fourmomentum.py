from math import *

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
        return sqrt(p_T2)

    def eta(self):
        """ Return the pseudorapidity of the 4-vector. """
        sinheta = self.momentum[2]/self.transverse()
        return asinh(sinheta)

    def azimuthal(self):
        """ Return the azimuthal angle of the 4-vector. """
        tanphi = self.momentum[1]/self.momentum[0]
        return atan(tanphi)

    @staticmethod
    def from_line(line):
        """ Parse line of format "p_x p_y p_z E" into FourMomentum object. """
        line = line.split()
        momentum = [float(line[0]), float(line[1]), float(line[2])]
        energy = float(line[3])
        return FourMomentum(momentum, energy)


