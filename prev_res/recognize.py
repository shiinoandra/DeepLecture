# -*- coding: utf-8 -*-
import sugartensor as tf
import numpy as np
import librosa
from model import *
import data
import spell


__author__ = 'namju.kim@kakaobrain.com'


# set log level to debug
tf.sg_verbosity(1)

#
# hyper parameters
#

batch_size = 1     # batch size

#
# inputs
#

# vocabulary size
voca_size = data.voca_size

# mfcc feature of audio
x = tf.placeholder(dtype=tf.sg_floatx, shape=(batch_size, None, 20))

# sequence length except zero-padding
seq_len = tf.not_equal(x.sg_sum(axis=2), 0.).sg_int().sg_sum(axis=1)

# encode audio feature
logit = get_logit(x, voca_size=voca_size)

# ctc decoding
decoded, _ = tf.nn.ctc_beam_search_decoder(logit.sg_transpose(perm=[1, 0, 2]), seq_len, merge_repeated=False)

# to dense tensor
y = tf.sparse_to_dense(decoded[0].indices, decoded[0].dense_shape, decoded[0].values) + 1

#
# regcognize wave file
#

# command line argument for input wave file path
tf.sg_arg_def(file=('', 'speech wave file to recognize.'))


# load wave file
sampr = 16000
# wav, _ = librosa.load(tf.sg_arg().file, mono=True, sr=16000)
# get mfcc feature

sentences_noLM = []
sentences_LM = []
def do_recognize(wav):
    # wav, _ = librosa.load(filename, mono=True, sr=16000)
    for i in range(0,len(wav),(sampr*3)) :
        chunk = wav[i:i+(sampr*3)]
        mfcc = np.transpose(np.expand_dims(librosa.feature.mfcc(chunk, sampr), axis=0), [0, 2, 1])

        # run network
        with tf.Session() as sess:

            # init variables
            tf.sg_init(sess)

            # restore parameters
            saver = tf.train.Saver()
            saver.restore(sess, tf.train.latest_checkpoint('asset/train_orig'))
            # run session
            label = sess.run(y, feed_dict={x: mfcc})
            out_str = data.get_index(label)

            # print "without LM"
            # new_sentence = sentence.Sentence(time_label_start,int(time_label_start_remainder), time_label_end,int(time_label_end_remainder),sub_text)
            # print(out_str)
            # print "with LM"
            # print(spell.correction(out_str))

            return (out_str,spell.correction(out_str))
