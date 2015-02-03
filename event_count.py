""" Generate and output file that works out how many four momenta are in event
    and puts them in a seperate file. """


import sys


def main():
    with open(sys.argv[1]) as data_file, open(sys.argv[1] + '_count', 'w') as output:
        raw = data_file.read().split('\n')

        num_four_momenta = 0
        first_event_found = False
        for line in raw:
            if line.startswith('Event'):
                if first_event_found:
                    output.write(str(num_four_momenta) + '\n')

                first_event_found = True
                num_four_momenta = 0
                continue

            if line:
                num_four_momenta += 1

        # Output the final event's count
        output.write(str(num_four_momenta))


if __name__ == '__main__':
    main()
