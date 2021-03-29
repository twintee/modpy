modpy
# modpy
===============

## description
python用の私用ヘルパ  
実装したもの

- ci
  - gitlab: apiクラス
  - jenkins: job実行用スクリプト
  - coverage: チェック用スクリプト
  - sonarqube: チェック用スクリプト
- classes
  - elapsed_timer: 処理時間測定クラス
- db
  - influxDB
    - init_env: DB接続情報の更新用
    - get: レコード取得用
    - insert: レコード追加用
    - influxdb_handler: DBハンドラ
- image
  - adjust: 画像フォルダ一括調整用
- loader
  - csv_loader: csvのreader/writerクラス
  - env_loader: .envのreader/writerクラス
  - json_loader: jsonのreader/writerクラス
- mattermost:
  - init_env: 接続情報の更新用
  - create: post作成用スクリプト
  - delete: post削除用スクリプト
  - update: post更新用スクリプト
  - mattermost_handler: apiコール用ハンドラ
- helper: 汎用ヘルパ


## usage

1. 適当にクローンして使用。必要に応じてパスに追加。

<pre>
sys.path.append(os.path.join(os.path.dirname(__file__), './modpy'))
</pre>

1. topのrequirementsは必須の物。バージョンの不一致等は適宜調整。利用するディレクトリにrequirements.txtがある場合は随時pipでインストール
<pre>
pip install -r modpy/requirements.txt
</pre>

1. ソースに含めないよう.gitignoreで調整
