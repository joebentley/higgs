import matplotlib.pyplot as plt
import sys, argparse
import numpy as np

def parse_file(path, count=False):
    with open(path) as data_file:
        raw = data_file.read().replace('[', '').replace(']', '').split(',')
        raw = list(map(lambda x: float(x), raw))
    return raw



def main():
    cs_higgs = 17.35
    bf_yy = 2.28e-3
    cs_bkg = 140
    w_higgs =(cs_higgs * bf_yy)**-1
    w_bkg = 1/float(cs_bkg)
    invariant_masses_higgs = parse_file('outputIM_Higgs.txt')
    invariant_masses_bkg = parse_file('outputIM_bkg.txt')
    invariant_masses_combined = parse_file('outputIM_cmb.txt')
    #Resolution of histogram
    res = 3
    #Use numpy to manually set up each histogram so the weights can be applied to each and recombined at the end.
    bins = list(map(lambda x: res * x, range(0, int(sorted(invariant_masses_combined)[-1]))))
    hist_higgs, bins = np.histogram(invariant_masses_higgs, bins)
    hist_bkg, bins = np.histogram(invariant_masses_bkg, bins)
    sum_higgs = float(sum(hist_higgs))
    sum_bkg = float(sum(hist_bkg))
    hist_higgs = list(map(lambda x: x*w_higgs, hist_higgs))
    hist_bkg = list(map(lambda x: x*w_bkg, hist_bkg))
    hist_comb = list(map(lambda x, y: x + y, hist_higgs, hist_bkg)) 
    
    sum_hist_comb = float(sum(hist_comb))
    #hist_comb = list(map(lambda x: x/sum_hist_comb, hist_comb))
    plt.bar(bins[0:len(bins) - 1], hist_comb)
    #plt.bar(bins[0:len(bins) - 1], hist_higgs)
    plt.xlabel('Invariant Mass (GeV/c^2)')
    plt.ylabel('Frequency')
    plt.title('Histogram of invariant masses')
    #plt.axis([0, 200, 0, 0.1])
    plt.grid(True)
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    main()
