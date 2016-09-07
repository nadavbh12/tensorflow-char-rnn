import argparse
import json
import os

from char_rnn_model import *
from jazz.checkMeasure import get_measure_score
from train import load_vocab


def main(args):
    parser = argparse.ArgumentParser()
    
    # Parameters for using saved best models.
    parser.add_argument('--init_dir', type=str, default='',
                        help='continue from the outputs in the given directory')

    # Parameters for sampling.
    parser.add_argument('--temperature', type=float,
                        default=1.0,
                        help=('Temperature for sampling from softmax: '
                              'higher temperature, more random; '
                              'lower temperature, more greedy.'))
    
    parser.add_argument('--max_prob', dest='max_prob', action='store_true',
                        help='always pick the most probable next character in sampling')

    parser.set_defaults(max_prob=False)
    
    parser.add_argument('--start_text', type=str,
                        default='',
                        help='the text to start with')

    parser.add_argument('--chords_file', type=str, default='chords/12_bar_blues_twice.txt',
            help='File containing the bar progression')

    parser.add_argument('--seed', type=int,
                        default=-1,
                        help=('seed for sampling to replicate results, '
                              'an integer between 0 and 4294967295.'))

    # Parameters for evaluation (computing perplexity of given text).
    parser.add_argument('--evaluate', dest='evaluate', action='store_true',
                        help='compute the perplexity of given text')
    parser.set_defaults(evaluate=False)
    parser.add_argument('--example_text', type=str,
                        default='The meaning of life is 42.',
                        help='compute the perplexity of given example text.')

    # Parameters for debugging.
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='show debug information')
    parser.set_defaults(debug=False)
    
    args = parser.parse_args(args)

    # Prepare parameters.
    with open(os.path.join(args.init_dir, 'result.json'), 'r') as f:
        result = json.load(f)
    params = result['params']
    best_model = result['best_model']
    best_valid_ppl = result['best_valid_ppl']
    if 'encoding' in result:
        args.encoding = result['encoding']
    else:
        args.encoding = 'utf-8'
    args.vocab_file = os.path.join(args.init_dir, 'vocab.json')
    vocab_index_dict, index_vocab_dict, vocab_size = load_vocab(args.vocab_file, args.encoding)

    # Create graphs
    logging.info('Creating graph')
    graph = tf.Graph()
    with graph.as_default():
        with tf.name_scope('evaluation'):
            test_model = CharRNN(is_training=False, use_batch=False, **params)
            saver = tf.train.Saver(name='checkpoint_saver')


    # Read Chords
    f = file(args.chords_file, 'r')
    chords_strings = f.read().split(' ')

    if args.seed >= 0:
        np.random.seed(args.seed)
    # Sampling a sequence
    sample=args.start_text
    num_chords = 10
    with tf.Session(graph=graph) as session:
        for c in chords_strings:
            bars = [None] * num_chords
            bar_scores = [None] * num_chords

            saver.restore(session, best_model)
            for i in range(num_chords):
                bar = test_model.sample_bar(session, sample,
                                                vocab_index_dict, index_vocab_dict,
                                                temperature=args.temperature,
                                                max_prob=args.max_prob)
                bars[i] = bar.split('@')[-2]
                try:
                    bar_score = get_measure_score(bars[i], c)
                except:
                    continue
                bar_scores[i] = bar_score
                # print "bar_score= " + str(bar_score)

                best_bar = bars[np.argmax(bar_scores)]
            sample += best_bar + '@'

    print(sample)
    return sample

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
