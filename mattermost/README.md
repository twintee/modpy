modpy
# modpy - mattermost
===============

## 使用準備

* .env ファイルを作成するためのスクリプトを実行します。
<pre>
set_env.py {mattermost_user} {mattermost_password} {mattermost_host} {mattermost_team} {mattermost_port}
</pre>

## 使用法

* メッセージ投稿
<pre>
create.py {mattermost_channel} {message}
</pre>

* メッセージ更新(メッセージ投稿時にreturnされるidを利用する)
<pre>
update.py {posted_id}} {message}
</pre>

* メッセージ削除(メッセージ投稿時にreturnされるidを利用する)
<pre>
delete.py {posted_id}
</pre>
