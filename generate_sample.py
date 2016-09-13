from jazz.postprocess import add_header_and_footer
import sample_jazz
from jazz.displayXml import display_xml

def main(args):
    sample = sample_jazz.main(['--init_dir=outputs/best', '--temperature=1'])
    sample = add_header_and_footer(sample)
    print sample
    display_xml(sample)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])