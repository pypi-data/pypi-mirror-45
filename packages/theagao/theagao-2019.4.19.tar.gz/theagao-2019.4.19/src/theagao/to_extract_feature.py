# coding=utf-8
# Author: Yongwei
# @Time: 19-4-19 下午3:42

from librosa import load, stft, feature, cqt
import numpy as np


def load_wav(filepath, sr=44100):
    '''
    load wav file with sample size of 44100
    :param filepath: the path of wav file
    :param sr: sample rate wanted
    :return: wave and sample rate
    '''
    y, sr = load(filepath, sr=sr)
    return y, sr


def fenture_stft(y, win_length=1024, hop_length=512, n_fft=1024, abs=True):
    '''
    extract stft
    :param y: wave loaded
    :param win_length: window size of one frame
    :param hop_length: hop size
    :param n_fft: window size of fft
    :param abs: True means that you want to get the energy spectrum
    :return: stft feature
    '''
    Spec = stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    if abs == True:
       Spec = np.abs(Spec)
    Spec = Spec.astype(np.float32)
    return Spec


def fenture_mfcc(y, sr=44100, n_mfcc=13, hop_length=512, n_fft=1024):
    '''
    extract mfcc
    :param y: wave loaded
    :param hop_length: hop size
    :param n_fft: window size of fft
    :return: mfcc feature
    '''
    Spec = feature.mfcc(y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    return Spec


def feature_cqt(y, sr=44100, hop_length=512, fmin=55.0, n_bins=300, bins_per_octave=60):
    '''
    extract cqt
    :param y: wave loaded
    :param sr: sample rate
    :return: cqt feature
    '''
    Spec = cqt(y, sr=sr, hop_length=hop_length, fmin=fmin, n_bins=n_bins, bins_per_octave=bins_per_octave)
    return Spec





