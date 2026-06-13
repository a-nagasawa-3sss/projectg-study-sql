# study-sql

SQL練習問題集です。各自のPC上でローカル実行します。サーバーへの公開は不要です。

## セットアップ

```bash
# 1. 仮想環境の作成（study-sqlディレクトリ直下、初回のみ）
python -m venv .venv

# 2. 仮想環境の有効化
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (コマンドプロンプト)
.venv\Scripts\activate.bat
# macOS/Linux
source .venv/bin/activate

# 3. 依存パッケージのインストール
pip install -r requirements.txt

# 4. 練習用データベースの作成（初回のみ）
python app/db/build_db.py
```

## 起動方法

```bash
# 仮想環境を有効化した状態で
python app/app.py
```

起動後、ブラウザで http://127.0.0.1:8000 を開いてください。

## 使い方

1. トップページの説明を読み、「はじめての人はこちら」からGemini APIキーを登録します
   （[Google AI Studio](https://aistudio.google.com/apikey)で無料発行できます）。
   APIキーはブラウザのlocalStorageに保存され、サーバーには保存されません。
   APIキーを登録しなくても出題・正誤判定自体は利用できます。
2. 「練習を始める」から難易度（easy / medium / hard / very-hard）を選び、「問題を取得」を押します。
3. 表示された問題文と、関連するテーブルのデータを確認しながら回答SQLを入力します。
4. 「回答する」を押すと実行結果が表示され、正解と一致すれば「✅ 正解」、
   一致しない場合は「❌ 不正解」となり、AIによるヒントが表示されます
   （APIキー未設定時はヒントはスキップされます）。
5. 「問題を取得」を押すと次の問題に進みます。

## Gemini APIについて

不正解時のAIヒント表示には、Google Gemini APIを利用します。

### 取得方法

1. [Google AI Studio](https://aistudio.google.com/apikey) にGoogleアカウントでログインします。
2. 「APIキーを作成」（環境によっては「Create API key」）をクリックします。
3. プロジェクトの選択を求められた場合は、既存のプロジェクトを選択するか、
   「新しいプロジェクトを作成」のまま進めてください（個人利用であればどちらでも問題ありません）。
4. 作成が完了すると、APIキー（`AIzaSy...`で始まる文字列）が表示されます。
   右側のコピーアイコンをクリックしてコピーします。
   - このダイアログを閉じてもAPIキー自体は無効になりませんが、
     再表示するには一覧画面から該当のキーを選んでコピーする必要があります。
5. study-sqlの `/setup` ページにアクセスし、コピーしたAPIキーを貼り付けて「保存する」を押します。
   APIキーはブラウザのlocalStorageに保存され、サーバーには送信・保存されません。

### 使用するモデル

本アプリでは `gemini-2.5-flash-lite` を固定で使用します（モデル選択UIはありません）。
Gemini系の中でも最も軽量で、無料枠の範囲内に収まりやすく料金が発生しにくいモデルです。

（旧モデルの`gemini-2.0-flash`は2026年6月1日付けで廃止されています。）

### 無料でどれくらい使えるか

`gemini-2.5-flash-lite`のGemini API無料枠（Free Tier）は以下のような制限があります（2026年6月時点、Google公式のRate limitsページの情報）。

| モデル | リクエスト数/分 | リクエスト数/日 | トークン数/分 |
| --- | --- | --- | --- |
| gemini-2.5-flash-lite | 15 RPM | 1,500 RPD | 1,000,000 TPM |

study-sqlでは「不正解になったときに1回だけ」AIへ問い合わせるため、1日1,500回という制限に達することはほぼありません。
ただし、無料枠は予告なく変更される可能性があるため、最新情報は
[公式のRate limitsページ](https://ai.google.dev/gemini-api/docs/rate-limits)
を確認してください。

## 補足

- 回答SQLはSELECT文（またはWITH句）のみ実行できます。
- 正誤判定は、SQLの文字列一致ではなく**実行結果の比較**で行われます
  （行の並び順は問いません）。
- 問題は `app/data/questions.json` に格納されています。
