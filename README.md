# Python-speech-text


## 概要 Description
テキストを読み上げ

URL やパス、テキストを貼り付けると内容を音声で読み上げます。  

## 特徴 Features

- はてなブログの記事の URL をコピーして本アプリに貼り付けると読み上げます
- 記事の部分だけを読み上げます
- ローカルのテキストファイル、HTMLファイルを本アプリにドラッグアンドドロップすると読み上げます
- クリップボードにコピーしたテキストを本アプリに貼り付けすると読み上げます
- 読み上げるとともに文章を画面表示します
- 読み上げないで文章だけ表示することができます
- 読み上げの一時停止/再開、中断ができます
- はてなブログの記事以外でも記事の部分だけ読み上げるようにカスタマイズできます

## 依存関係 Requirement

- Python 3.8.5  
- mpg123(Python) 0.4
- mpg123 1.31.3
- beautifulsoup4 4.12.2
- requests 2.31.0
- tkinterdnd2 0.3.0
- gTTS 2.3.2
- www_juu7g 1.0.0
- アイコン用の画像ファイルが必要です

## 使い方 Usage

- 操作  

	- *読み上げの開始*
		- 貼り付けで開始  
			本アプリ画面上で右クリックして「貼り付け」をクリックします  
			貼り付けられる内容
			- URL のリンク
			- HTML ファイルのパス
			- テキストファイルのパス
			- テキスト（上記以外）
		- ドラッグアンドドロップで開始  
			エクスプローラーなどから本アプリにファイルをドラッグアンドドロップします  
			ドラッグアンドドロップで動作するもの
			- HTML ファイル
			- テキストファイル
	- *読み上げの一時停止*  
		- 「一時停止」ボタンを押します  
		- 画面表示した文章を読み終わってから一時停止します  
		- ボタンの表示が「再開」に変わります
	- *読み上げの再開*  
		- 「再開」ボタンを押します  
		- ボタンの表示が「一時停止」に変わります
	- *読み上げの中断*  
		- 「中断」ボタンを押します  
		- 画面表示した文章を読み終わってから中断します  
		- 一時停止中も有効です  
		- 「中断しました」と画面に表示されます


- 画面の説明  
	- ボタン
		- 中断：  
			読み上げを中断します
		- 一時停止/再開：  
			読み上げを一時停止します。一時停止中はボタンの表示が再開になります  
			再開ボタンを押すと読み上げを再開します

## 制限事項  

- インターネットに接続している必要があります
- Google 翻訳の音声機能について Google に情報が見つかりませんが動作しています  
	Google 翻訳の音声機能がサービスされなくなると動作しなくなります

## 依存関係パッケージのインストール方法 Installation

- Python ライブラリ  
	- pip install gTTS
	- pip install mpg123  
	- pip install tkinterdnd2
	- pip install git+https://github.com/juu7g/Python-www.git

- mpg123 ライブラリの取得と設定  
	- 取得  
		次のリンクから mpd123 ライブラリをダウンロードしてください  
		(Windows 64 bit OS の場合)
		- [Index of /download/win64/1.31.3 <i class="blogicon-external"></i>](https://www.mpg123.de/download/win64/1.31.3/)  
			`mpg123-1.31.3-x86-64.zip` をダウンロードしてください
			解凍して使用します
	- 設定
		`settings_speech_text.py` ファイル内の `path_mpg123` に mpg123 ライブラリのフォルダを指定してください

## プログラムの説明サイト Program description site

- [gTTSとmpg123で作るテキスト読み上げアプリ【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/text-to-speech/speech-text)  
  
## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSEファイルを確認してください。  
This software is released under the MIT License, see LICENSE file.

