import librosa
import numpy as np
import os
import argparse
import math
from sklearn.cluster import KMeans
import hmmlearn.hmm
import pickle

def get_mfcc(file_path):
    y, sr = librosa.load(file_path) # read .wav file
    hop_length = math.floor(sr*0.010) # 10ms hop
    win_length = math.floor(sr*0.025) # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    # substract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1,1)) 
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0) # O^r
    # return T x 36 (transpose of X)
    return X.T # hmmlearn use T x N matrix

def get_class_data(data_dir):
    files = os.listdir(data_dir)
    mfcc = [get_mfcc(os.path.join(data_dir,f)) for f in files if f.endswith(".wav") and not f.endswith("_bad.wav")]
    return mfcc

def clustering(X, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, n_init=50, random_state=0, verbose=0)
    kmeans.fit(X)
    print("centers", kmeans.cluster_centers_.shape)
    return kmeans

def predict():
    class1 = ["toi", "test_toi"]
    class2 = ["mot", "test_mot"]
    class3 = ["trong", "test_trong"]
    class4 = ["thoigian", "test_thoigian"]
    class5 = ["chungta", "test_chungta"]
    classdemo = ["demo"]

    class_names = []
    # class_names.extend(class1)
    # class_names.extend(class2)
    # class_names.extend(class3)
    # class_names.extend(class4)
    # class_names.extend(class5)
    class_names.extend(classdemo)

    dataset = {}
    for cname in class_names:
        print(f"Load {cname} dataset")
        dataset[cname] = get_class_data(os.path.join("data", cname))

    # Get all vectors in the datasets
    all_vectors = np.concatenate([np.concatenate(v, axis=0) for k, v in dataset.items()], axis=0)
    print("vectors", all_vectors.shape)
    # Run K-Means algorithm to get clusters
    kmeans = clustering(all_vectors)
    print("centers", kmeans.cluster_centers_.shape)


    config = {
        'toi': {'n_components':5},
        'mot': {'n_components': 5},
        'trong': {'n_components': 7},
        'thoigian': {'n_components': 10},
        'chungta': {'n_components': 8},
        'test_toi': {'n_components': 5},
        'test_mot': {'n_components': 5},
        'test_trong': {'n_components': 7},
        'test_thoigian': {'n_components': 10},
        'test_chungta': {'n_components': 8},
        'demo': {'n_components': 1},
    }

    '''

    models = {}
    for cname in class_names:
        class_vectors = dataset[cname]
        # convert all vectors to the cluster index
        # dataset['one'] = [O^1, ... O^R]
        # O^r = (c1, c2, ... ct, ... cT)
        # O^r size T x 1
        dataset[cname] = list([kmeans.predict(v).reshape(-1,1) for v in dataset[cname]])
        n_components = config[cname]['n_components']
        hmm = hmmlearn.hmm.MultinomialHMM(
            n_components=n_components, random_state=0, n_iter=1000, verbose=True,
        )
        start_prob = np.zeros(n_components)
        start_prob[0] = 1.0
        hmm.startprob_ = start_prob

        if cname[:4] != 'test':
            X = np.concatenate(dataset[cname])
            lengths = list([len(x) for x in dataset[cname]])
            print("training class", cname)
    #         print(X.shape, lengths, len(lengths))
            hmm.fit(X, lengths=lengths)
            models[cname] = hmm
    print("Training done")
    model_filename = 'finalized_model.pkl'
    with open (model_filename, 'wb') as f:
        pickle.dump(models, f)

    '''


    model_filename = 'finalized_model.pkl'
    with open(model_filename, 'rb') as f:
        models = pickle.load(f)
    print((models))

    print("Testing")
    for true_cname in class_names:
        if true_cname == 'demo':
        # count = 0
            for O in dataset[true_cname]:
                score = {cname : model.score(O, [len(O)]) for cname, model in models.items() if cname[:4] != 'test' and cname != 'demo' }
                predict = max(score, key = score.get)
            return predict
        #     if predict == true_cname or true_cname[:4] == 'test' and predict == true_cname.split('_')[1]:
        #         count+=1
        #     print(true_cname, score, predict)
        # print(f"true: {count}/{len(dataset[true_cname])}")