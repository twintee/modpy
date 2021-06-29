# python sound modules

python3のサウンド関連モジュール

## Installation

```
pip install -r requirements.txt
```

## usage

### 音声録音

```
sr = SoundRecoder()
sr.rec()
wav_path = sr.get_wav()
```

#### デモ実行

* スクリプト実行
`python soundrecorder_demo.py`
下記表示されたら音声録音中
`Recording...`
* `Ctrl + c`で録音終了。`sample.wav`が作成されて波形画像が表示される。

### ノイズ除去

```
nc = NoiseCanceller()
nc.load("nc.wav")
nc.spectral_canceller(env_thresh=0.1, noise_level=1.0, volume_fix=True)
# output noise cancelled wav
wav_nc_path = nc.write("nc_.wav")
```

#### デモ実行

* スクリプト実行
`python noisecanceller_demo.py`
* オリジナル波形(青)、エンベロープ(オレンジ)、閾値（）の画像表示
* オリジナル波形(青)、ノイズ除去波形(オレンジ)の画像表示
* オリジナル音源再生
* enterキーでノイズ除去音源再生
```
nc = NoiseCanceller()
nc.load("nc.wav")
nc.spectral_canceller(env_thresh=None, noise_level=1.0)
```
