# coding: utf-8
from os.path import abspath
import pyaudio

import numpy as np
import librosa
import librosa.display as disp_rosa
import soundfile as sf

import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.ndimage import maximum_filter1d

class NoiseCanceller():

    def __init__(self, wav_path=None) -> None:

        self.wav_path = wav_path
        self.load(wav_path)

    def load(self, wav_path):
        if not wav_path is None:
            self.y_org, self.sample_rate = librosa.load(wav_path, sr=None)
            print(f"[info] load wav. :{wav_path} - {self.sample_rate}Hz")

    def play(self, y=None):
        _y = self.y_org
        if not y is None:
            _y = y
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.sample_rate,
                        frames_per_buffer=1024,
                        output=True)
        stream.write(_y.astype(np.float32).tostring())

        # ストリームを閉じる
        stream.close()
        # PyAudio終了
        p.terminate()

    def show_power(self, *y):
        print("[info] showpower")
        for i, _y in enumerate(y):
            disp_rosa.waveplot(y=_y, sr=self.sample_rate)
        plt.show()
        plt.close()

    def show_spec(self, *y):
        print("[info] showspec")
        for i, _y in enumerate(y):
            # メルスペクトログラムを求める
            feature_melspec = librosa.feature.melspectrogram(y=_y, sr=self.sample_rate)
            feature_melspec_db = librosa.power_to_db(feature_melspec, ref=np.max)
            disp_rosa.specshow(feature_melspec_db, sr=self.sample_rate, x_axis='time', y_axis='hz')
            plt.colorbar(format="%+2.0f dB")
            plt.title("Mel spectrogram(db scale)")
            plt.tight_layout()
            plt.show()
        plt.close()

    def noise_clip(self, y, threshold_rate=0.5, upper=False):
        self.envelope(y, threshold_rate, upper)

    def envelope(self, y, threshold_rate:float=None, upper=False):
        """
        Args:
            - y: 信号データ
            - threshold_rate: エンベロープ最小最大間に対して閾値を設定する（min: 0>, max: <1.0）
            - upper: 閾値より上をノイズ判定するかのフラグ
        Returns:
            - mask: 振幅がしきい値以上か否か
            - y_mean: Sound Envelop
        """
        y_mean = maximum_filter1d(np.abs(y), mode="constant", size=self.sample_rate//20)
        threshold = np.mean(y_mean)
        if not threshold_rate is None:
            threshold = abs(np.max(y_mean) - np.min(y_mean)) * threshold_rate + np.min(y_mean)
        print(f"threshold: {threshold}")
        # plt.plot(self.y_org)
        # plt.show()
        # plt.close()

        if upper:
            mask = [mean > threshold for mean in y_mean]
        else:
            mask = [mean < threshold for mean in y_mean]
        print(len(mask))
        y_threshold = np.full_like(y_mean, threshold)
        y_noise = self.y_org[mask]
        plt.plot(self.y_org)
        plt.plot(y_mean)
        plt.plot(y_threshold)
        plt.show()
        plt.close()
        return mask, y_mean, y_noise

        # return mask, y_mean

    def _stft(self, y, n_fft, hop_length, win_length):
        return librosa.stft(y=self.y_org, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

    def _amp_to_db(self, x):
        return librosa.core.amplitude_to_db(x, ref=1.0, amin=1e-20, top_db=80.0)

    def _db_to_amp(self, x):
        return librosa.core.db_to_amplitude(x, ref=1.0)

    def _istft(self, y, hop_length, win_length):
        return librosa.istft(y, hop_length, win_length)

    def volume_fix(self):
        # print(f"np_min: {np.min(self.y_cancel)}")
        # self.y_cancel = self.y_cancel - np.min(self.y_cancel)
        # _y_fix = self.y_cancel - np.min(self.y_cancel)
        volume_rate = np.max(np.abs(self.y_org)) / np.max(np.abs(self.y_cancel))
        self.y_cancel = self.y_cancel * volume_rate

    def spectral_canceller(self, n_fft=2048, hop_length=512, win_length=2048, n_std_thresh=1.5, env_thresh=None, noise_level=1.5, volume_fix=False):
        """
        Args:
            - n_fft  # STFTカラム間の音声フレーム数
            - hop_length  # STFTカラム間の音声フレーム数
            - win_length  # ウィンドウサイズ
            - n_std_thresh  # 信号とみなされるために、ノイズの平均値よりも大きい標準偏差（各周波数レベルでの平均値のdB）が何個あるかのしきい値
            - env_thresh  # envelope処理の閾値。
                None指定 -> 平均値
                float(min0.0 - max 1.0)指定 -> 絶対値の最小 - 最大の幅で割合値
            - noise_level  # ノイズ除去レベル(float)
            - volume_fix  # ノイズ除去音源をオリジナル音源のmin-maxの値まで引き延ばすボリューム補正
        """

        mask, envelope, noise_clip = self.envelope(self.y_org, env_thresh)
        noise_stft = self._stft(noise_clip, n_fft, hop_length, win_length)
        noise_stft_db = self._amp_to_db(np.abs(noise_stft))  # dBに変換する

        mean_freq_noise = np.mean(noise_stft_db, axis=1)
        std_freq_noise = np.std(noise_stft_db, axis=1)
        noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

        n_grad_freq = 2  # マスクで平滑化する周波数チャンネルの数
        n_grad_time = 4  # マスクを使って滑らかにする時間チャンネル数
        prop_decrease = noise_level  # ノイズをどの程度減らすか

        # 音源もSTFTで特徴量抽出する
        sig_stft = self._stft(self.y_org, n_fft, hop_length, win_length)
        sig_stft_db = self._amp_to_db(np.abs(sig_stft))

        # 時間と頻度でマスクの平滑化フィルターを作成
        smoothing_filter = np.outer(
                np.concatenate(
                    [
                        np.linspace(0, 1, n_grad_freq + 1, endpoint=False),
                        np.linspace(1, 0, n_grad_freq + 2),
                    ]
                )[1:-1],
                np.concatenate(
                    [
                        np.linspace(0, 1, n_grad_time + 1, endpoint=False),
                        np.linspace(1, 0, n_grad_time + 2),
                    ]
                )[1:-1],
            )
        smoothing_filter = smoothing_filter / np.sum(smoothing_filter)

        # 時間と周波数のしきい値の計算
        db_thresh = np.repeat(
                np.reshape(noise_thresh, [1, len(mean_freq_noise)]),
                np.shape(sig_stft_db)[1],
                axis=0,
            ).T
        sig_mask = sig_stft_db < db_thresh
        sig_mask = fftconvolve(sig_mask, smoothing_filter, mode="same")
        sig_mask = sig_mask * prop_decrease

        mask_gain_dB = np.min(self._amp_to_db(np.abs(sig_stft)))

        sig_stft_db_masked = (
                sig_stft_db * (1 - sig_mask)
                + np.ones(np.shape(mask_gain_dB)) * mask_gain_dB * sig_mask
        )

        sig_imag_masked = np.imag(sig_stft) * (1 - sig_mask)
        sig_stft_amp = (self._db_to_amp(sig_stft_db_masked) * np.sign(sig_stft)) + (1j * sig_imag_masked)

        self.y_cancel = self._istft(sig_stft_amp, hop_length, win_length)

        # self.show_spec(self.y_org, self.y_cancel)
        if volume_fix:
            self.volume_fix()

        self.show_power(self.y_org, self.y_cancel)
        # self.show_spec(self.y_org)

        print("play original wav:")
        self.play(self.y_org)
        input("play noise cancelled wav:")
        self.play(self.y_cancel)


    def write(self, wav_path=None):
        _wav_path = "tmp.wav"
        if not wav_path is None:
            _wav_path = wav_path
        sf.write(_wav_path, self.y_cancel, self.sample_rate, subtype="PCM_16")
        print(f"[info] write wav. :{_wav_path}")
        return abspath(_wav_path)

