import music21
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_krn')
args = parser.parse_args()

m = music21.converter.parse(args.input_krn)
m.show("musicxml")
