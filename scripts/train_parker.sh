#!/bin/bash

python train.py \
       --data_file=data/parker.txt \
       --num_epochs=50 \
       --hidden_size=512 \
       --num_layers=3 \
       --batch_size=64 \
       --output_dir=parker_512_3

tensorboard --logdir=parker_512_3/tensorboard_log/ --port=6006
