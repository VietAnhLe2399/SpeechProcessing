import librosa
import numpy as np
import os
import math
from sklearn.cluster import KMeans
import hmmlearn.hmm
from hmmlearn.hmm import GaussianHMM
from hmmlearn.hmm import GMMHMM
import random
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
    mfcc = [get_mfcc(os.path.join(data_dir,f)) for f in files if f.endswith(".wav")]
    return mfcc

def clustering(X, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, n_init=50, random_state=0, verbose=0)
    kmeans.fit(X)
    print("centers", kmeans.cluster_centers_.shape)
    return kmeans

if __name__ == "__main__":
    class_names = ['tôi', 'nhà', 'học', 'nhân viên', 'hà nội']
    dataset = {}
    dataset_train = {}
    dataset_test = {}

    for cname in class_names:
        print(f"Load {cname} dataset")
        dataset[cname] = get_class_data(os.path.join("data", cname))
    #     uncomment to shuffle dataset
        random.shuffle(dataset[cname])
        train_size = int(0.8*len(dataset[cname]))
        dataset_train[cname] = dataset[cname][:train_size]
        dataset_test[cname] = dataset[cname][train_size:]

    # Get all vectors in the datasets
    all_vectors = np.concatenate([np.concatenate(v, axis=0) for k, v in dataset.items()], axis=0)
    # print("vectors", all_vectors.shape)
    # Run K-Means algorithm to get clusters
    # Comment KMEANS for GMMHMM
    # kmeans = clustering(all_vectors)
    # print("centers", kmeans.cluster_centers_.shape)

    models = {}
    for cname in class_names:
        class_vectors = dataset[cname]
    #     use Multinominal HMM
    #     dataset[cname] = list([kmeans.predict(v).reshape(-1,1) for v in dataset[cname]])
    #     hmm = hmmlearn.hmm.MultinomialHMM(
    #         n_components=20, random_state=0, n_iter=1000, verbose=True
    #     )

        hmm = GMMHMM(
        n_components=5, n_mix = 1, random_state=42, n_iter=1000, verbose=True,
            params='mctw',
            init_params='mc',
    #         startprob_prior = np.array([1.0,0.0,0.0,0.0,0.0]),
    #         transmat_prior = np.array([
    #             [0.7,0.3,0.0,0.0,0.0],
    #             [0.0,0.7,0.3,0.0,0.0],
    #             [0.0,0.0,0.7,0.3,0.0],
    #             [0.0,0.0,0.0,0.7,0.3],
    #             [0.0,0.0,0.0,0.0,1.0],
    #         ])
        )
        hmm.startprob_ = np.array([1.0,0.0,0.0,0.0,0.0])
    #     hmm.transmat_ = np.array([
    #         [0.7,0.3,0.0,0.0,0.0],
    #         [0.0,0.7,0.3,0.0,0.0],
    #         [0.0,0.0,0.7,0.3,0.0],
    #         [0.0,0.0,0.0,0.7,0.3],
    #         [0.0,0.0,0.0,0.0,1.0],
    #     ])

    #     uncomment below line to train with full dataset
    #     X = np.concatenate(dataset[cname])
    #     lengths = list([len(x) for x in dataset[cname]])
    #     hmm.fit(X, lengths=lengths)

        X = np.concatenate(dataset_train[cname])
        lengths = list([len(x) for x in dataset_train[cname]])
    #     FOR GMMHMM: NO NEED lengths parameter
        hmm.fit(X)
        models[cname] = hmm
    print("Training done")

    print("Testing")

    for true_cname in class_names:
        true_predict = 0
    #     for O in dataset[true_cname]:
        for O in dataset_test[true_cname]:
            score = {cname : model.score(O, [len(O)]) for cname, model in models.items()}
            predict = max(score, key=score.get)
            if predict == true_cname:
                true_predict += 1
    #         print(true_cname, score, predict)
        print(true_cname)
    #     change dataset_test to dataset to test in full dataset
        print(f'TRUE PREDICT: {true_predict}/{len(dataset_test[true_cname])}')
        print('ACCURACY:', true_predict/len(dataset_test[true_cname]))

    with open("models.pkl", "wb") as file:
        pickle.dump(models, file)
        print("Save model as models.pkl")