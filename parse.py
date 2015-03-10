#!/usr/bin/env python3

import sys, argparse, pickle
import matplotlib.pyplot as plt
from multiprocessing import Pool

from fourmomentum import FourMomentum
from event import Event


#Number filter (more than n events)
def number_threshold(events, n):
    """ Filters events so that only events with more than
        n momenta are returned. """
    return list(filter(lambda x: len(x) > n, events))

#Transverse momentum filter
def transverse_threshold(events, p_T):
    new_events = []
    for event in events:
        event.momenta = list(filter(lambda x: x.transverse() > p_T, event.momenta))
        if len(event.momenta) > 0:
            new_events.append(event)
    return new_events

#Keeps the 20GeV transverse momentum
def transverse_threshold_2(events, p_T):
    events2 = []
    for event in events:
        for momenta in event.momenta:
            # If there are any transverse momenta > p_T, that event is valid
            if momenta.transverse() > p_T:
                events2.append(event)
                break
    return events2

#Energy filter
def energy_threshold(events, E):
    new_events = []
    for event in events:
        event.momenta = list(filter(lambda x: x.energy > E, event.momenta))
        if len(event.momenta) > 0:
            new_events.append(event)
    return new_events

def energy_threshold_2(events, E):
    events2 = []
    for event in events:
        for momenta in event.momenta:
            if momenta.energy > E:
                events2.append(event)
                break
    return events2

def deta_threshold(events, eta):
    res = list(filter(lambda x: x.eta_diff_max() > eta**2, events))
    return res

def dazi_threshold(events, azi):
    return list(filter(lambda x: x.azi_diff_max() > azi**2, events))

def invmass_threshold(events, m):
    return list(filter(lambda x: x.invariant_mass()>m, events))

def invmass_limit(events, m):
    return list(filter(lambda x: x.invariant_mass() < m, events))

#combined filter
def combined_filter(events, num=1, momentum_lower=4, momentum_higher=50, energy_lower=20, energy_higher = 20,
                    deta = 0, dazi = 0, invm1 = 100, invm2 = 1000):
    #Filtering events
    #only show events with at least 2 momenta
    res = number_threshold(events, num)
    print("Number filtered")
    #Exclude in lower invariant mass range
    res = invmass_threshold(res, invm1)
    print("Lower Inv mass filtered")

    res = transverse_threshold(res, momentum_lower)
    res = transverse_threshold_2(res, momentum_higher)
    print("Momenta filtered")

    res = energy_threshold(res, energy_lower)
    res = energy_threshold_2(res, energy_higher)
    print("Energy filtered")

    #Pick2 highest p_T
    for event in res:
        event = event.filter_highest_pt(2)

    print('Chose 2 highest p_T photons')
    #res = deta_threshold(res, deta)
    print("Pseudorapidity filtered")
    #res = dazi_threshold(res, dazi)
    print("Azimuthal filtered")

    for event in res:
        if len(event) > 2:
            raise ValueError

    #Exclude higher invariant mass range
    #res = invmass_limit(res, invm2)
    print('Upper invariant mass')
    print("Finished filtering")
    return res

def get_invariant_masses(events):
    invariant_masses = []
    for i, event in enumerate(events):
        invariant_masses.append(event.invariant_mass())
    return invariant_masses

def parse_file(path, count=False, momenta_in_event=False):
    """ Parse the event file with name path returning Event objects.

        Keyword arguments:
        path  -- The filepath of the event file
        count -- Whether to print the current num. processed events
        momenta_in_event -- Whether to use file containing num. four
                            momenta in each event.

        The four momenta count file should have the filename path + '_count'
        and each line should contain the number of four momenta in each
        event of the events file (as specified in the path argument) in
        order of event appearance (the first number in the count file
        has the number of four momenta in the first event of the events file)."""

    events = []
    with open(path) as data_file:
        raw = data_file.read().split('\n')

        if momenta_in_event:
            count_file = open(path + '_count')
            counts = count_file.read().split('\n')
            # Current event number in file
            current_event_number = 0

        four_momenta_count = 0
        counter = 0
        p = Pool(100)
        for i, line in enumerate(raw):
            # If the line starts with 'Event', begin to process it
            if line.startswith('Event'):
                # If number of momenta given, use that, else just use 20
                if momenta_in_event:
                    four_momenta_count = int(counts[current_event_number])
                    current_event_number += 1
                else:
                    four_momenta_count = 20

                new_event = Event.from_text(raw[i+1:i+four_momenta_count])
                p.apply_async(events.append(new_event))
                #events.append(Event.from_text(raw[i:i+10]))

                if count:
                    counter += 1
                    if counter % 1000 == 0:
                        print(counter)

    return events



def main():
    parser = argparse.ArgumentParser(description='Generate histogram from Higgs event data')
    parser.add_argument('--higgs', nargs=1, default='higgs.txt', metavar='path_to_higgs',
                        dest='higgs_path', help='Relative path to higgs data')
    parser.add_argument('--background', nargs=1, default='background.txt', metavar='path_to_background',
                        dest='background_path', help='Relative path to background data')
    parser.add_argument('--print_higgs', action='store_true',
                        help='Whether to print the calculated invariant masses of the Higgs signal to stdout.')
    parser.add_argument('--print_bkg', action = 'store_true',
                        help='Whether to print the calculated invariant masses of the background to stdout.')
    parser.add_argument('--parsed_higgs', action='store_true',
                        help='Print parsing information of Higgs signal to stdout.')
    parser.add_argument('--parsed_bkg', action='store_true',
                        help='Print parsing information of background to stdout.')
    parser.add_argument('--count', action='store_true',
                        help='Whether to print current line of parsing.')
    parser.add_argument('--momenta_count_in_event', action='store_false',
        help="""Don't use files which hold the number of events in the event,
                with the name of the datafile + '_count'.""")
    parser.add_argument('--onlyhiggs', action='store_true',
        help="""Only use the Higgs file (don't parse the background)""")
    parser.add_argument('--opt', action = 'store_true', help = 'uses optimised values')

    args = parser.parse_args()
    default_param = [4, 50, 20, 20, 0, 0, 50]
    p_T1, p_T2, E_1, E_2, dphi, deta, m = default_param

    if args.opt:
        opt_param = open('optimised.txt', 'r').read().split(',')
        opt_param = list(map(lambda x: float(x), opt_param))
        p_T1, p_T2, E_1, E_2, dphi, deta, m, m2 = opt_param

    # Higgs signal
    higgs_events = parse_file(args.higgs_path, count=args.count,
            momenta_in_event=args.momenta_count_in_event)
    print("Parsed higgs")
    higgs_events = combined_filter(higgs_events, num = 1, momentum_lower = p_T1, momentum_higher = p_T2, energy_lower = E_1, energy_higher = E_2,
                                   deta = deta, dazi = dphi)
    print("Filtered higgs")
    invariant_masses_higgs = get_invariant_masses(higgs_events)
    print("Got invariant masses higgs")

    # Background signal
    if not args.onlyhiggs:
        bkg_events = parse_file(args.background_path, count=args.count,
                momenta_in_event=args.momenta_count_in_event)
        print("Parsed background")
        bkg_events = combined_filter(bkg_events, num = 1, momentum_lower = p_T1, momentum_higher = p_T2, energy_lower = E_1, energy_higher = E_2,
                                       deta = deta, dazi = dphi)
        print("Filtered background")
        invariant_masses_bkg = get_invariant_masses(bkg_events)
        invariant_masses_combined = invariant_masses_higgs + invariant_masses_bkg
        print("Got invariant masses background")
    else:
        invariant_masses_combined = invariant_masses_higgs

    if args.print_higgs:
        for mass in invariant_masses_higgs:
            print(mass)

    if args.print_bkg:
        for mass in invariant_masses_bkg:
            print(mass)

    if args.parsed_higgs:
        for event in higgs_events:
            print(event.momenta)
            print('Event', event.id)
            for momenta in event.momenta:
                print('Energy:', momenta.energy)
                print('p_T:', momenta.transverse())

            print('Invariant mass:', invariant_mass)

    if args.parsed_bkg:
        for event in bkg_events:
            print(event.momenta)
            print('Event', event.id)
            for momenta in event.momenta:
                print('Energy:', momenta.energy)
                print('p_T:', momenta.transverse())

            print('Invariant mass:', invariant_mass)

    print("Writing invariant masses to file")
    if args.onlyhiggs:
        #out_higgs = open('outputIM_Higgs.txt', 'r+')
        #out_higgs.truncate()
        #out_higgs.close()
        out_higgs = open('outputIM_Higgs.txt', 'w')
        out_higgs.write(str(invariant_masses_higgs))
    else:
        #out_bkg = open('outputIM_bkg.txt', 'r+')
        #out_bkg.truncate()
        #out_bkg.close()
        #out_cmb = open('outputIM_cmb.txt', 'r+')
        #out_cmb.truncate()
        #out_cmb.close()
        with open('outputIM_Higgs.txt', 'wb') as f:
            pickle.dump(invariant_masses_higgs, f)
        with open('outputIM_bkg.txt', 'wb') as f:
            pickle.dump(invariant_masses_bkg, f)
        with open('outputIM_cmb.txt', 'wb') as f:
            pickle.dump(invariant_masses_combined, f)

if __name__ == '__main__':
    main()


