#!/usr/bin/env python3

from math import sqrt
import parse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def statistical_significance(signal, background):
    """ Calculate statistical significance given num. signal events
        and num. background events. """
    return signal / sqrt(signal + background)

def main():
    parser = argparse.ArgumentParser(description="""Generate 2D histogram of
                        statistical significance of various filters.""")
    parser.add_argument('--back', action='store_false',
                        help="Don't use the background.")

    args = parser.parse_args()

    # Get all the events
    higgs_events = parse.parse_file('higgs.txt', momenta_in_event=True)
    filtered_higgs = {}

    if args.back:
        bkg_events = parse.parse_file('background.txt', momenta_in_event=True)
        filtered_bkg = {}

    # Apply a series of different filters in turn
    lower_momentum = range(4, 10, 2)

    for lower in lower_momentum:
        for higher in range(50, 70, 5):
            filtered_higgs[(lower, higher)] = parse.combined_filter(higgs_events,
                    num=1, momentum_lower=lower,
                    momentum_higher=higher, energy=20)
            if args.back:
                filtered_bkg[(lower, higher)] = parse.combined_filter(bkg_events,
                        num=1, momentum_lower=lower,
                        momentum_higher=higher, energy=20)

    # Higgs and background should have same keys
    keys = filtered_higgs.keys()

    bins = []
    for key in keys:
        if args.back:
            bins.append(statistical_significance(len(filtered_higgs[key]),
                                                 len(filtered_bkg[key])))
        else:
            bins.append(statistical_significance(len(filtered_higgs[key]), 0))

    x = []
    y = []
    for k in keys:
        x.append(k[0])
        y.append(k[1])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, bins)

    plt.show()

if __name__ == '__main__':
    main()
