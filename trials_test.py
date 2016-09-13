import os
import json
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials, trials_from_docs
from hyperopt import rand

spaceJazz = {
    'num_layers': hp.choice('num_layers',[2, 3]),
    'hidden_size': hp.choice('hidden_size',[128,256,512]),
    'num_unrollings': hp.quniform('num_unrollings', 20, 2, 1),
    'batch_size': hp.quniform('batch_size', 5, 40, 1),
    'dropout': hp.uniform('dropout', 0, 1),
    'max_grad_norm': hp.uniform('max_grad_norm', 1.,10.),
    'learning_rate': hp.loguniform('learning_rate', -5, -4),
    # 'decay_rate': hp.uniform('decay_rate', 0.7, 0.99),
    # 'model': hp.choice('model', ['lstm', 'rnn', 'gru']),
    # 'opt_algorithm': hp.choice('opt_algorithm', ['adam', 'rmsprop']),
}


# @domain_constructor()
# def coin_flip():
#     """ Possibly the simplest possible Bandit implementation
#     """
#     return {'loss': hp.choice('flip', [0.0, 1.0]), 'status': base.STATUS_OK}
docs = []
bob = trials_from_docs(docs, {'misc': {'tid': 0},'state': 2, 'tid':0,'result':{'status': 'ok','loss': 2.06412363052},\
                              'loss': 2.06412363052, 'status': STATUS_OK, 'vals':{'num_layers':2, 'hidden_size':256, 'num_unrollings':7, 'batch_size':20, 'dropout':0.719468969786, 'max_grad_norm':4.85623833568, 'learning_rate':0.0134454415987}})

print bob.trials