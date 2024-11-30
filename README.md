# NEF to JPEG コンバーター
## 概要
NEF to JPEG コンバーターは、指定されたディレクトリ内のすべてのNEF（Nikon RAW）ファイルをJPEG形式に変換します。変換時には、元のNEFファイルの作成日と修正日をJPEGファイルに適用し、EXIFデータも保持します。進捗状況はプログレスバーで表示され、変換プロセスを視覚的に確認できます。

## 特徴
- 一括変換: 指定ディレクトリ内のすべてのNEFファイルを一括でJPEGに変換。
- EXIFデータ保持: 変換後のJPEGファイルに元のNEFファイルのEXIFデータをコピー。
- タイムスタンプ維持: ファイルの作成日と修正日を元のNEFファイルと同じに設定。
- 進捗表示: tqdmライブラリを使用したプログレスバーで変換状況を表示。
- ImageMagick対応: ImageMagick 7以降に対応するためのオプション提供。
## 要件
- Python: バージョン 3.6 以上
- ImageMagick: バージョン 6 または 7
- ExifTool
- 必要なPythonライブラリ:
  - tqdm
- インストール
  - Python のインストール

  - Pythonがインストールされていない場合は、公式サイトからインストールしてください。

## 必要なPythonライブラリのインストール
```bash
pip install tqdm
```

## ImageMagick のインストール
- Windows: ImageMagick公式サイトからインストーラーをダウンロードしてインストール。

- macOS: Homebrewを使用してインストールできます。

```bash
brew install imagemagick
```

## ExifTool のインストール
- Windows: ExifTool公式サイトからダウンロードしてインストール。
- macOS: Homebrewを使用してインストールできます。

```bash
brew install exiftool
```

## 使い方
- スクリプトのダウンロード
- スクリプトをローカルに保存します。例として main.py という名前で保存します。

## コマンドの実行

ターミナル（コマンドプロンプト）を開き、スクリプトが保存されているディレクトリに移動します。
```bash
python main.py /path/to/nef/files
```

/path/to/nef/files をNEFファイルが保存されているディレクトリのパスに置き換えてください。

## オプションの使用

ImageMagick 7以降を使用している場合は、--use-magick オプションを付けて実行します。

```bash
python main.py /path/to/nef/files --use-magick
```

## コマンドラインオプション
- directory
  - 変換対象のNEFファイルが含まれるベースディレクトリを指定します。

- --use-magick
  - ImageMagick 7以降で必要な magick コマンドを使用する場合に指定します。デフォルトでは convert コマンドが使用されます。

## 依存関係
Pythonライブラリ:

tqdm: プログレスバーを表示するために使用します。
外部ツール:

- ImageMagick: NEFファイルをJPEGに変換するために使用します。
- ExifTool: EXIFデータをコピーおよびタイムスタンプを設定するために使用します。

## トラブルシューティング
- ImageMagick または ExifTool が見つからないエラー
  - スクリプト実行時に「コマンドが見つかりません」というエラーが表示された場合、ImageMagickまたはExifToolが正しくインストールされているか、システムのPATHに追加されているかを確認してください。

- 変換中のエラー
  - 特定のNEFファイルの変換中にエラーが発生した場合、ファイルが破損していないか、対応するImageMagickのバージョンが正しいかを確認してください。

- macOSでのタイムスタンプ設定エラー
  - macOSで作成日を設定する際にエラーが発生する場合、SetFile コマンドが利用可能であることを確認してください。SetFile は Xcode コマンドラインツールの一部として提供されています。

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSE ファイルを参照してください。

## 作者
Himawari Project (羽ばたくエンジニア)

## 参考資料
- ImageMagick公式サイト
- ExifTool公式サイト
- tqdm GitHubリポジトリ


このツールが役に立った場合は、ぜひ他のユーザーと共有してください！