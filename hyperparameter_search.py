import os
import json
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import train


def hyperopt_train_test_jazz(params):

    out_dir = 'outputs/num_layers' + str(int(params['num_layers'])) \
              + '_hidden_size' + str(int(params['hidden_size']))\
              + '_num_unrollings' + str(int(params['num_unrollings']))\
              + '_batch_size' + str(int(params['batch_size']))\
              + '_dropout' + str(float(params['dropout']))\
              + '_max_grad_norm' + str(float(params['max_grad_norm'])) \
              + '_learning_rate' + str(float(params['learning_rate']))
              # + '_decay_rate' + str(float(params['decay_rate'])) \
              # + '_model' + str(params['model']) \
              # + '_opt_algorithm' + str(params['opt_algorithm'])\


    args = ['--data_file=data/parker.txt',
            '--train_frac=0.9',
            '--num_epochs=10',
            '--save_best_only',
            '--num_layers='     + str(int(params['num_layers'])),
            '--hidden_size='    + str(int(params['hidden_size'])),
            '--num_unrollings=' + str(int(params['num_unrollings'])),
            '--batch_size='     + str(int(params['batch_size'])),
            '--dropout='        + str(float(params['dropout'])),
            '--max_grad_norm='  + str(float(params['max_grad_norm'])),
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
    'hidden_size': hp.choice('hidden_size',[128,256,512,1024]),
    'num_unrollings': hp.quniform('num_unrollings', 20, 2, 1),
    'batch_size': hp.quniform('batch_size', 5, 40, 1),
    'dropout': hp.uniform('dropout', 0, 1),
    'max_grad_norm': hp.uniform('max_grad_norm', 1.,10.),
    'learning_rate': hp.loguniform('learning_rate', -5, -3),
    # 'decay_rate': hp.uniform('decay_rate', 0.7, 0.99),
    # 'model': hp.choice('model', ['lstm', 'rnn', 'gru']),
    # 'opt_algorithm': hp.choice('opt_algorithm', ['adam', 'rmsprop']),
}

trials = Trials()
best = fmin(
    fn=hyperopt_train_test_jazz,
    space=spaceJazz,
    algo=tpe.suggest,
    max_evals=100,
    trials=trials
)

print 'Best: ', best

for trial in trials.trials:
    print trial
