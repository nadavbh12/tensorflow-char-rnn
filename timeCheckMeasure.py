import jazz.checkMeasure
import time
import cProfile
import sample_jazz
import sys


# bar1 = '''ccc
# 8r
# 16a-
# 16cc'''
# bar2 = '''16dd
# 16ff
# [8gg
# 12gg]
# 12ee
# 12ff'''
# bar3='''16ff
# 16gg
# 16ee-
# 16b
# @
# 4.cc
# 8r
# 2r'''
# bar4='''32ddd-
# 32ccc
# 32aa
# 32bb-
# 32ccc
# 32ddd
# [16aa
# 8aa]
# 8gg'''
#
# bar5='''qff
# 8gg
# 4.bb-
# 2ccc'''
# start = time.time()
#
# for i in range(1, 100):
#     checkMeasure.get_measure_score(bar1,'Cmaj7')
#
# end = time.time()
# print(end - start)
# cProfile.run("for i in range(0, 100): checkMeasure.get_measure_score(bar1, 'Cmaj7')", None, 'cumulative')
cProfile.run("sample_jazz.main(sys.argv[1:])", None, 'cumulative')