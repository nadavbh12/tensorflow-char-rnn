import argparse
import json
import os

from char_rnn_model import *
from jazz.checkMeasure import get_measure_score3
from jazz.checkMeasure import replaceVocab
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
    parser.add_argument('--bar_temperature', type=float,
                        default=1.0,
                        help=('Temperature for sampling from softmax of bar generation'))

    parser.add_argument('--max_prob', dest='max_prob', action='store_true',
                        help='always pick the most probable next character in sampling')

    parser.set_defaults(max_prob=False)
    
    parser.add_argument('--start_text', type=str,
                        default='',
                        help='the text to start with')

    parser.add_argument('--chords_file', type=str, default='chords/12_bar_blues.txt',
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
    sample_processed = replaceVocab(sample)
    num_chords = 10
    with tf.Session(graph=graph) as session:
        for c in chords_strings:
            bars = [None] * num_chords
            bars_proccessed = [None] * num_chords
            bar_scores = [None] * num_chords

            saver.restore(session, best_model)
            for i in range(num_chords):
                bar = test_model.sample_bar(session, sample,
                                                vocab_index_dict, index_vocab_dict,
                                                temperature=args.temperature,
                                                max_prob=args.max_prob)
                bars[i] = bar.split('@')[-2]
                bars_proccessed[i] = replaceVocab(bars[i])
                try:
                    if ',' in c:
                        cs = c.split(',')
                        bar_score = get_measure_score3(bars_proccessed[i], cs[0], cs[1])
                    else:
                        bar_score = get_measure_score3(bars_proccessed[i], c, c)
                except:
                    bar_scores[i] = 0
                    continue

                bar_scores[i] = bar_score

            unnormalized_probs = np.multiply(np.sign(bar_scores), np.exp((bar_scores - np.max(bar_scores)) / args.bar_temperature))
            probs = unnormalized_probs / np.sum(unnormalized_probs)
            best_bar_idx = np.random.choice(probs.size, 1, p=probs)
            best_bar = bars[best_bar_idx[0]]
            best_bar_proccessed = bars_proccessed[best_bar_idx[0]]
            sample += best_bar + '@'
            sample_processed += best_bar_proccessed + '@'

    print(sample_processed)
    return sample_processed

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
