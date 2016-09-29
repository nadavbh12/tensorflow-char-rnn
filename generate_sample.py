from jazz.postprocess import add_header_and_footer
import sample_jazz
from jazz.displayXml import display_xml
import argparse
import music21


def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str,
                        default='samples',
                        help='Dir to save samples')
    parser.add_argument('--num_samples', type=int,
                        default=1,
                        help='How many samples to generate')
    args = parser.parse_args()

    for i in range(0,args.num_samples):
        sample = sample_jazz.main(['--init_dir=outputs/best', '--temperature=1.5', '--chords_file=chords/12_bar_blues_twice.txt'])
        sample = add_header_and_footer(sample)
        file_name = args.output_dir + '/' + str(i)
        open(file_name + '.krn', "w").writelines(sample)
        convert_to_midi_and_save(sample, file_name + '.mid')
        display_xml(sample)


def convert_to_midi_and_save(kern, file_name):
    m = music21.converter.parse(kern)
    mf = music21.midi.translate.streamToMidiFile(m)
    mf.open(file_name, 'wb')
    mf.write()
    mf.close()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])