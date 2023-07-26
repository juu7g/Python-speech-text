"""
音声読み上げ
"""

from gtts import gTTS
from io import BytesIO
import os, sys, time, re
from mpg123 import Mpg123, Out123
import tkinter as tk
from tkinter import PhotoImage
from tkinter import font
from tkinterdnd2 import *
import threading
from urllib.parse import urlparse
from www_juu7g.get_web_text import WebSite
import mimetypes
mimetypes.add_type('text/markdown', '.md')  # Windows環境では存在しないので追加
sys.path.append(os.path.dirname(sys.executable))
import settings_speech_text as settings

# mpg123をインストールした場所
path_mpg123 = settings.path_mpg123
# MPG123を使用するための環境設定
os.environ['PATH'] = os.environ.get('PATH', '') + os.pathsep + path_mpg123
os.environ['MPG123_MODDIR'] = os.path.join(path_mpg123, 'plugins')

class MyFrame(tk.Frame):
    """
    操作画面クラス
    """
    def __init__(self, master) -> None:
        """
        コンストラクタ：画面作成
        """
        super().__init__(master)

        self.aborting = False     # 中断処理用フラグの初期化
        self.in_pause = False     # 一時停止/再開フラグの初期化
        self.event = threading.Event()

        # ウィジェット作成
        # 文章表示用ラベル(折り返し幅が300pxになるようラベル幅を調整、テキストは左右上に寄せる)
        self.font4lbl = font.Font(size=16, weight='bold')  # フォントサイズ指定
        self.var_strings = tk.StringVar()   # ウィジェット変数
        self.var_strings.set('ここにドロップ、\nまたは貼り付け')
        lbl_strings = tk.Label(self, textvariable=self.var_strings, font=self.font4lbl
                , wraplength=300, width=28, anchor='nw', justify=tk.LEFT, padx=10, pady=10)
        lbl_strings.pack(side=tk.RIGHT, fill=tk.Y)
        # アイコン画像用ラベル(画像：60x60px)
        if hasattr(sys, "_MEIPASS"):
            icon_path = sys._MEIPASS  # 実行ファイルで起動した場合
        else:
            icon_path = "."  # python コマンドで起動した場合
        icon_path = os.path.join(icon_path, r"1531637_w60.png")
        self.img = PhotoImage(file=icon_path)
        lbl_icon = tk.Label(self, image=self.img)
        lbl_icon.pack()
        # 中断ボタン
        self.btn_stop = tk.Button(self, text='中断', state=tk.DISABLED, command=self.abort_run)
        self.btn_stop.pack(fill=tk.X)
        # 一時停止/再開
        self.var_pause =tk.StringVar()
        self.var_pause.set('一時停止')
        self.btn_pause = tk.Button(self, textvariable=self.var_pause, state=tk.DISABLED, command=self.pause_run)
        self.btn_pause.pack(fill=tk.X)
        # コンテキストメニュー(貼り付けのみ)
        self.cmenu = tk.Menu(self, tearoff=False)   # メニュー作成
        # 要素追加
        self.cmenu.add_command(label='貼り付け', command=self.check_string_and_get_text_and_speech)
        # SpeechTextクラスの参照の初期化
        self.speech_text = None
        # HatenaBlogクラスのインスタンス作成
        self.hatena_blog = WebSite()
    
    def set_speech_text(self, speech_text):
        """
        SpeechTextクラスの参照を設定
        """
        self.speech_text = speech_text

    def abort_run(self):
        """
        中断処理
        """
        self.aborting = True
        if self.in_pause:
            self.pause_run()    # 一時停止中に中断ボタンが押された場合再開させて中断する
        # ボタンが押された状態にする(読み上げ終わるまで)
        self.btn_stop.config(relief=tk.SUNKEN, state=tk.DISABLED)
        

    def pause_run(self):
        """
        一時停止/再開処理
        """
        if self.in_pause:
            # 再開ボタンが押されたので表示を「一時停止」にしてイベントの内部フラグをセットしてスレッドを再開させる
            self.var_pause.set('一時停止')
            self.event.set()
        else:
            # ボタンが押された状態にする(読み上げ終わるまで)
            self.btn_pause.config(relief=tk.SUNKEN, state=tk.DISABLED)
            # 一時停止ボタンが押されたので表示を「再開」に替えてイベントの内部フラグをクリアする
            self.var_pause.set('再開')
            self.event.clear()
        self.in_pause = not self.in_pause           # フラグを反転

    def show_cmenu(self, event):
        """
        コンテキストメニュー表示
        """
        self.cmenu.post(event.x_root, event.y_root)
    
    def check_string_and_get_text_and_speech(self, event=None):
        """
        ペーストされたテキストがパスかURLかその他かをチェックし、
        パス、URLなら対象を読み込み、読み上げを開始
        """
        # ペースされたものを取得
        if event and hasattr(event, 'data'):        # D&Dの場合
            s1 = self.tk.splitlist(event.data)[0]   # 先頭のみ対象
        else:                                       # ペーストの場合
            s1 = self.clipboard_get()               # クリップボードから取得
        # ファイルが存在したらファイルの内容を読み込む
        if os.path.isfile(s1):
            # MIMEタイプでテキストかどうか判断
            m_t = mimetypes.guess_type(s1)
            if m_t[0].startswith('text/'):
                doc = self.speech_text.get_text_from_file(s1)
                # MIMEタイプがhtml場合テキストだけを取得
                if m_t[0] == 'text/html':
                    doc = self.hatena_blog.get_text_from_html(doc, settings.select_tag, settings.select_class)
            else:
                self.var_strings.set('テキストファイルではありません')
                return
        else:
            # URLだったらサイトから読み込む
            r1 = urlparse(s1)
            if r1.scheme in ('https', 'http'):
                # urlを使ってHTML文書を取得 
                html, err = self.hatena_blog.get_html(s1)
                if err: # HTML文書取得でエラーがあればエラー表示して終了
                    self.var_strings.set(err)
                    return
                # HTML文書からテキストを取得
                doc = self.hatena_blog.get_text_from_html(html, settings.select_tag, settings.select_class)
            else:
                # テキストをそのまま使用
                doc = s1
        # スレッドで読み上げ処理を起動
        th = threading.Thread(target=self.speech_text.do, args=(doc,), daemon=True)
        th.start()

class SpeechText():
    """
    テキストを読み上げるクラス
    """

    def __init__(self, view:MyFrame) -> None:
        """
        コンストラクタ
        Args:
            MyFrame:    ビューのオブジェクト
        """
        self.view = view    # 制御画面クラスのオブジェクト

    def get_text_from_file(self, path) -> str:
        """
        ファイルからテキストを読み込んで返す
        まずUTF8でエンコード、エラーならShift-jisでエンコード
        Args:
            path:   ファイルのパス
        Returns:
            str:    ファイルの中身のテキスト
        """
        try:
            with open(path, encoding='utf_8') as f:
                s = f.read()
        except UnicodeDecodeError:
            try:
                with open(path, encoding='shift_jis') as f:
                    s = f.read()
            except UnicodeDecodeError:
                s = ''
        return s

    def speak_with_mpeg123(self, text:str, lang:str = 'ja'):
        """
        テキストを音声出力する
        Args:
            str:    読み上げるテキスト
            str:    言語(日本語："ja")
        """
        # gTTSで文章を音声合成し、結果をファイルライクオブジェクト(mp3)に書き込み
        f = BytesIO()
        gTTS(text = text, lang = lang).write_to_fp(f)
        f.seek(0)

        # mp3形式のファイルライクオブジェクトを再生
        mp3 = Mpg123()
        mp3.feed(f.read())
        out = Out123()

        for frame in mp3.iter_frames(out.start):
            out.play(frame)

    def text_to_list(self, text:str) -> list:
        """
        文章を改行または句点で分割。ただし、短い文はまとめる。
        1要素は128文字以内。ただし、改行がない場合を除く。
        Args:
            str:    読み上げるテキスト
        Returns:
            list:   読み上げる単位に区切ったテキストのリスト
        """
        # 改行、または「。」の右側で分割する。「。」は残す
        texts = re.split(r"\n|(?<=。)", text)

        strs = []
        pre_s = texts[0]
        for cur_s in texts[1:]:
            if len(pre_s) + len(cur_s) > 128 :
                if pre_s:
                    strs.append(pre_s)
                pre_s = cur_s
            else:
                pre_s = pre_s + " " + cur_s # 空白で区切りをつけておく
        strs.append(pre_s)
        return strs

    def do(self, doc:str):
        """
        テキストを読み上げる
        中断や一時停止を処理する
        Args:
            str:    読み上げるテキスト
        """
        # ボタンを有効にする
        self.view.btn_pause.config(state=tk.NORMAL)
        self.view.btn_stop.config(state=tk.NORMAL)

        strs = self.text_to_list(doc)   # 文章を読み上げ単位に分割

        for text in strs:
            # 一時停止処理
            if self.view.in_pause:
                self.view.event.wait()      # イベントの内部フラグがセットされるまで待つ
            # 中断処理
            if self.view.aborting:
                self.view.var_strings.set('中断しました')
                self.view.aborting = False
                self.view.btn_stop.config(relief=tk.RAISED, state=tk.NORMAL)
                break
            
            # print(f'start:{text[:40]}')
            # 読み上げる設定なら読み上げ、そうでない(表示のみ)なら2秒待つ
            self.view.var_strings.set(text)     # 文章を画面表示
            if settings.do_speech:
                self.speak_with_mpeg123(text)   # 文章の読み上げ
            else:
                time.sleep(5)
            # ボタンが押された状態を戻す
            self.view.btn_pause.config(relief=tk.RAISED, state=tk.NORMAL)
        # ボタンを無効にする
        self.view.btn_pause.config(state=tk.DISABLED)
        self.view.btn_stop.config(state=tk.DISABLED)

class App(TkinterDnD.Tk):
    """
    アプリケーションクラス
    """
    def __init__(self) -> None:
        """
        コンストラクタ：操作画面クラスと制御クラスを作成し関連付ける
        """
        super().__init__()

        self.title("貼って読み上げ")      # タイトル
        my_frame = MyFrame(self)       # MyFrameクラス(V)のインスタンス作成
        my_frame.pack()

        # ペーストの設定
        self.bind('<Control-v>', my_frame.check_string_and_get_text_and_speech)
        self.bind('<Button-3>', my_frame.show_cmenu)    # 右クリックでコンテキストメニュー表示

        # ドラッグ&ドロップの設定
        self.drop_target_register(DND_FILES)       # ドロップを受け付け
        self.dnd_bind('<<Drop>>', my_frame.check_string_and_get_text_and_speech)

        speech_text = SpeechText(my_frame)     # 制御クラス(C)のインスタンス作成
        my_frame.set_speech_text(speech_text)  # ビューにSpeechTextクラスを設定

if __name__ == '__main__':
    app = App()
    app.mainloop()
