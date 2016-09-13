#!/bin/bash

OUT_FILE="samples/parker_sample.krn"

echo $PWD

python sample_jazz.py --init_dir=outputs/best  --temperature=1.5 > $OUT_FILE

#python jazz/postprocess.py --input_krn $OUT_FILE --header scripts/header_parker --trailer scripts/trailer_parker
#
#python jazz/displayXml.py --input_krn $OUT_FILE