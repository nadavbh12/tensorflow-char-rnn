from music21 import converter, stream, harmony
import glob

ll = glob.glob("/home/nadav/Jazz/torch-rnn/music/parker/*.xml")
ll = ll[0:1]
# print ll
for song in ll:
    s = converter.parse(song)
    for measure in s.parts[0].measures(1, None):
        if isinstance(measure, stream.Measure):
            for e in measure.elements:
                if e.isinstance(harmony):
                    print e
