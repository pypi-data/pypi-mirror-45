import pickle
import zlib

import numpy as np
import plotly.graph_objs as go
from plotly import tools
from scipy.constants import c
from scipy.signal import welch


def lamb2freq(lam):
    '''

    :param lam: wavelength [m]
    :return: frequence [Hz]
    '''
    return c / lam


def freq2lamb(freq):
    '''

    :param freq: frequence [Hz]
    :return: lambda:[m]
    '''
    return c / freq


def downsample(signal, sps):
    '''
    downsample along row

    can receive siganl object or ndarray
    :param signal: Signal Object or ndarray
    :param sps:
    :return: signal
    '''
    if not isinstance(signal, np.ndarray):
        sample = signal.data_sample_in_fiber
        after_process = np.zeros_like(signal.symbol)

    else:
        sample = np.atleast_2d(signal)
        length = divmod(sample.shape[1], sps)

        if length[1] != 0:
            raise ("after downsample the sample number should be integer")
        after_process = np.zeros((sample.shape[0], length[0]), dtype=sample.dtype)

    for i in range(sample.shape[0]):
        after_process[i, :] = sample[i, ::sps]

    return after_process


def scatterplot_colorful(signal, down_sample=True):
    pass


def scatterplot(signal, down_sample=True, backend='mplt', visdom_env="scatterplot", server='http://localhost',
                port=8097):
    '''

    :param signal:      signal object or ndarray
    :param down_sample: if down_sample is true , signal must be signal object
    :param backend:     can choose mplt or pyqt
    :return:
    '''

    if down_sample:
        assert hasattr(signal, 'sps_in_fiber')
        symbol = downsample(signal, signal.sps_in_fiber)

    else:
        if hasattr(signal, 'decision_symbol'):
            symbol = signal.decision_symbol

        else:
            symbol = signal

    pol_number = signal.shape[0]
    if backend == 'mplt':
        import matplotlib.pyplot as plt
        plt.figure(figsize=(20, 6))
        for i in range(pol_number):
            plt.subplot(1, pol_number, i + 1)
            ibranch = symbol[i, :].real
            qbranch = symbol[i, :].imag
            plt.scatter(ibranch, qbranch, marker='o', color='b')
        plt.show()

    if backend == 'visdom':
        import visdom
        viz = visdom.Visdom(env=visdom_env, server=server, port=port)
        traces = []
        for i in range(pol_number):
            trace = go.Scattergl(x=symbol[i, :].real, y=symbol[i, :].imag, mode='markers')
            traces.append(trace)
        fig = tools.make_subplots(rows=1, cols=pol_number, print_grid=False)

        for index, trace in enumerate(traces):
            fig.append_trace(trace, 1, index + 1)
        fig['layout'].update(height=600, width=800)
        for i in range(pol_number):
            fig['layout'][f'xaxis{i + 1}'].update(title='I-Branch')
            fig['layout'][f'yaxis{i + 1}'].update(title='Q-Branch')
        viz.plotlyplot(fig)


def spectrum_analyzer(signal, fs=None, backend='mplt', visdom_env='spectrum', server='http://localhost',
                      port=8097):
    '''

    :param signal: signal object or ndarray
    :return: None
    '''

    if isinstance(signal, np.ndarray):
        assert fs is not None
        sample = signal
    else:
        fs = signal.fs_in_fiber

        sample = signal[:]

    pol_number = sample.shape[0]
    if backend == 'mplt':
        import matplotlib.pyplot as plt
        plt.figure(figsize=(20, 6))
        for i in range(pol_number):
            plt.subplot(1, pol_number, i + 1)
            [f, pxx] = welch(sample[i, :], fs, nfft=2048, detrend=False, return_onesided=False)
            plt.plot(f / 1e9, 10 * np.log10(np.abs(pxx)))
            plt.xlabel('Frequency [GHZ]')
            plt.ylabel('Power Spectrem Density [db/Hz]')
        plt.show()
    if backend == 'visdom':
        import visdom
        viz = visdom.Visdom(env=visdom_env, server=server, port=port)
        traces = []

        for i in range(pol_number):
            [f, pxx] = welch(sample[i, :], fs, nfft=2048, detrend=False, return_onesided=False)
            trace = go.Scattergl(x=f, y=10*np.log10(np.abs(pxx)), mode='lines',)
            traces.append(trace)
        fig = tools.make_subplots(rows=1, cols=pol_number, print_grid=False)

        for index, trace in enumerate(traces):
            fig.append_trace(trace, 1, index + 1)
        fig['layout'].update(height=400, width=800)
        for i in range(pol_number):
            fig['layout'][f'xaxis{i + 1}'].update(title='I-Branch')
            fig['layout'][f'yaxis{i + 1}'].update(title='Q-Branch')
        viz.plotlyplot(fig)


def eyedigram(signal):
    pass


def save_signal(fn, signal, lvl=4, **kwargs):
    """
    Save a signal object using zlib compression

    Parameters
    ----------
    fn : basestring
        filename
    signal : SignalObject
        the signal to save
    lvl : int, optional
        the compression to use for zlib
    """
    with open(fn, "wb") as fp:
        sc = zlib.compress(
            pickle.dumps({'signal': signal, 'simulation_information': kwargs}, protocol=pickle.HIGHEST_PROTOCOL),
            level=lvl)
        fp.write(sc)


def load_signal(fn):
    """
    Load a signal object from a zlib compressed pickle file.

    Parameters
    ----------
    fn : basestring
        filename of the file

    Returns
    -------
    sig : SignalObject
        The loaded signal object

    """
    with open(fn, "rb") as fp:
        s = zlib.decompress(fp.read())
        obj = pickle.loads(s)
    return obj
