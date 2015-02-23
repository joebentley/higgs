#!/usr/bin/env python3

#Take the differences between the m_yy for higgs signal and for bkg signal.
#Using lots of filters.

#Possible cuts
#a. P_T cuts
#b. E_T cuts
#c. phi cuts
#d. eta cuts


from math import sqrt

import sys, argparse
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool

from fourmomentum import FourMomentum
from event import Event

import parse


def statistical_significance(signal, background):
    """ Calculate statistical significance given num. signal events
        and num. background events. """
    return signal / sqrt(signal + background)


'''Want to have 4 2D arrays to optimize the cuts'''

def main():
    parser = argparse.ArgumentParser(description='Optimise the filter')
    parser.add_argument('--transverse', action='store_true',
                        help='Produces 2D plot for transverse momenta')
    parser.add_argument('--energy', action = 'store_true',
                        help='2D plot for energy')
    parser.add_argument('--phi', action='store_true',
                        help='2D plot for azimithal angle')
    parser.add_argument('--eta', action='store_true',
                        help='2D plot for pseudorapidity')
    parser.add_argument('--back', action='store_false',
                        help="Don't use back")

    args = parser.parse_args()

    #1. Get the raw events
    higgs_events = parse.parse_file('higgs.txt', momenta_in_event=True)
    #bkg_events = parse.parse_file('background.txt', momenta_in_event=True)
    #2 Always use the number filter
    higgs_events = parse.number_threshold(higgs_events, 1)

    if args.back:
        bkg_events = parse.number_threshold(bkg_events, 1)

    #Now optional filters
    #a. transverse momenta 2 variables, we have Nt different momenta
    if args.transverse:
        Nt = 10
        pt1 = range(0, Nt)
        pt1i, pt1f = 0, 40
        pt2 = range(0, Nt)
        pt2i, pt2f = 0, 20
        pt1 = list(map(lambda x: (pt1f - pt1i) * x/float(Nt) + pt1i, pt1))
        pt2 = list(map(lambda x: (pt2f - pt2i) * x/float(Nt) + pt2i, pt2))
        all_higgs_events = list(map(lambda x: parse.transverse_threshold(higgs_events, x), pt1))
        all_higgs_events = list(map(lambda x: parse.transverse_threshold_2(higgs_events, x), pt2))
        #all_bkg_events = list(map(lambda x: parse.transverse_threshold(bkg_events, x), pt1))
        #all_bkg_events = list(map(lambda x: parse.transverse_threshold_2(bkg_events, x), pt2))
        #2d plot variable
        x_var = pt1
        y_var = pt2

    #
    #b. Energy cuts, have Ne different energies
    if args.energy:
        Ne = 10
        E1 = range(0, Ne)
        E1i, E1f = 0, 40
        E2 = range(0, Ne)
        E2i, E2f = 0, 20
        E1 = list(map(lambda x: (E1f - E1i) * x/float(Ne) + E1i, E1))
        E2 = list(map(lambda x: (E2f - E2i) * x/float(Ne) + E2i, E2))
        all_higgs_events = list(map(lambda x: parse.energy_threshold(higgs_events, x), E1))
        all_higgs_events = list(map(lambda x: parse.energy_threshold_2(higgs_events, x), E2))

        if args.back:
            all_bkg_events = list(map(lambda x: parse.energy_threshold(bkg_events, x), E1))
            all_bkg_events = list(map(lambda x: parse.energy_threshold_2(bkg_events, x), E2))

        x_var = E1
        y_var = E2
    #
    #c.phi cuts, Np different phis
    #d. eta cuts, Nn different etas
    '''if args.eta:
        Nn = 10
        et1 = range(0, Nn)
        et1i, et1f = 0, 40
        et2 = range(0, Nn)
        et2i, et2f = 0, 20
        et1 = list(map(lambda x: (et1f - et1i) * x/float(Nt) + et1i, et1))
        et2 = list(map(lambda x: (et2f - et2i) * x/float(Nt) + et2i, et2))
        all_higgs_events = list(map(lambda x: parse.eta_threshold(higgs_events, x), et1))
        all_higgs_events = list(map(lambda x: parse.eta_threshold_2(higgs_events, x), et2))

        if args.back:
            all_bkg_events = list(map(lambda x: parse.eta_threshold(bkg_events, x), et1))
            all_bkg_events = list(map(lambda x: parse.eta_threshold_2(bkg_events, x), et2))

        x_var = et1
        y_var = et2'''

    #Invariant masses after all the filtering.
    invariant_masses_higgs = parse.get_invariant_masses(higgs_events)

    if args.back:
        invariant_masses_bkg = parse.get_invariant_masses(bkg_events)
        invariant_masses_combined = invariant_masses_higgs + invariant_masses_bkg

    # the invariant masses, pre filtering
    all_invariant_masses_higgs = list(map(lambda x: parse.get_invariant_masses(x), all_higgs_events))
    if args.back:
        all_invariant_masses_bkg = list(map(lambda x: parse.get_invariant_masses(x), all_bkg_events))

    #Plotting the data
    #Cross section data
    cs_higgs = 17.35
    bf_yy = 2.28e-3
    cs_bkg = 140
    w_higgs = cs_higgs * bf_yy
    w_bkg = cs_bkg
    z = []
    res = 3
    for i in range(0, len(all_invariant_masses_higgs)):
        invariant_masses = all_invariant_masses_higgs[i]
        bins = list(map(lambda x: x * res, range(0, int(sorted(invariant_masses)[-1]))))
        hist_higgs, bins = np.histogram(invariant_masses, bins)
        hist_higgs = list(map(lambda x: x * w_higgs, hist_higgs))
        bins = bins[0:len(bins) - 1]
        peak_guess = hist_higgs[int(120/res)]
        z.append(peak_guess)


if __name__ == '__main__':
    main()
