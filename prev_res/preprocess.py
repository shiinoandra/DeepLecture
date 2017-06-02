import numpy as np
import pandas as pd
import glob
import csv
import librosa
import scikits.audiolab
import data
import os


__author__ = 'namju.kim@kakaobrain.com'


# data path
_data_path = "asset/data/"


#
# process VCTK corpus
#

def process_vctk(csv_file):

    # create csv writer
    writer = csv.writer(csv_file, delimiter=',')

    # read label-info
    df = pd.read_table(_data_path + 'VCTK-Corpus/speaker-info.txt', usecols=['ID'],
                       index_col=False, delim_whitespace=True)

    # read file IDs
    file_ids = []
    for d in [_data_path + 'VCTK-Corpus/txt/p%d/' % uid for uid in df.ID.values]:
        file_ids.extend([f[-12:-4] for f in sorted(glob.glob(d + '*.txt'))])

    for i, f in enumerate(file_ids):

        # wave file name
        wave_file = _data_path + 'VCTK-Corpus/wav48/%s/' % f[:4] + f + '.wav'

        # print info
        print("VCTK corpus preprocessing (%d / %d) - '%s']" % (i, len(file_ids), wave_file))

        # load wave file
        wave, sr = librosa.load(wave_file, mono=True, sr=None)

        # re-sample ( 48K -> 16K )
        wave = wave[::3]

        # get mfcc feature
        mfcc = librosa.feature.mfcc(wave, sr=16000)

        # get label index
        label = data.str2index(open(_data_path + 'VCTK-Corpus/txt/%s/' % f[:4] + f + '.txt').read())

        # save result ( exclude small mfcc data to prevent ctc loss )
        if len(label) < mfcc.shape[1]:
            # filename
            fn = wave_file.split('/')[-1]

            # save meta info
            writer.writerow([fn] + label)

            # save mfcc
            np.save('asset/data/preprocess/mfcc/' + fn + '.npy', mfcc, allow_pickle=False)


#
# process LibriSpeech corpus
#

def process_libri(csv_file, category):

    parent_path = _data_path + 'LibriSpeech/' + category + '/'
    labels, wave_files = [], []

    # create csv writer
    writer = csv.writer(csv_file, delimiter=',')

    # read directory list by speaker
    speaker_list = glob.glob(parent_path + '*')
    for spk in speaker_list:

        # read directory list by chapter
        chapter_list = glob.glob(spk + '/*/')
        for chap in chapter_list:

            # read label text file list
            txt_list = glob.glob(chap + '/*.txt')
            for txt in txt_list:
                with open(txt, 'rt') as f:
                    records = f.readlines()
                    for record in records:
                        # parsing record
                        field = record.split('-')  # split by '-'
                        speaker = field[0]
                        chapter = field[1]
                        field = field[2].split()  # split field[2] by ' '
                        utterance = field[0]  # first column is utterance id

                        # wave file name
                        wave_file = parent_path + '%s/%s/%s-%s-%s.flac' % \
                                                  (speaker, chapter, speaker, chapter, utterance)
                        wave_files.append(wave_file)

                        # label index
                        labels.append(data.str2index(' '.join(field[1:])))  # last column is text label

    # save results
    for i, (wave_file, label) in enumerate(zip(wave_files, labels)):

        # print info
        print("LibriSpeech corpus preprocessing (%d / %d) - '%s']" % (i, len(wave_files), wave_file))

        # load flac file
        wave, sr, _ = scikits.audiolab.flacread(wave_file)

        # get mfcc feature
        mfcc = librosa.feature.mfcc(wave, sr=16000)

        # save result ( exclude small mfcc data to prevent ctc loss )
        if len(label) < mfcc.shape[1]:
            # filename
            fn = wave_file.split('/')[-1]

            # save meta info
            writer.writerow([fn] + label)

            # save mfcc
            np.save('asset/data/preprocess/mfcc/' + fn + '.npy', mfcc, allow_pickle=False)


#
# process TEDLIUM corpus
#

def process_ted(csv_file, category):

    parent_path = _data_path + 'TEDLIUM_release2/' + category + '/'
    labels, wave_files, offsets, durs = [], [], [], []

    # create csv writer
    writer = csv.writer(csv_file, delimiter=',')

    # read STM file list
    stm_list = glob.glob(parent_path + 'stm/*')
    for stm in stm_list:
        with open(stm, 'rt') as f:
            records = f.readlines()
            for record in records:
                field = record.split()

                # wave file name
                wave_file = parent_path + 'sph/%s.sph.wav' % field[0]
                wave_files.append(wave_file)

                # label index
                labels.append(data.str2index(' '.join(field[6:])))

                # start, end info
                start, end = float(field[3]), float(field[4])
                offsets.append(start)
                durs.append(end - start)

    # save results
    for i, (wave_file, label, offset, dur) in enumerate(zip(wave_files, labels, offsets, durs)):

        # print info
        print("TEDLIUM corpus preprocessing (%d / %d) - '%s-%.2f]" % (i, len(wave_files), wave_file, offset))

        # load wave file
        wave, sr = librosa.load(wave_file, mono=True, sr=None, offset=offset, duration=dur)

        # get mfcc feature
        mfcc = librosa.feature.mfcc(wave, sr=16000)

        # save result ( exclude small mfcc data to prevent ctc loss )
        if len(label) < mfcc.shape[1]:
            # filename
            fn = "%s-%.2f" % (wave_file.split('/')[-1], offset)

            # save meta info
            writer.writerow([fn] + label)

            # save mfcc
            np.save('asset/data/preprocess/mfcc/' + fn + '.npy', mfcc, allow_pickle=False)



#proces webLecture corpus
def process_weblecture(csv_file):
    # create csv writer
    writer = csv.writer(csv_file, delimiter=',')

    file_ids = []
    ids = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
    for d in [_data_path + 'webLecture/' + 'txt/l%s/' % uid for uid in ids]:
        # print d.split("/")[len(d.split("/"))-2]
        file_ids.extend([f.split("/")[len(f.split("/"))-1].split(".")[0] for f in sorted(glob.glob(d + '*.txt'))])

    for i, f in enumerate(file_ids):



        # wave file name
        wave_file = _data_path + 'webLecture/'  + 'wav48/%s/' % f.split("-")[0] + f + '.wav'

        if os.stat(wave_file).st_size > 88200:  # at least 2 seconds


            # print info
            print("weblecture corpus preprocessing (%d / %d) - '%s']" % (i, len(file_ids), wave_file))

            # load wave file
            wave, sr = librosa.load(wave_file, mono=True, sr=None)

            # re-sample ( 48K -> 16K )
            wave = wave[::3]

            # get mfcc feature
            mfcc = librosa.feature.mfcc(wave, sr=14700)

            # get label index
            label = data.str2index(open(_data_path + 'webLecture/' + '/txt/%s/' % f.split("-")[0] + f + '.txt').read())

            # save result ( exclude small mfcc data to prevent ctc loss )
            if len(label) < mfcc.shape[1]:
                # filename
                fn = wave_file.split('/')[-1]

                # save meta info
                writer.writerow([fn] + label)

                # save mfcc
                np.save('asset/data/preprocess/mfcc/' + fn + '.npy', mfcc, allow_pickle=False)


#
# Create directories
#
if not os.path.exists('asset/data/preprocess'):
    os.makedirs('asset/data/preprocess')
if not os.path.exists('asset/data/preprocess/meta'):
    os.makedirs('asset/data/preprocess/meta')
if not os.path.exists('asset/data/preprocess/mfcc'):
    os.makedirs('asset/data/preprocess/mfcc')


#
# Run pre-processing for training
#

# # VCTK corpus
# csv_f = open('asset/data/preprocess/meta/train.csv', 'w')
# process_vctk(csv_f)
# csv_f.close()
#
# # LibriSpeech corpus for train
# csv_f = open('asset/data/preprocess/meta/train.csv', 'a+')
# process_libri(csv_f, 'train-clean-360')
# csv_f.close()
#
# # TEDLIUM corpus for train
# csv_f = open('asset/data/preprocess/meta/train.csv', 'a+')
# process_ted(csv_f, 'train')
# csv_f.close()

# weblecture corpus for train
csv_f = open('asset/data/preprocess/meta/train.csv', 'a+')
process_weblecture(csv_f)
csv_f.close()

#
# Run pre-processing for validation
#

# # LibriSpeech corpus for valid
# csv_f = open('asset/data/preprocess/meta/valid.csv', 'w')
# process_libri(csv_f, 'dev-clean')
# csv_f.close()
#
# # TEDLIUM corpus for valid
# csv_f = open('asset/data/preprocess/meta/valid.csv', 'a+')
# process_ted(csv_f, 'dev')
# csv_f.close()
#
# #
# # Run pre-processing for testing
# #
#
# # LibriSpeech corpus for test
# csv_f = open('asset/data/preprocess/meta/test.csv', 'w')
# process_libri(csv_f, 'test-clean')
# csv_f.close()
#
# # TEDLIUM corpus for test
# csv_f = open('asset/data/preprocess/meta/test.csv', 'a+')
# process_ted(csv_f, 'test')
# csv_f.close()
