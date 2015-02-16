#!/usr/bin/env python3

from math import sqrt
import parse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def statistical_significance(signal, background):
    """ Calculate statistical significance given num. signal events
        and num. background events. """
    if signal == 0:
        return 0
    else:
        return signal / sqrt(signal + background)

def main():
    parser = argparse.ArgumentParser(description="""Generate 2D histogram of
                        statistical significance of various filters.""")
    parser.add_argument('--back', action='store_false',
                        help="Don't use the background.")
    parser.add_argument('--transverse', action='store_true', help='transverse cuts')
    parser.add_argument('--energy', action = 'store_true', help = 'energy cuts')
    parser.add_argument('--etaphi', action = 'store_true', help = 'cuts both azimuthal and psudeorapidity difference squared')
    parser.add_argument('range2D', metavar = 'range2D', type = int, nargs = '+', 
                       help = 'choose x-axis for plot, xmin xmax step ymin ymax step')

    args = parser.parse_args()
    xlabel = ''
    ylabel = ''
    title = ''
    xrange = args.range2D[0:3]
    if len(xrange)<3:
        xrange = [0, 100, 20]
    yrange = args.range2D[3:len(args.range2D)]
    if len(yrange) < 3:
        yrange = [0, 100, 20]
    # Get all the events
    higgs_events = parse.parse_file('higgs.txt', momenta_in_event=True)
    filtered_higgs = {}

    if args.back:
        bkg_events = parse.parse_file('background.txt', momenta_in_event=True)
        filtered_bkg = {}
    
    if args.transverse:
    # Apply a series of different filters in turn
        lower_momentum = range(xrange[0], xrange[1], xrange[2])
        higher_momentum = range(yrange[0], yrange[1], yrange[2])
        xlabel = '$p_{T1}$'
        ylabel = '$p_{T2}$'
        title = 'transverse momenta'
        for lower in lower_momentum:
            for higher in higher_momentum:
                filtered_higgs[(lower, higher)] = parse.combined_filter(higgs_events,
                                                                        num=1, momentum_lower=lower,
                                                                        momentum_higher=higher, energy_lower=0,
                                                                        energy_higher = 0, deta = 0, dazi = 0)
                if args.back:
                    filtered_bkg[(lower, higher)] = parse.combined_filter(bkg_events,
                                                                          num=1, momentum_lower=lower,
                                                                          momentum_higher=higher, energy_lower=0,
                                                                          energy_higher = 0, deta = 0, dazi = 0)

    if args.energy:
        lower_energy = range(xrange[0], xrange[1], xrange[2])
        higher_energy = range(yrange[0], yrange[1], yrange[2])
        xlabel = '$E_1$'
        ylabel = '$E_2$'
        title = 'Energy'
        for lower in lower_energy:
            for higher in higher_energy:
                filtered_higgs[(lower, higher)] = parse.combined_filter(higgs_events, 
                                                                        num = 1, momentum_lower = 0,
                                                                        momentum_higher = 0, energy_lower = lower,
                                                                        energy_higher = higher, deta = 0, dazi = 0)
                if args.back:
                    filtered_bkg[(lower, higher)] = parse.combined_filter(bkg_events, 
                                                                          num = 1, momentum_lower = 0,
                                                                          momentum_higher = 0, energy_lower = lower,
                                                                          energy_higher = higher, deta = 0, dazi = 0)
    if args.etaphi:
        eta = range(xrange[0], xrange[1], xrange[2])
        phi = range(yrange[0], yrange[1], yrange[2])
        ylabel = '$d\eta^2$'
        xlabel = '$d\phi^2$'
        title = 'azimuthal angle, and pseudorapidity'
        for az in phi:
            for rap in eta:
                filtered_higgs[(az, rap)] = parse.combined_filter(higgs_events,
                                                                        num = 1, momentum_lower = 0,
                                                                        momentum_higher = 0, energy_lower = 0,
                                                                        energy_higher = 0, deta = rap, dazi = az)
                
                if args.back:
                    filtered_bkg[(az, rap)] = parse.combined_filter(bkg_events, 
                                                                     num = 1, momentum_lower = 0, 
                                                                     momentum_higher = 0, energy_lower = 0,
                                                                     energy_higher = 0, deta = rap, dazi = az)
                                                                 
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
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(x, y, bins)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title('Optimisation plot for ' + title + ' cuts.')
    plt.show()

if __name__ == '__main__':
    main()
