from jazz.postprocess import add_header_and_footer
import sample_jazz
from jazz.displayXml import display_xml
from jazz.extract_chords_from_xml import extract_chords_from_xml
from jazz.convertXml2Krn import xml_2_krn
from jazz.gatherDataParker import removeHeader, removeTrailer, removeOdeCharacters, removeBeamChars
import argparse
import music21
import codecs


def generate_samples(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str,
                        default='samples',
                        help='Dir to save samples')
    parser.add_argument('--xml_file', type=str,
                        default='',
                        help='xml file to convert to krn')
    parser.add_argument('--num_samples', type=int,
                        default=1,
                        help='How many samples to generate')
    args = parser.parse_args()

    create_chords_file(args.xml_file)
    xml_2_krn(args.xml_file)
    krn_file = args.xml_file.replace('.xml', '.krn')
    start_notes = clean_krn(krn_file)

    # print start_notes
    # display_xml(add_header_and_footer(start_notes))

    for i in range(0,args.num_samples):
        sample = sample_jazz.main(['--init_dir=outputs/best_tokenized', '--temperature=1', \
                                   '--chords_file=/tmp/tmp_chords.txt', '--start_text=' + start_notes])
        sample = add_header_and_footer(sample)
        file_name = args.output_dir + '/' + str(i)
        open(file_name + '.krn', "w").writelines(sample)
        convert_to_midi_and_save(sample, file_name + '.mid')
        display_xml(sample)


def clean_krn(krn_file):
    song_in_krn = codecs.open(krn_file, "r")
    song = song_in_krn.readlines()
    song = removeHeader(song)
    song = removeTrailer(song)
    start_notes = ''
    for l in song:
        # print l
        if l.startswith("="):
            l = '@\n'
        if l.startswith("!"):
            ## ignore comments
            continue
        if l.startswith("*^") or l.startswith("*v"):
            ## ignore double spines
            continue
        if l.startswith("*"):
            continue
        if l.startswith("=="):
            break
        l = removeOdeCharacters(l)
        l = removeBeamChars(l)
        start_notes += l
    start_notes += '@\n'
    return start_notes


def create_chords_file(xml_file):
    chords = extract_chords_from_xml(xml_file)
    with codecs.open("/tmp/tmp_chords.txt", 'r+') as chords_file:
        chords_file.writelines(chords)
        chords_file.close()


def convert_to_midi_and_save(kern, file_name):
    m = music21.converter.parse(kern)
    mf = music21.midi.translate.streamToMidiFile(m)
    mf.open(file_name, 'wb')
    mf.write()
    mf.close()

if __name__ == '__main__':
    import sys
    generate_samples(sys.argv[1:])