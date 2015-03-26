#!/usr/bin/env python3

import pickle, math
import matplotlib.pyplot as plt
import sys, argparse
from math import *
import numpy as np
import scipy.optimize as opt

def statistical_significance(signal, background):
    """ Calculate statistical significance given num. signal events
        and num. background events. """
    return signal / sqrt(signal + background)


def parse_file(path, count=False):
    with open(path, 'rb') as data_file:
        return pickle.load(data_file)

def fit_bkg(x, y, res=3, x_min=120, x_max=150, length = 100):
    #Fit exp
    #Want a continuous function independant of resolution
    #This is the fitting resolution (make it large to be continuous)
    x = x[:int(x_max/res)]
    y = y[:int(x_max/res)]
    f = lambda x, a0, a1, a2, a3, a4: a0 + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4
    #g = lambda x, n: x**n * exp(-x)
    c = opt.curve_fit(f, x, y)[0]
    #d = opt.curve_fit(g, x, y)[0]
    N = int(1e4)
    A = sorted(y)[-1]
    xmin = y.index(A)
    xmax = xmin + length
    #x_min to x_max - so piecewise could be done.
    #k = log(y[x_min]/y[x_max])/float(x_max)
    x_range = range(0,  N)
    x_res = list(map(lambda x: (x_min + x * (x_max - x_min)/N), x_range))
    #y_res = list(map(lambda x: A* exp(-(x - x_min) * k), x_res))
    y_res = list(map(lambda x: f(x, c[0], c[1], c[2], c[3], c[4]), x_res))
    #y_res = list(map(lambda x: g(x, c[0]), x_res))

    return [x_res, y_res]

def main():
    parser = argparse.ArgumentParser(description = 'Generate histogram from Higgs and background data')
    parser.add_argument('--not_comb', action = 'store_true', help='Do not plot the combined data')
    parser.add_argument('--higgs', action = 'store_true', help = 'Plots the histogram from only the Higgs signal')
    parser.add_argument('--bkg', action = 'store_true', help = 'Plots the histogram from only the background')
    parser.add_argument('--masses', default = 'unfiltered_invmasses', help = 'Path to directory containing invariant masses')
    parser.add_argument('--norm', action = 'store_true', help = 'Normalise all plots')
    parser.add_argument('--ratio', action = 'store_true', help = 'Use ratio to calculate the weights of higgs and bkgs.')
    parser.add_argument('--fit_bkg', action = 'store_true', help = 'Plot line of background when doing combined.')
    parser.add_argument('--lower', help = 'Lower boundary on mass window', default=120, type=int)
    parser.add_argument('--upper', help = 'Upper boundary on mass window', default=140, type=int)
    args = parser.parse_args()

    invariant_masses_higgs = parse_file(args.masses + '/outputIM_Higgs.txt')
    invariant_masses_bkg = parse_file(args.masses + '/outputIM_bkg.txt')
    invariant_masses_combined = parse_file(args.masses + '/outputIM_cmb.txt')

    cs_higgs = 17.35
    bf_yy = 2.28e-3
    cs_bkg = 140
    w_higgs = cs_higgs * bf_yy/cs_bkg
    w_bkg = 1

    if args.ratio:
        ratio = (w_higgs / w_bkg) * len(invariant_masses_bkg)
        print('Expected num. Higgs events:', int(ratio))
        print('Actual num. Higgs events:  ', len(invariant_masses_higgs))

        w_higgs = ratio / len(invariant_masses_higgs)
        w_bkg = 1

    print('Higgs weighting:', w_higgs)
    print('Backr weighting:', w_bkg)

    #Resolution of histogram
    res = 1000
    #Use numpy to manually set up each histogram so the weights can be applied to each and recombined at the end.
    #bins = list(map(lambda x: res * x, range(0, int(sorted(invariant_masses_combined)[-1]))))

    hist_higgs, bins_higgs = np.histogram(invariant_masses_higgs, res)
    hist_bkg, bins_bkg = np.histogram(invariant_masses_bkg, res)

    hist_higgs = list(map(lambda x: x*w_higgs, hist_higgs))
    hist_bkg = list(map(lambda x: x*w_bkg, hist_bkg))

    hist_comb, bins = np.histogram(invariant_masses_higgs + invariant_masses_bkg, res)

    # Get rid of zero values? (TODO: change this)
    hist_comb[0] = 0

    # Get the bins for the mass range and then find the statistical
    # significance of the higgs in the mass range
    x = np.array(range(args.lower, args.upper))
    indices_higgs = np.digitize(x, bins_higgs)
    indices_bkg = np.digitize(x, bins_bkg)

    sum_higgs = 0
    sum_bkg = 0
    for (index_higgs, index_bkg) in zip(indices_higgs, indices_higgs):
        sum_higgs += hist_higgs[index_higgs]
        sum_bkg += hist_bkg[index_bkg]


    print('In mass window {0} to {1}: '.format(args.lower, args.upper))
    print('sigma = ' + str(statistical_significance(sum_higgs, sum_bkg)))


    bins = bins[0:len(bins) - 1]
    #hist_comb = list(map(lambda x: x/sum_hist_comb, hist_comb))
    if args.norm:
        sum_higgs = float(sum(hist_higgs))
        sum_bkg = float(sum(hist_bkg))
        sum_comb = float(sum(hist_comb))
        hist_higgs = list(map(lambda x: x/sum_higgs, hist_higgs))
        hist_bkg = list(map(lambda x: x/sum_bkg, hist_bkg))
        hist_comb = list(map(lambda x: x/sum_comb, hist_comb))

    #bkg_x, bkg_y = fit_bkg(bins, hist_bkg, res)

    if not args.not_comb:
        plt.bar(bins, hist_comb, label = 'Higgs + Background', color='b')

    if args.fit_bkg:
        plt.plot(bkg_x, bkg_y, label = 'Background line', color = 'r')


    if args.higgs:
        plt.bar(bins, hist_higgs, label = 'Higgs', color='r')

    if args.bkg:
        plt.bar(bins, hist_bkg, label = 'Background', color='g')

    plt.xlabel('$m_{\gamma \gamma}$ (GeV/$c^2$)')
    plt.ylabel('Frequency')
    plt.title('Histogram of invariant masses')
    #plt.axis([0, 200, 0, 0.1])
    plt.xlim((0, 200))
    plt.grid(True)
    plt.legend(loc = 'upper left')
    plt.show()

if __name__ == '__main__':
    main()
