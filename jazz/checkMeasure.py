import music21
import sys
from gatherDataParker import reverse_vocab


class InvalidBarError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def num_of_pitches_in_chord(chord, pitches):
    num = 0
    for pitch in pitches:
        for chordPitch in chord.pitches:
            if pitch.name == chordPitch.name:
                num += 1
    return num


def num_of_pitches_in_scale(chord, pitches):
    num = 0
    scale_pitches = get_scale_pitches_from_chord(chord)
    for pitch in pitches:
        for scalePitch in scale_pitches:
            if pitch.name == scalePitch.name:
                num += 1
    return num


def get_scale_pitches_from_chord(chord):
    chord_kind = chord.chordKind
    # print("chord_kind: " + chord_kind)
    root = chord.root()
    net = music21.scale.intervalNetwork.IntervalNetwork()
    if 'major' == chord_kind or 'major-seventh' == chord_kind or 'major-sixth' == chord_kind:
        sc = music21.scale.MajorScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'minor' == chord_kind or 'minor-seventh' == chord_kind or 'minor-sixth' == chord_kind \
            or 'minor-ninth' == chord_kind:
        sc = music21.scale.MinorScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'mM7' == chord_kind:
        sc = music21.scale.HarmonicMinorScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'm7b5' == chord_kind or 'half-diminished-seventh' == chord_kind:
        sc = music21.scale.LocrianScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'dominant-seventh' == chord_kind or 'suspended-fourth' == chord_kind  or 'dominant-ninth' == chord_kind \
            or 'dominant-13th' == chord_kind:
        sc = music21.scale.MixolydianScale(root)
        return [p for p in sc.getPitches(root)]
    elif 'augmented' == chord_kind or 'augmented-seventh' == chord_kind:
        edge_list = ['M2', 'M2', 'M2', 'M2', 'm2', 'M2', 'm2']
        net.fillBiDirectedEdges(edge_list)
        return [p for p in net.realizePitch(root)]
    elif 'diminished' == chord_kind or 'diminished-seventh' == chord_kind:
        edge_list = ['M2', 'M2', 'm2', 'm2', 'M2', 'M2', 'M2']
        net.fillBiDirectedEdges(edge_list)
        return [p for p in net.realizePitch(root)]
    else:
        print 'unrecognized chord: ' + chord_kind
        sys.exit(1)

def replaceVocab(krn_stream):
    for token in sorted(reverse_vocab.items(), key=lambda x: x[1]):
        if token[0] in krn_stream:
            # krn_stream = krn_stream.replace(token[0], reverse_vocab[token[0]])
            krn_stream = krn_stream.replace(token[0], token[1])
    return krn_stream

def get_measure_score(krn_stream, chord_string):
    chord = music21.harmony.ChordSymbol(chord_string)
    # krn_stream = replaceVocab(krn_stream)

    wrapped_input = "**kern\n" + "*M4/4\n" + "*^\n" + krn_stream + "\n==\n*-"
    m = music21.converter.parse(wrapped_input)
    p = m.pitches

    rests_only = (len(p) == 0)
    if rests_only or (m.highestTime > 4.0 or not m.isWellFormedNotation()):
        raise InvalidBarError('Bar is illegal')

    score = float(num_of_pitches_in_scale(chord, p)) / float(len(p)) \
        + 3 * float(num_of_pitches_in_chord(chord, p)) / float(len(p))
    return score


def get_measure_score2(krn_stream, chord_string1, chord_string2):
    chord1 = music21.harmony.ChordSymbol(chord_string1)
    chord2 = music21.harmony.ChordSymbol(chord_string2)

    wrapped_input = "**kern\n" + "*M4/4\n" + "*^\n" + krn_stream + "\n==\n*-"
    m = music21.converter.parse(wrapped_input)
    p = m.pitches

    rests_only = (len(m.pitches) == 0)
    if rests_only or (m.highestTime > 4.0 or not m.isWellFormedNotation()):
        raise InvalidBarError('Bar is illegal')

    flat = m.flat.notes.stream()
    p1 = [x for x in flat.elements if x.offset < 2]
    p2 = [x for x in flat.elements if x.offset >= 2]

    if not p1 or not p2:
        score = float(num_of_pitches_in_scale(chord1, p)) / float(len(p)) \
            + 3 * float(num_of_pitches_in_chord(chord1, p)) / float(len(p))
    else:
        score = float(num_of_pitches_in_scale(chord1, p1)) / float(len(p1)) \
                + float(num_of_pitches_in_scale(chord2, p2)) / float(len(p2)) \
                + 3 * float(num_of_pitches_in_chord(chord1, p1)) / float(len(p1)) \
                + 3 * float(num_of_pitches_in_chord(chord1, p2)) / float(len(p2))
    return score

def get_pitches_score(pitches, chord):
    scale_pitches = get_scale_pitches_from_chord(chord)
    score = 0
    for p in pitches:
        if p in chord.pitches:
            if p.offset.is_integer():
                score += 5
            else:
                score += 3
        elif p in scale_pitches:
            score += 1
    return score


def get_measure_score3(krn_stream, chord_string1, chord_string2):
    chord1 = music21.harmony.ChordSymbol(chord_string1)
    chord2 = music21.harmony.ChordSymbol(chord_string2)

    wrapped_input = "**kern\n" + "*M4/4\n" + "*^\n" + krn_stream + "\n==\n*-"
    m = music21.converter.parse(wrapped_input)
    pitches = m.pitches

    rests_only = (len(m.pitches) == 0)
    if rests_only or (m.highestTime > 4.0 or not m.isWellFormedNotation()):
        raise InvalidBarError('Bar is illegal')

    flat = m.flat.notes.stream()
    p1 = [x for x in flat.elements if x.offset < 2]
    p2 = [x for x in flat.elements if x.offset >= 2]

    score = 0
    score += get_pitches_score(p1, chord1)
    score += get_pitches_score(p2, chord2)

    return score



    # if not p1 or not p2:
    #     score = float(num_of_pitches_in_scale(chord1, pitches)) / float(len(pitches)) \
    #         + 3 * float(num_of_pitches_in_chord(chord1, pitches)) / float(len(pitches))
    # else:
    #     score = float(num_of_pitches_in_scale(chord1, p1)) / float(len(p1)) \
    #             + float(num_of_pitches_in_scale(chord2, p2)) / float(len(p2)) \
    #             + 3 * float(num_of_pitches_in_chord(chord1, p1)) / float(len(p1)) \
    #             + 3 * float(num_of_pitches_in_chord(chord1, p2)) / float(len(p2))
    return score
