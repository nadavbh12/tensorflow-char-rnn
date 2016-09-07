#!/bin/bash

OUT_FILE="samples/parker_sample.krn"

echo $PWD

python sample_jazz.py --init_dir=output --length=100 --temperature=1.5 > $OUT_FILE

#python scripts/postprocess.py --input_krn $OUT_FILE --header scripts/header_parker --trailer scripts/trailer_parker

#python scripts/displayXml.py --input_krn $OUT_FILE