#!/usr/bin/env python3

from math import sqrt
from math import radians
import parse
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def get_largest(z, x, y):
    if len(z) == 0:
        return [0, 0, 0]

    z_max = max(z)
    index = z.index(z_max)
    x_max = x[index]
    y_max = y[index]
    return [x_max, y_max, z_max]

def statistical_significance(signal, background):
    """ Calculate statistical significance given num. signal events
        and num. background events. """
    cs_H = 17.35
    br_yy = 2.28e-3
    cs_bkg = 140.
    w = cs_H * br_yy/cs_bkg
    if signal == 0:
        return 0
    else:
        return signal * w / sqrt(signal * w + background)

def main():
    parser = argparse.ArgumentParser(description="""Generate 2D histogram of
                        statistical significance of various filters.""")
    parser.add_argument('--back', action='store_false',
                        help="Don't use the background.")
    parser.add_argument('--transverse', action='store_true', help='transverse cuts')
    parser.add_argument('--energy', action = 'store_true', help = 'energy cuts')
    parser.add_argument('--etaphi', action = 'store_true', help = 'cuts both azimuthal and psudeorapidity difference squared')
##    parser.add_argument('range2D', metavar = 'range2D', type = int, nargs = '+',
##                       help = 'choose x-axis for plot, xmin xmax step ymin ymax step')
    parser.add_argument('--out_opt', action = 'store_false', help = 'outputs invarant masses of optimised results')
    parser.add_argument('--plot', action = 'store_true', help = 'plots the optimisation')
    parser.add_argument('--nopreset', action = 'store_false', help = "don't use optimisation data")
    parser.add_argument('--choose_range', action = 'store_false', help = 'takes the old optimised value (from a previous run) and looks 2 parameters (at a chosen resolution)')
    args = parser.parse_args()
    xlabel = ''
    ylabel = ''
    title = ''

    xrange = [0, 100, 20]
    yrange = [0, 100, 20]



##    if not args.choose_range:
##        xrange = args.range2D[0:3]
##        if len(xrange)<3:
##            xrange = [0, 100, 20]
##        yrange = args.range2D[3:len(args.range2D)]
##        if len(yrange) < 3:
##            yrange = [0, 100, 20]
    # Get all the events
    m = 0
    higgs_events = parse.parse_file('higgs.txt', momenta_in_event=True)

    res = 0.05
    filtered_higgs = {}
    default_param = [90, 90, 0, 0, 0, 0, 113, 132]
    opt_p_T1, opt_p_T2, opt_E_1, opt_E_2, opt_dphi, opt_deta, m1, m2 = default_param

    ranges = [
            range(0, 200, 50),
            range(0, 200, 50),
            range(1, 11, 2),
            range(1, 11, 2),
            range(0, 6, 2),
            range(0, 3, 1),
         ]

    # Preset optimised values
    if args.nopreset:
        param = open('optimised.txt', 'r').read().split(',')
        param = list(map(lambda x: float(x), param))
        opt_p_T1, opt_p_T2, opt_E_1, opt_E_2, opt_dphi, opt_deta, m1, m2 = param

        # When you use an automatic range, use these parameters
        # Each range corresponds to the default ranges for each filter
        # in order: transverse momenta 1 & 2, energies 1 & 2, azimuthal, pseudorapidity
        ranges = [
                    range(60, 120, 30),
                    range(60, 120, 30),
                    range(0, 101, 20),
                    range(0, 101, 20),
                    range(0, 6, 2),
                    range(0, 3, 1),
                 ]

        if args.choose_range:
            lim = input('Outer limits for optimisation: ')
            lim = float(lim)

            a = [-lim, 0, lim]
            ranges = []
            for p in param:
                ranges.append(list(map(lambda x: x + p, a)))

            print(ranges)

    if args.back:
        bkg_events = parse.parse_file('background.txt', momenta_in_event=True)
        filtered_bkg = {}

    if args.transverse:
    # Apply a series of different filters in turn
##        lower_momentum = range(xrange[0], xrange[1], xrange[2])
##        higher_momentum = range(yrange[0], yrange[1], yrange[2])
        lower_momentum = ranges[0]
        higher_momentum = ranges[1]
        xlabel = '$p_{T1}$'
        ylabel = '$p_{T2}$'
        title = 'transverse momenta'
        for lower in lower_momentum:
            for higher in higher_momentum:
                filtered_higgs[(lower, higher)] = parse.combined_filter(higgs_events,
                                                                        num=1, momentum_lower=lower,
                                                                        momentum_higher=higher, energy_lower=0,
                                                                        energy_higher = 0, deta = 0, dazi = 0, invm1 = m1, invm2 = m2)
                if args.back:
                    filtered_bkg[(lower, higher)] = parse.combined_filter(bkg_events,
                                                                          num=1, momentum_lower=lower,
                                                                          momentum_higher=higher, energy_lower=0,
                                                                          energy_higher = 0, deta = 0, dazi = 0, invm1 = m1, invm2 = m2)

                print('Finished for pt_1 =  ' + str(lower) + ' and pt_2 = ' + str(higher))
    if args.energy:
##        lower_energy = range(xrange[0], xrange[1], xrange[2])
##        higher_energy = range(yrange[0], yrange[1], yrange[2])
        lower_energy = ranges[2]
        higher_energy = ranges[3]
        xlabel = '$E_1$'
        ylabel = '$E_2$'
        title = 'Energy'
        for lower in lower_energy:
            for higher in higher_energy:
                filtered_higgs[(lower, higher)] = parse.combined_filter(higgs_events,
                                                                        num = 1, momentum_lower = 0,
                                                                        momentum_higher = 0, energy_lower = lower,
                                                                        energy_higher = higher, deta = 0, dazi = 0, invm1 = m1, invm2 = m2)
                if args.back:
                    filtered_bkg[(lower, higher)] = parse.combined_filter(bkg_events,
                                                                          num = 1, momentum_lower = 0,
                                                                          momentum_higher = 0, energy_lower = lower,
                                                                          energy_higher = higher, deta = 0, dazi = 0, invm1 = m1, invm2 = m2)

                print('Finished for E_1 =  ' + str(lower) + ' and E_2 = ' + str(higher))
    if args.etaphi:
##        eta = list(map(radians, range(xrange[0], xrange[1], xrange[2])))
##        phi = list(map(radians, range(yrange[0], yrange[1], yrange[2])))
        eta = ranges[4]
        phi = ranges[5]
        ylabel = '$d\eta^2$'
        xlabel = '$d\phi^2$'
        title = 'azimuthal angle, and pseudorapidity'
        for az in phi:
            for rap in eta:
                filtered_higgs[(az, rap)] = parse.combined_filter(higgs_events,
                                                                        num = 1, momentum_lower = 0,
                                                                        momentum_higher = 0, energy_lower = 0,
                                                                        energy_higher = 0, deta = rap, dazi = az, invm1 = m1, invm2 = m2)

                if args.back:
                    filtered_bkg[(az, rap)] = parse.combined_filter(bkg_events,
                                                                     num = 1, momentum_lower = 0,
                                                                     momentum_higher = 0, energy_lower = 0,
                                                                     energy_higher = 0, deta = rap, dazi = az, invm1 = m1, invm2 = m2)

                print('Finished for phi =  ' + str(az) + ' and eta = ' + str(rap))
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

    if args.plot:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        ax.scatter(x, y, bins)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('Optimisation plot for ' + title + ' cuts.')
        plt.show()

    opt_x, opt_y,z_max  = get_largest(bins, x, y)

    if args.nopreset:
        opt_pT1, opt_pT2, opt_E1, opt_E2, opt_dphi, opt_deta = [0, 0, 0, 0, 0 ,0]
    if args.transverse:
        opt_pT1, opt_pT2 = opt_x, opt_y
    if args.energy:
        opt_E1, opt_E2 = opt_x, opt_y
    if args.etaphi:
        opt_dphi, opt_deta = opt_x, opt_y

    m1, m2 = 113, 132
    param = [opt_pT1, opt_pT2, opt_E1, opt_E2, opt_dphi, opt_deta, m1, m2]
    param = str(param)
    param = param.replace('[', '').replace(']', '')

    if args.out_opt:
        output_opt = open('optimised.txt', 'w')
        output_opt.write(param)
        output_opt.close()



if __name__ == '__main__':
    main()
