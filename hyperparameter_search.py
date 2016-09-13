import os
import json
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import train
import pickle


def hyperopt_train_test_jazz(params):

    out_dir = 'outputs/num_layers' + str(int(params['num_layers'])) \
              + '_hidden_size' + str(int(params['hidden_size']))\
              + '_num_unrollings' + str(int(params['num_unrollings']))\
              + '_dropout' + str(float(params['dropout']))\
              + '_max_grad_norm' + str(float(params['max_grad_norm'])) \
              + '_learning_rate' + str(float(params['learning_rate']))
            # + '_batch_size' + str(int(params['batch_size']))\
            # + '_decay_rate' + str(float(params['decay_rate'])) \
            # + '_model' + str(params['model']) \
            # + '_opt_algorithm' + str(params['opt_algorithm'])\

    args = ['--data_file=data/parker.txt',
            '--train_frac=0.9',
            '--num_epochs=20',
            '--save_best_only',
            '--min_valid_ppl=1.7',
            '--num_layers='     + str(int(params['num_layers'])),
            '--hidden_size='    + str(int(params['hidden_size'])),
            '--num_unrollings=' + str(int(params['num_unrollings'])),
            '--dropout='        + str(float(params['dropout'])),
            '--max_grad_norm='  + str(float(params['max_grad_norm'])),
            # '--batch_size=' + str(int(params['batch_size'])),
            # '--decay_rate='     + str(float(params['decay_rate'])),
            # '--model='          + str(params['model']),
            # '--opt_algorithm='  + params['opt_algorithm'],
            '--learning_rate='  + str(float(params['learning_rate'])),
            '--output_dir='     + out_dir]

    clf = train.main(args)
    with open(os.path.join(out_dir, 'result.json'), 'r') as f:
        result = json.load(f)
    return result['best_valid_ppl']

spaceJazz = {
    'num_layers': hp.choice('num_layers',[2, 3]),
    'hidden_size': hp.choice('hidden_size',[128,256,512]),
    'num_unrollings': hp.quniform('num_unrollings', 20, 2, 1),
    # 'batch_size': hp.quniform('batch_size', 5, 40, 1),
    'dropout': hp.uniform('dropout', 0, 1),
    'max_grad_norm': hp.uniform('max_grad_norm', 1.,10.),
    'learning_rate': hp.uniform('learning_rate', 0.0001, 0.01),
    # 'decay_rate': hp.uniform('decay_rate', 0.7, 0.99),
    # 'model': hp.choice('model', ['lstm', 'rnn', 'gru']),
    # 'opt_algorithm': hp.choice('opt_algorithm', ['adam', 'rmsprop']),
}

# trials = Trials()
trials = pickle.load(open("trials.p", "rb"))
for i in range(14, 50) :
    best = fmin(
        fn=hyperopt_train_test_jazz,
        space=spaceJazz,
        algo=tpe.suggest,
        max_evals=i,
        trials=trials
    )
    print len(trials.results)
    print 'Best: ', best
    pickle.dump(trials, open("trials.p", "wb"))
    trials = pickle.load(open("trials.p", "rb"))

for trial in trials.trials:
    print trial
