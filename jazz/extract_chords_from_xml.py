from music21 import *
import sys


def extract_chords_from_xml(xml_file):
    # s = converter.parse('/home/nadav/Jazz/torch-rnn/music/parker/1090 Au Privave Charlie Parker Take 1.xml')
    s = converter.parse(xml_file)
    m = s.parts[0].getElementsByClass(stream.Measure)

    i = 0;
    chordChart = '\n'
    chords = ''
    while i < len(m):
        c = m[i].getElementsByClass(harmony.ChordSymbol)
        if (len(c) == 0):
            chordChart += '{:20} | '.format('')
        if (len(c) == 1):
            c0 = c[0].figure
            chordChart += '{:20} | '.format(c0)
            chords += c0 + ' '
            # print(c0)
        if (len(c) == 2):
            c0 = c[0].figure
            c1 = c[1].figure
            chordChart += '{:10}{:10} | '.format(c0, c1)
            chords += c0 + ',' + c1 + ' '
        if (len(c) == 3):
            c0 = c[0].figure
            c1 = c[1].figure
            c2 = c[2].figure
            chordChart += '{:7}{:7}{:7}| '.format(c0, c1, c2)
        if (len(c) == 4):
            c0 = c[0].figure
            c1 = c[1].figure
            c2 = c[2].figure
            c3 = c[3].figure
            chordChart += '{:5}{:5}{:5}{:5} | '.format(c0, c1, c2, c3)
        i += 1
        if i % 4 == 0: chordChart += '\n'

    # print(chordChart)
    # print(chords)
    return chords

if __name__ == '__main__':
    # print sys.argv[1:]
    extract_chords_from_xml(sys.argv[1:])