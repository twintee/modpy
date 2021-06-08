# coding: utf-8
from os.path import abspath
import pyaudio
import numpy as np
import wave
import librosa
import librosa.display
import matplotlib.pyplot as plt
from time import sleep

class SoundRecoder():

    def __init__(self,
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            frames_per_buffer=1024) -> None:
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

        self.reset(format, channels, rate, frames_per_buffer)

    def reset(self,
            format=None,
            channels=None,
            rate=None,
            frames_per_buffer=None):

        if not format is None:
            self.format = format
        if not channels is None:
            self.channels = channels
        if not rate is None:
            self.rate = rate
        if not frames_per_buffer is None:
            self.frames_per_buffer = frames_per_buffer

        self.audio = pyaudio.PyAudio()

        self.frames = []

    def rec(self):

        try:

            stream = self.audio.open(format=self.format,
                    channels=self.channels,
                    rate=self.rate,
                    frames_per_buffer=self.frames_per_buffer,
                    input=True,
                    output=False)

            self.frames = []

            print ("recording...")
            while stream.is_active():
                try:
                    input = stream.read(self.frames_per_buffer, exception_on_overflow=False)
                    self.frames.append(input)
                except KeyboardInterrupt:
                    stream.stop_stream()
                    stream.close()
                    print ("finished recording")
                    break

        except OSError as e:
            print(f'OSError :{e}')
            # return False

    def get_wav(self, wav_path='tmp.wav', img_path='tmp.png', show_spec=False):
        """
        Args:
            - wav_path: wav保存先
            - img_path: 波形画像保存先
            - showspec: matplotlibで波形を表示するフラグ(bool)
        Returns:
            - wav_path: 保存されたwavの絶対パス
        """

        # wave保存
        with wave.open(wav_path, 'wb') as f:
            f.setnchannels(self.channels)
            f.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            f.setframerate(self.rate)
            f.writeframes(b''.join(self.frames))
            f.close()

        waveform, sample_rate = librosa.load(wav_path)

        # メルスペクトログラムを求める
        feature_melspec = librosa.feature.melspectrogram(y=waveform, sr=sample_rate)

        plt.figure(figsize=(15,5))

        # librosa.feature.melspectrogramをそのまま可視化した場合
        plt.subplot(1,2,1)
        plt.title("mel spectrogram")
        librosa.display.specshow(feature_melspec, sr=sample_rate, x_axis='time', y_axis='hz')
        plt.colorbar()

        # デシベルスケールに変換した場合
        plt.subplot(1,2,2)
        plt.title("db scale mel spectrogram")
        feature_melspec_db = librosa.power_to_db(feature_melspec, ref=np.max)
        librosa.display.specshow(feature_melspec_db, sr=sample_rate, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')

        plt.tight_layout()

        plt.savefig(img_path)

        if show_spec:
            plt.show()

        return abspath(wav_path)
