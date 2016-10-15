import glob
import argparse
import re
import os
import subprocess
import codecs

REP="@\n"


vocab = {'aa'   : unichr(0x87),
         'aaa'  : unichr(0x88),
         'aaaa' : unichr(0x89),
         'bb'   : unichr(0x8a),
         'bbb'  : unichr(0x8b),
         'bbbb' : unichr(0x8c),
         'cc'   : unichr(0x8d),
         'ccc'  : unichr(0x8e),
         'cccc' : unichr(0x8f),
         'dd'   : unichr(0x90),
         'ddd'  : unichr(0x91),
         'dddd' : unichr(0x92),
         'ee'   : unichr(0x93),
         'eee'  : unichr(0x94),
         'eeee' : unichr(0x95),
         'ff'   : unichr(0x96),
         'fff'  : unichr(0x97),
         'ffff' : unichr(0x98),
         'gg'   : unichr(0x99),
         'ggg'  : unichr(0x9a),
         'gggg' : unichr(0x9b),
         '12'   : unichr(0x9c),
         '16'   : unichr(0x9d),
         '20'   : unichr(0x9e),
         '24'   : unichr(0x9f),
         '28'   : unichr(0x9f),
         '32'   : unichr(0xa0),
         '36'   : unichr(0xa0),
         '40'   : unichr(0xa1),
         '48'   : unichr(0xa2),
         '64'   : unichr(0xa3),
         '72'   : unichr(0xa4),
         '96'   : unichr(0xa5),
         '128'  : unichr(0xa6),
         '0.055664': '32',
         '0.083008': '36',
         '0.083984': '36',
         '0.099609': '16',
         '0.100586': '16',
         '0.142578': '28',
         '0.143555': '28',
         '0.166016': '24',
         '0.166992': '24',
         '0.199219': '20',
         '0.200195': '20',
         '0.333008': '12',
         '0.333984': '12',
         }

reverse_vocab = { unichr(0x87) : 'aa'  ,
                  unichr(0x88) : 'aaa' ,
                  unichr(0x89) : 'aaaa',
                  unichr(0x8a) : 'bb'  ,
                  unichr(0x8b) : 'bbb' ,
                  unichr(0x8c) : 'bbbb',
                  unichr(0x8d) : 'cc'  ,
                  unichr(0x8e) : 'ccc' ,
                  unichr(0x8f) : 'cccc',
                  unichr(0x90) : 'dd'  ,
                  unichr(0x91) : 'ddd' ,
                  unichr(0x92) : 'dddd',
                  unichr(0x93) : 'ee'  ,
                  unichr(0x94) : 'eee' ,
                  unichr(0x95) : 'eeee',
                  unichr(0x96) : 'ff'  ,
                  unichr(0x97) : 'fff' ,
                  unichr(0x98) : 'ffff',
                  unichr(0x99) : 'gg'  ,
                  unichr(0x9a) : 'ggg' ,
                  unichr(0x9b) : 'gggg',
                  unichr(0x9c) : '12'  ,
                  unichr(0x9d) : '16'  ,
                  unichr(0x9e) : '20'  ,
                  unichr(0x9f) : '24'  ,
                  unichr(0x9f) : '28'  ,
                  unichr(0xa0) : '32'  ,
                  unichr(0xa0) : '36'  ,
                  unichr(0xa1) : '40'  ,
                  unichr(0xa2) : '48'  ,
                  unichr(0xa3) : '64'  ,
                  unichr(0xa4) : '72'  ,
                  unichr(0xa5) : '96'  ,
                  unichr(0xa6) : '128' ,
                  }

def removeHeader(lines):
    found_first = False
    j = 0
    for i in range(len(lines)):
        j = i
        if not lines[i].startswith("*") and found_first == True:
            break
        if lines[i].startswith("="):
            found_first = True
    return lines[j:]
        
def removeTrailer(lines):
    for i in range(len(lines)-1, -1, -1):
        if lines[i].startswith("=="):
            break
    return lines[:i]

def removeBreakLines(lines):
    i = 0
    for i in range(len(lines)):
#         print lines[i]
        if lines[i].startswith('='):
            continue
        if not lines[i].startswith('1r'):
            break
    return lines[max(i-1,0):]

def removeMiddleBreakLines(lines):
    i = 0
    maxLines = 0
    for i in range(len(lines)):
        if lines[i].startswith('='):
            continue
        if lines[i].startswith('1r'):
            maxLines += 1
        elif maxLines > 3:
            lines[:] = lines[1:(i-maxLines*2)] + lines[i:]
            break
        else:
            maxLines = 0

    return lines


def removeBeamChars(line):
    line = line.replace('L','')
    line = line.replace('/','')
    line = line.replace('\\','')
    line = line.replace('J','')
    line = line.replace('k','')
    line = line.replace('K','')
    line = line.replace('K','')
    return line

def removeOdeCharacters(line):
    line = line.replace(';','')
    line = line.replace('_','')
    line = line.replace('[','')
    line = line.replace(']','')
    line = line.replace('i','')
    line = line.replace('l','')
    line = line.replace('y','')
    line = line.replace('m','')
    line = line.replace('M','')
    line = line.replace('Q','')
    line = line.replace('t','')

    return line


def convertVocabulary(line):
    # for token in reversed(sorted(vocab.keys())):
    for token in reversed(sorted(vocab.items(), key=lambda x: x[1])):
        if token[0] in line:
            line = line.replace(token[0],vocab[token[0]])
    return line

def removeDoubleSpine(line):
    index = line.find('\t')
    line = line[0:index] + '\n'
    return line


keys = ["P1", "m2", "M2", "m3", "M3", "P4", "A4", "P5", "m6", "M6", "m7", "M7"]
dynamIndices = {}

comp_txt = codecs.open("parker" + ".txt","w", encoding='latin_1')
##    ll = glob.glob(dir + "/ana-music/corpus/{composer}/*.krn".format(composer=composer))
ll = glob.glob("/home/nadav/Jazz/torch-rnn/music/parker_krn/*.krn")

for key in keys:
# for key in ["P1"]:
    for song in ll:
        # song = "/home/nadav/Jazz/torch-rnn/music/ana-music/corpus/parker/Dont_Blame_Me_Charlie_Parker_Complete_Dial_Sessions.krn"
        cmd = "transpose -t %s %s > /tmp/%s" % (key, song, key)
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
#             print "program output:", out
        lines = open("/tmp/" + key,"r").readlines()

        out = []
        lines = removeHeader(lines)
        lines = removeTrailer(lines)
        lines = removeBreakLines(lines)
        lines = removeBreakLines(list(reversed(lines)))
        lines = list(reversed(lines))
        lines = removeMiddleBreakLines(lines)
        lines = removeMiddleBreakLines(lines)
        lines = removeMiddleBreakLines(lines)
        # lines = removeMiddleBreakLines(lines)

        found_first = False
        i = 0
        # numRs = 0
        for l in lines:
            i += 1
            # if args.meter == 4:
            # ## take only pieces with meter of 4/4
            #     if l.startswith("*M3") or l.startswith("*M6"):
            #            break
            # elif args.meter == 3:
            # ## take only pieces with meter of 3/4
            #     if l.startswith("*M2") or l.startswith("*M4"):
            #             break

            if l.startswith("="):
                ## new measure, replace the measure with the @ sign, not part of humdrum
                out.append(REP)
                continue
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

            l = removeBeamChars(l)
            l = removeDoubleSpine(l)
            l = removeOdeCharacters(l)
            # if '1r' in l:
            #     numRs += 1
            # if numRs > 20:
            #     print song
            #     numRs = 0
            l = convertVocabulary(l)

            out.append(l)

        comp_txt.writelines(out)
        # comp_txt.flush()
        # break
comp_txt.close()
