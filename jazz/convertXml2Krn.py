import argparse, os
import music21
import glob

# parser = argparse.ArgumentParser()
# parser.add_argument('--input_dir')
# parser.add_argument('--output_dir')
# args = parser.parse_args()
#
# # ll = glob.glob(args.input_dir + "4 Serpents Tooth Rollins Bird Take 1.xml")
# ll = glob.glob(args.input_dir + "*.xml")
# for song in ll:
#     nameArray = song.split('/')
#     songName = nameArray[-1]
#     inputName = song.replace(' ', '\ ')
#     outputName = songName.replace(' ', '_')
#     outputName = outputName.replace('.xml', '.krn')
#     runCommand = "./scripts/xml2hum %s > %s" % (inputName, args.output_dir + '/' + outputName)
#
#     os.system(runCommand)

def xml_2_krn(xml_file):
    nameArray = xml_file.split('/')
    songName = nameArray[-1]
    inputName = xml_file.replace(' ', '\ ')
    outputName = songName.replace(' ', '_')
    outputName = outputName.replace('.xml', '.krn')
    runCommand = "./jazz/xml2hum %s > %s" % (inputName, '/'.join(nameArray[:-1]) + '/' + outputName)
    # print runCommand
    os.system(runCommand)
