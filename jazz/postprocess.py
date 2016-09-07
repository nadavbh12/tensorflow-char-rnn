import argparse
import music21

parser = argparse.ArgumentParser()
parser.add_argument('--input_krn')
parser.add_argument('--header')
parser.add_argument('--trailer')
args = parser.parse_args()

f = open(args.input_krn,"r").readlines()
r = []
bar = 1
for l in f:
    if l.startswith("@"):
        if bar == 1:
            r.append("=1-\t\n")
#             r.append("=1-\t=1-\n")
            #r.append("=1-\t=1-\t=1-\n")
        else:
            r.append("={bar}\n".format(bar=bar))
#             r.append("={bar}\t={bar}\n".format(bar=bar))
            #r.append("={bar}\t={bar}\t={bar}\n".format(bar=bar))
        bar += 1
    else:
        r.append(l)
header = open(args.header,"r").readlines()
trailer = open(args.trailer,"r").readlines()
open(args.input_krn,"w").writelines(header)
open(args.input_krn,"a").writelines(r)
open(args.input_krn,"a").writelines(trailer)

# alternative approach

# for l in f:
#     if l.startswith("@"):
#         r.append(l)
# 
# wrappedInput = "**kern\n" + "*M4/4\n" + "*^\n" + r + "\n==\n*-"
# # print wrappedInput 
# try:
#     m = music21.converter.parse(r)
# #     catch music21.humdrum.spineParser.HumdrumException
# except:
#     sys.exit(1)
# 
# rMeasures = r.makeMeasures()
# open(args.input_krn,"w").writelines(rMeasures)
