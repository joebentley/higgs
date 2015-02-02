import matplotlib.pyplot as plt
import sys, argparse

def parse_file(path, count=False):
    with open(path) as data_file:
        raw = data_file.read().replace('[', '').replace(']', '').split(',')
        raw = list(map(lambda x: float(x), raw))
    return raw
        
    

def main():
    cs_higgs = 17.35
    bf_yy = 2.28e-3
    cs_bkg = 140
    w = cs_higgs * bf_yy/cs_bkg
    invariant_masses_higgs = parse_file('outputIM_Higgs.txt')
    '''invariant_masses_bkg = parse_file('outputIM_bkg.txt')
    invariant_masses_combined = parse_file('outputIM_cmb.txt')'''
    weights = list(map(lambda x: w, invariant_masses_higgs))
    #weights_bkg = list(map(lambda x: 1, invariant_masses_bkg))
    #weights_combined = list(map(lambda x: 1, invariant_masses_combined))
    n, bins, patches = plt.hist(invariant_masses_higgs, 1000, normed=True,
             weights=weights, facecolor='b', alpha=0.75, label='Higgs')
    '''n, bins, patches = plt.hist(invariant_masses_bkg, 1000, normed=False, weights = weights_bkg,
                                #facecolor='g', alpha=0.75, label='Background')
    n, bins, patches = plt.hist(invariant_masses_combined, 1000, normed = False, weights = weights_combined,
                                facecolor = 'r', alpha = 0.75, label = 'Combined')'''
    plt.xlabel('Invariant Mass (GeV/c^2)')
    plt.ylabel('Frequency')
    plt.title('Histogram of invariant masses')
    #plt.axis([0, 200, 0, 10000])
    plt.grid(True)
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    main()
