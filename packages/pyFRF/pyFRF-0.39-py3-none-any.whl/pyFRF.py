# -*- coding: utf-8 -*-
# Copyright (C) 2014-2017 Martin Česnik, Matjaž Mršnik, Miha Pirnat, Janko Slavič, Blaž Starc (in alphabetic order)
# 
# This file is part of pyFRF.
# 
# pyFRF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# pyFRF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyFRF.  If not, see <http://www.gnu.org/licenses/>.


"""

Module for FRF signal processing.

Classes:
    class FRF:      Handles 2 channel frequency response function.

"""

import numpy as np
import fft_tools

__version__ = '0.39'
_EXC_TYPES = ['f', 'a', 'v', 'd', 'e']  # force for EMA and kinematics for OMA
_RESP_TYPES = ['a', 'v', 'd', 'e']  # acceleration, velocity, displacement, strain
_FRF_TYPES = ['H1', 'H2', 'Hv', 'vector', 'ODS']
_FRF_FORM = ['accelerance', 'mobility', 'receptance']
_WGH_TYPES = ['None', 'Linear', 'Exponential']
_WINDOWS = ['None', 'Hann', 'Hamming', 'Force', 'Exponential', 'Bartlett', 'Blackman', 'Kaiser']

_DIRECTIONS = ['scalar', '+x', '+y', '+z', '-x', '-y', '-z']
_DIRECTIONS_NR = [0, 1, 2, 3, -1, -2 - 3]


def direction_dict():
    dir_dict = {a: b for a, b in zip(_DIRECTIONS, _DIRECTIONS_NR)}
    return dir_dict


class FRF:
    """
    Perform Dual Channel Spectral Analysis

        :param sampling_freq: sampling frequency
        :param exc_type: excitation type, see _EXC_TYPES
        :param resp_type: response type, see _RESP_TYPES
        :param exc_window: excitation window, see _WINDOWS
        :param resp_window: response window, see _WINDOWS
        :param resp_delay: response time delay (in seconds) with regards to the excitation
                           (use positive value for a delayed signal)
        :param weighting: weighting type for average calculation, see _WGH_TYPES
        :param n_averages: number of measurements, used for averaging
               if later data for overlapping is used, the n_averages is automatically defined
        :param fft_len: the length of the FFT
                        If None then the freq length matches the time length
        :param nperseg: int, optional
                        Length of each segment.
                        If None, then the length corresponds to the data length
        :param noverlap: int, optional
                         Number of points to overlap between segments.
                         If None,  ``noverlap = nperseg / 2``.  Defaults to None.
        :param archive_time_data: archive the time data (this can consume a lot of memory)
        :param frf_type: default frf type returned at self.get_frf(), see _FRF_TYPES
        :param copy: if true the exc and resp arrays are copied (if data is not copied the
                     applied window affect the source arrays
    """

    def __init__(self, sampling_freq,
                 exc=None,
                 resp=None,
                 exc_type='f', resp_type='a',
                 exc_window='Force:0.01', resp_window='Exponential:0.01',
                 resp_delay=0.,
                 weighting='Exponential', n_averages=1,
                 fft_len=None,
                 nperseg=None,
                 noverlap=None,
                 archive_time_data=False,
                 frf_type='H1',
                 copy=True):
        """
        initiates the Data class:

        :param sampling_freq: sampling frequency
        :param exc: excitation array; if None, no data is added and init
        :param resp: response array
        :param exc_type: excitation type, see _EXC_TYPES
        :param resp_type: response type, see _RESP_TYPES
        :param exc_window: excitation window, see _WINDOWS
        :param resp_window: response window, see _WINDOWS
        :param resp_delay: response time delay (in seconds) with regards to the excitation.
        :param weighting: weighting type for average calculation, see _WGH_TYPES
        :param n_averages: number of measurements, used for averaging
        :param fft_len: the length of the FFT (zero-padding if longer than length of data)
        :param nperseg: optional segment length, by default one segment is analyzed
        :param noverlap: optional segment overlap, by default ``noverlap = nperseg / 2``
        :param archive_time_data: archive the time data (this can consume a lot of memory)
        :param frf_type: default frf type returned at self.get_frf(), see _FRF_TYPES
        :param copy: if true the exc and resp arrays are copied (if data is not copied the
                     applied window affect the source arrays
        :return:
        """

        # data info
        self.sampling_freq = sampling_freq
        self._data_available = False
        self.exc_type = exc_type
        self.resp_type = resp_type
        self.exc_window = exc_window
        self.resp_window = resp_window
        self.resp_delay = resp_delay
        self.frf_type = frf_type
        self.copy = copy

        # ini
        self.exc = np.array([])
        self.resp = np.array([])
        self.exc_archive = []
        self.resp_archive = []
        self.samples = None

        # set averaging and weighting
        self.n_averages = int(n_averages)
        self.weighting = weighting
        self.frf_norm = 1.

        # fft length
        if fft_len is None:
            if exc is None:
                raise Exception('If no excitaton signal is given, fft_len needs to be defined!')
            self.fft_len = len(exc)
        else:
            self.fft_len =  int(fft_len)
        self.nperseg = nperseg
        self.noverlap = noverlap

        # save time data
        self.archive_time_data = archive_time_data

        # error checking
        if not (self.frf_type in _FRF_TYPES):
            raise Exception('wrong FRF type given %s (can be %s)'
                            % (self.frf_type, _FRF_TYPES))

        if not (self.weighting in _WGH_TYPES):
            raise Exception('wrong weighting type given %s (can be %s)'
                            % (self.weighting, _WGH_TYPES))

        if not (self.exc_type in _EXC_TYPES):
            raise Exception('wrong excitation type given %s (can be %s)'
                            % (self.exc_type, _EXC_TYPES))

        if not (self.resp_type in _RESP_TYPES):
            raise Exception('wrong response type given %s (can be %s)'
                            % (self.resp_type, _RESP_TYPES))

        if not (self.exc_window.split(':')[0] in _WINDOWS):
            raise Exception('wrong excitation window type given %s (can be %s)'
                            % (self.exc_window, _WINDOWS))

        if not (self.resp_window.split(':')[0] in _WINDOWS):
            raise Exception('wrong response window type given %s (can be %s)'
                            % (self.resp_window, _WINDOWS))

        self.curr_meas = np.int(0)

        if exc is not None and resp is not None:
            self.add_data(exc, resp)

    def add_data_for_overlapping(self, exc, resp):
        """Adds data and prepares FRF with the overlapping options

        :param exc: excitation array
        :param resp: response array
        :return:
        """
        self._add_to_archive(exc, resp)
        samples = len(exc)
        if self.nperseg is None:
            self.nperseg = samples
        elif self.nperseg >= samples:
            raise ValueError('nperseg must be less than samples.')
        if self.noverlap is None:
            self.noverlap = self.nperseg // 2
        elif self.noverlap >= self.nperseg:
            raise ValueError('noverlap must be less than nperseg.')

        self._ini_lengths_and_windows(self.nperseg)
        step = self.nperseg - self.noverlap
        indices = np.arange(0, samples - self.nperseg + 1, step)
        self.n_averages = len(indices)
        for k, ind in enumerate(indices):
            if self.noverlap or self.copy:  # need to prepare copy array (due to the windows)
                self.exc = np.copy(exc[ind:ind + self.nperseg])
                self.resp = np.copy(resp[ind:ind + self.nperseg])
            else:
                self.exc = exc[ind:ind + self.nperseg]
                self.resp = resp[ind:ind + self.nperseg]

            # add windows
            self._apply_window()

            # go into freq domain
            self._get_fft()

            # get averaged FRF and coherence
            self._get_frf_av()

            # measurement number counter
            self.curr_meas += 1
            self._data_available = True

    def is_data_ok(self, exc, resp, 
                 overflow_samples=3, 
                 double_impact_limit=1e-3, print_double_impact_ratio=False):
        """Checks the data for overflow and double-impact

        :param exc: excitation array
        :param resp: response array
        :param overflow_samples: number of samples that need to be equal to max
                                 for overflow identification
        :param double_impact_limit: ratio of freq content od the double vs single hit
                      smaller number means more sensitivity
        :param print_double_impact_ratio: prints the ratio of the double PSD main lobe vse after lobe 
        :return: True if data added
        """
        if self._is_overflow(exc, overflow_samples=overflow_samples) or \
            self._is_overflow(resp, overflow_samples=overflow_samples) or \
            self._is_double_impact(exc, limit=double_impact_limit, print_ratio=print_double_impact_ratio):
            return False
        else:
            return True


    def add_data(self, exc, resp):
        """Adds data and prepares receptance FRF

        :param exc: excitation array
        :param resp: response array
        :return: True if data added
        """
          
        # add time data
        self._add_to_archive(exc, resp)
        if self.copy:
            self.exc = np.copy(exc)
            self.resp = np.copy(resp)
        else:
            self.exc = exc
            self.resp = resp
        self._ini_lengths_and_windows(len(self.exc))

        # add windows
        self._apply_window()

        # go into freq domain
        self._get_fft()

        # get averaged FRF and coherence
        self._get_frf_av()

        # measurement number counter
        self.curr_meas += 1
        self._data_available = True
        
        return True

    def get_df(self):
        """Delta frequency in Hz

        :return: delta frequency in Hz
        """
        if not self._data_available:
            raise Exception('No data has been added yet!')

        return self.get_f_axis()[1]

    def get_f_axis(self):
        """

        :return: frequency vector in Hz
        """
        if not self._data_available:
            raise Exception('No data has been added yet!')

        return np.fft.rfftfreq(self.fft_len, 1. / self.sampling_freq)

    def get_t_axis(self):
        """Returns time axis.

        :return: return time axis
        """

        if not self._data_available:
            raise Exception('No data has been added yet!')

        return np.arange(self.samples) / self.sampling_freq

    def _apply_window(self):
        """Apply windows to exc and resp data

        :return:
        """
        self.exc *= self.exc_window_data
        self.resp *= self.resp_window_data

    def _get_window_sub(self, window='None'):
        """Returns the window time series and amplitude normalization term

        :param window: window string
        :return: w, amplitude_norm
        """
        window = window.split(':')

        if window[0] in ['Hanning', 'Hann']:
            w = np.hanning(self.samples)
        elif window[0] in ['Hamming']:
            w = np.hamming(self.samples)
        elif window[0] in ['Bartlett']:
            w = np.bartlett(self.samples)
        elif window[0] in ['Blackman']:
            w = np.blackman(self.samples)
        elif window[0] in ['Kaiser']:
            beta = float(window[1])
            w = np.kaiser(self.samples, beta)
        elif window[0] == 'Force':
            w = np.zeros(self.samples)
            force_window = float(window[1])
            to1 = np.long(force_window * self.samples)
            w[:to1] = 1.
        elif window[0] == 'Exponential':
            w = np.arange(self.samples)
            exponential_window = float(window[1])
            w = np.exp(np.log(exponential_window) * w / (self.samples - 1))
        else:  # window = 'None'
            w = np.ones(self.samples)


        if window[0] == 'Force':
            amplitude_norm = 2 / len(w)
        else:
            amplitude_norm = 2 / np.sum(w)

        return w, amplitude_norm

    def _get_fft(self):
        """Calculates the fft ndarray of the most recent measurement data

        :return:¸
        """
        # define FRF - related variables (only for the first measurement)

        if self.curr_meas == 0:
            if self.fft_len is None:
                self.fft_len = int(self.samples)
            self.w_axis = 2 * np.pi * np.fft.rfftfreq(self.fft_len, 1. / self.sampling_freq)

        self.Exc = np.fft.rfft(self.exc, self.fft_len)
        self.Resp = np.fft.rfft(self.resp, self.fft_len)

        if self.resp_type != 'e':  # if not strain
            # convert H1 to receptance
            self.Resp = fft_tools.convert_frf(self.Resp, self.w_axis, input_frf_type=self.resp_type,
                                              output_frf_type='d')

            # correct delay
        if self.resp_delay != 0.:
            self.Resp = fft_tools.correct_time_delay(self.Resp, self.w_axis, -self.resp_delay)

    def get_ods_frf(self):
        """Operational deflection shape averaged estimator

        Numerical implementation of Equation (6) in [1].

        Literature:
            [1] Schwarz, Brian, and Mark Richardson. Measurements required for displaying
                operating deflection shapes. Presented at IMAC XXII January 26 (2004): 29.

        :return: ODS FRF estimator
        """
        # 2 / self.samples added for proper amplitude
        # TODO check for proper norming if window changed
        return 2 / self.samples * (np.sqrt(self.S_XX) * self.S_XF / np.abs(self.S_XF))

    def get_resp_spectrum(self, amplitude_spectrum=True, last=True):
        """get response amplitude/power spectrum

        :param amplitude_spectrum: get amplitude spectrum else power
        :param last: return the last only (else the averaged value is returned)
        :return: response spectrum
        """
        k = self.resp_window_amp_norm

        if last:
            amp = np.abs(self.Resp)
        else:
            amp = np.sqrt(np.abs(self.S_XX))

        if amplitude_spectrum:
            return k * amp
        else:
            return k * amp ** 2

    def get_exc_spectrum(self, amplitude_spectrum=True, last=True):
        """get excitation amplitude/power spectrum

        :param amplitude_spectrum: get amplitude spectrum else power
        :param last: return the last only (else the averaged value is returned)
        :return: excitation spectrum
        """
        k = self.exc_window_amp_norm

        if last:
            amp = np.abs(self.Exc)
        else:
            amp = np.sqrt(np.abs(self.S_FF))

        if amplitude_spectrum:
            return k * amp
        else:
            return k * amp**2

    def get_H1(self):
        """H1 FRF averaged estimator  (receptance), preferable call via get_FRF()

        :return: H1 FRF estimator
        """
        with np.errstate(invalid='ignore'):
            return self.frf_norm * self.S_FX / self.S_FF

    def get_H2(self):
        """H2 FRF averaged estimator (receptance), preferable call via get_FRF()

        :return: H2 FRF estimator
        """
        with np.errstate(invalid='ignore'):
            return self.frf_norm * self.S_XX / self.S_XF

    def get_Hv(self):
        """Hv FRF averaged estimator (receptance), preferable call via get_FRF()

        Literature:
            [1] Kihong and Hammond: Fundamentals of Signal Processing for
                Sound and Vibration Engineers, page 293.

        :return: Hv FRF estimator
        """
        k = 1  # ratio of the spectra of measurement noises
        with np.errstate(invalid='ignore'):
            receptance = self.frf_norm * ((self.S_XX - k * self.S_FF + np.sqrt(\
                (k * self.S_FF - self.S_XX) ** 2 + 4 * k * np.conj(self.S_FX) * self.S_FX))\
                                        / (2 * self.S_XF))
        return receptance

    def get_FRF_vector(self):
        """Vector FRF averaged estimator (receptance), preferable call via get_FRF()

        :return: FRF vector estimator
        """
        with np.errstate(invalid='ignore'):
            return self.frf_norm * self.S_X / self.S_F

    def get_FRF(self, type='default', form='receptance'):
        """Returns the default FRF function set at init.

        :return: FRF estimator
        :type: choose default (as set at init) or H1, H2, Hv, vector or ODS
        :form: choose receptance, mobility, accelerance
        """
        if type=='default':
            type=self.frf_type
        if not (type in _FRF_TYPES):
            raise Exception('wrong FRF type given %s (can be %s)'
                            % (type, _FRF_TYPES))

        if type == 'H1':
            receptance = self.get_H1()
        if type == 'H2':
            receptance = self.get_H2()
        if type == 'Hv':
            receptance = self.get_Hv()
        if type == 'vector':
            receptance = self.get_FRF_vector()
        if type == 'ODS':
            receptance = self.get_ods_frf()

        if not (form in _FRF_FORM):
            raise Exception('wrong FRF form given %s (can be %s)'
                            % (form, _FRF_FORM))

        if form=='accelerance':
            return fft_tools.frequency_derivation(receptance, self.get_f_axis(), order=2)
        if form=='mobility':
            return fft_tools.frequency_derivation(receptance, self.get_f_axis(), order=1)
        return receptance

    def get_coherence(self):
        """Coherence

        :return: coherence
        """
        with np.errstate(invalid='ignore'):
            return np.abs(self.get_H1() / self.get_H2())

    def _get_frf_av(self):
        """Calculates the averaged FRF based on averaging and weighting type


        Literature:
            [1] Haylen, Lammens, Sas: ISMA 2011 Modal Analysis Theory and Testing page: A.2.27
            [2] http://zone.ni.com/reference/en-XX/help/371361E-01/lvanlsconcepts/average_improve_measure_freq/

        :return:
        """
        # obtain cross and auto spectra for current data
        S_FX = np.conj(self.Exc) * self.Resp
        S_FF = np.conj(self.Exc) * self.Exc
        S_XX = np.conj(self.Resp) * self.Resp
        S_XF = np.conj(self.Resp) * self.Exc
        # direct
        S_F = self.Exc
        S_X = self.Resp

        # obtain average spectra
        if self.curr_meas == 0:
            self.S_XX = S_XX
            self.S_FF = S_FF
            self.S_XF = S_XF
            self.S_FX = S_FX
            self.S_X = S_X
            self.S_F = S_F
        else:
            if self.weighting == 'Linear':
                N = np.float64(self.curr_meas) + 1
            else:  # 'Exponential'
                N = np.float64(self.n_averages)

            self.S_XX = 1 / N * S_XX + (N - 1) / N * self.S_XX
            self.S_FF = 1 / N * S_FF + (N - 1) / N * self.S_FF
            self.S_XF = 1 / N * S_XF + (N - 1) / N * self.S_XF
            self.S_FX = 1 / N * S_FX + (N - 1) / N * self.S_FX
            self.S_X = 1 / N * S_X + (N - 1) / N * self.S_X
            self.S_F = 1 / N * S_F + (N - 1) / N * self.S_F

    def _ini_lengths_and_windows(self, length):
        """
        Sets the lengths used later in fft

        Parameters
        ----------
        length: length of data expected
        """
        if self.curr_meas != 0:
            return
        if self.samples is None:
            self.samples = length
        elif self.samples != len(self.exc):
            raise ValueError('data length changed.')

        self.exc_window_data, self.exc_window_amp_norm = self._get_window_sub(self.exc_window)
        self.resp_window_data, self.resp_window_amp_norm = self._get_window_sub(self.resp_window)
        self.frf_norm = self.resp_window_amp_norm / self.exc_window_amp_norm

    def _add_to_archive(self, exc, resp):
        """Add time data to the archive for later data analysis

        :param exc: excitation data
        :param resp: response data
        :return:
        """
        if self.archive_time_data:
            self.resp_archive.append(resp)
            self.exc_archive.append(exc)

    def get_archive(self):
        """Returns the time archive. If not available, it returns None, None

        :return: (excitation, response) time archive
        """
        if self.archive_time_data:
            return self.exc_archive, self.resp_archive
        else:
            return None, None

    def _is_overflow(self, data, overflow_samples=3):
        """Check data for overflow
    
        :param overflow_samples: number of samples that need to be equal to max
                                 for overflow identification
        :return: overflow status
        """
        flat_shape = data.reshape(-1)
        s = np.sort(np.abs(flat_shape))[::-1]
        over = s == np.max(s)
        if np.sum(over) >= overflow_samples:
            return True
        else:
            return False

    def _is_double_impact(self, data, limit=1e-3, print_ratio=False):
        """Check data for double-impact

        See: at the end of http://scholar.lib.vt.edu/ejournals/MODAL/ijaema_v7n2/trethewey/trethewey.pdf
        
        :param data: one or two (time, samples) dimensional array
        :param limit: ratio of freq content of the double vs single hit
                      smaller number means more sensitivity
        :param print_ratio: prints the ratio of the double PSD main lobe vse after lobe 
        :return: double-hit status
        """
        if data.ndim > 2:
            raise Exception('Number of dimensions of data should be 2 or less!')

        def _double_impact_check(x):
            skip_low_freq = 10
            # first PSD
            X = np.fft.rfft(x)[skip_low_freq:]  
            X = 2 / self.sampling_freq * np.real(X * np.conj(X))/len(x)
            # second PSD: look for oscillations in PSD
            X2 = np.fft.rfft(X)
            X2 = 2 / self.sampling_freq * np.real(X2 * np.conj(X2))/len(X)
            upto = int(0.01 * len(X2))
            max_impact = np.max(X2[:upto])
            max_after_impact = np.max(X2[upto:])
            if print_ratio:
                print(f'Ratio of the double PSD main lobe vse after lobe {max_after_impact / max_impact:g}')
            if max_after_impact / max_impact > limit:
                return True
            else:
                return False

        if data.ndim == 2:
            double_hit = [_double_impact_check(d) for d in data.T]
            return double_hit
        else:
            double_hit = _double_impact_check(data)
            return double_hit


if __name__ == '__main__':
    pass
