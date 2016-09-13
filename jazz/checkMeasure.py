import music21
import sys


class InvalidBarError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def num_of_pitches_in_chord(chord, stream):
    num = 0
    for pitch in stream.pitches:
        for chordPitch in chord.pitches:
            if pitch.name == chordPitch.name:
                num += 1
    return num


def num_of_pitches_in_scale(chord, stream):
    num = 0
    scale_pitches = get_scale_pitches_from_chord(chord)
    for pitch in stream.pitches:
        for scalePitch in scale_pitches:
            if pitch.name == scalePitch.name:
                num += 1
    return num


def get_scale_pitches_from_chord(chord):
    chord_kind = chord.chordKind
    # print("chord_kind: " + chord_kind)
    root = chord.root()
    net = music21.scale.intervalNetwork.IntervalNetwork()
    if 'major' == chord_kind or 'major-seventh' == chord_kind:
        sc = music21.scale.MajorScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'minor' == chord_kind or 'minor-seventh' == chord_kind:
        sc = music21.scale.MinorScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'dominant-seventh' == chord_kind:
        sc = music21.scale.MixolydianScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'augmented' == chord_kind or 'augmented-seventh' == chord_kind:
        edge_list = ['M2', 'M2', 'M2', 'M2', 'm2', 'M2', 'm2']
        net.fillBiDirectedEdges(edge_list)
        return [p for p in net.realizePitch(root)]
    elif 'diminished' == chord_kind:
        edge_list = ['M2', 'M2', 'm2', 'm2', 'M2', 'M2', 'M2']
        net.fillBiDirectedEdges(edge_list)
        return [p for p in net.realizePitch(root)]
    else:
        print 'unrecognized chord'
        sys.exit(1)


def get_measure_score(krn_stream, chord_string):
    chord = music21.harmony.ChordSymbol(chord_string)

    wrapped_input = "**kern\n" + "*M4/4\n" + "*^\n" + krn_stream + "\n==\n*-"
    m = music21.converter.parse(wrapped_input)

    rests_only = (len(m.pitches) == 0)
    if rests_only or (m.highestTime > 4.0 or not m.isWellFormedNotation()):
        raise InvalidBarError('Bar is illegal')

    score = float(num_of_pitches_in_scale(chord, m)) / float(len(m.pitches)) \
        + 3 * float(num_of_pitches_in_chord(chord, m)) / float(len(m.pitches))
    return score
