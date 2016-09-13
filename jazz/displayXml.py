import music21
import argparse


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_krn')
    args = parser.parse_args()
    display_xml(args.input_krn)


def display_xml(kern):
    m = music21.converter.parse(kern)
    m.show("musicxml")

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])