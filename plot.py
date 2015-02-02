import matplotlib.pyplot as plt
import sys, argparse

def parse_file(path, count=False):
    with open(path) as data_file:
        raw = data_file.read().replace('[', '').replace(']', '').split(',')
        raw = list(map(lambda x: float(x), raw))
    return raw
        
    

def main():
    parser = argparse.ArgumentParser(description = 'Generate histogram')
    parser.add_argument('--higgs_only', action = 'store_true', help = 'Only plot higgs')
    parser.add_argument('--bkg_only', action = 'store_true', help = 'Only plot background')
    parser.add_argument('--combined', action = 'store_false', help = 'Default: plot both higgs and background''')
    args = parser.parse_args()
    cs_higgs = 17.35
    bf_yy = 2.28e-3
    cs_bkg = 140
    w = cs_higgs * bf_yy/cs_bkg
    invariant_masses_higgs = parse_file('outputIM_Higgs.txt')
    invariant_masses_bkg = parse_file('outputIM_bkg.txt')
    invariant_masses_combined = parse_file('outputIM_cmb.txt')
    weights = list(map(lambda x: w, invariant_masses_higgs))
    weights_bkg = list(map(lambda x: 1, invariant_masses_bkg))
    weights_combined = list(map(lambda x: 1, invariant_masses_combined))
    if args.higgs_only:
        args.combined = False
        n, bins, patches = plt.hist(invariant_masses_higgs, 1000, normed=True, weights=weights, facecolor='b', alpha=0.75, label='Higgs')
    if args.bkg_only:
        args.combined = False
        n, bins, patches = plt.hist(invariant_masses_bkg, 1000, normed=True, weights = weights_bkg, facecolor='g', alpha=0.75, label='Background')
    if args.combined:
        n, bins, patches = plt.hist(invariant_masses_combined, 1000, normed = True, weights = weights_combined,
                                facecolor = 'r', alpha = 0.75, label = 'Combined')
   
    plt.xlabel('Invariant Mass (GeV/c^2)')
    plt.ylabel('Frequency')
    plt.title('Histogram of invariant masses')
    plt.axis([0, 200, 0, 0.1])
    plt.grid(True)
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    main()
