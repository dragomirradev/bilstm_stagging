from __future__ import print_function
import numpy as np
import time
import pickle
import tensorflow as tf
import os
import sys
from utils.stagging_model import Stagging_Model

        
def run_model(opts, loader = None, epoch=0):
    g = tf.Graph()
    with g.as_default():
        model = Stagging_Model(opts)
        saver = tf.train.Saver(max_to_keep=1)
        with tf.Session() as session: 
            session.run(tf.global_variables_initializer())
            best_accuracy = 0.0
            bad_times = 0
            for i in xrange(opts.max_epochs):
                print('Epoch {}'.format(i+1))
                loss, accuracy = model.run_epoch(session)
                test_accuracy = model.run_epoch(session, True)
                print('test accuracy {}'.format(test_accuracy))
                if best_accuracy < test_accuracy:
                    best_accuracy = test_accuracy 
                    #saving_file = os.path.join(opts.model_dir, 'epoch{0}_accuracy{1:.5f}'.format(i+1, test_accuracy))
                    saving_file = os.path.join(opts.model_dir, 'best_model')
                    print('saving it to {}'.format(saving_file))
                    saver.save(session, saving_file)
                    bad_times = 0
                    checkpoint_file = os.path.join(opts.base_dir, 'checkpoint.txt')
                    with open(checkpoint_file, 'wt') as fwrite:
                        fwrite.write(' '.join([saving_file, 'epoch{}'.format(i+1), 'accuracy{}'.format(test_accuracy)]))
                        fwrite.write('\n')
                    print('test accuracy improving')
                else:
                    bad_times += 1
                    print('test accuracy deteriorating')
                if bad_times >= opts.early_stopping:
                    print('did not improve {} times in a row. stopping early'.format(bad_times))
                    #if saving_dir:
                    #    print('outputting test pred')
                    #    with open(os.path.join(saving_dir, 'predictions_test.pkl'), 'wb') as fhand:
                    #        pickle.dump(predictions, fhand)
#                    print(saving_file)
                    break
                
def run_model_test(opts, test_opts):
    g = tf.Graph()
    with g.as_default():
        model = Stagging_Model(opts, test_opts)
        saver = tf.train.Saver(max_to_keep=1)
        with tf.Session() as session: 
            session.run(tf.global_variables_initializer())
            saver.restore(session, test_opts.modelname)
            test_accuracy = model.run_epoch(session, True)
            if test_opts.get_accuracy:
                print('\nTest accuracy {}'.format(test_accuracy))
