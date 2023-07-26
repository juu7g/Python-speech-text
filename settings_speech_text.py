"""
テキスト朗読用設定
"""

# mpg123をインストールした場所
path_mpg123 = r'C:\mpg123'

# テスト用に発声をしないで画面表示だけにする
do_speech = True

# HTMLから文章を抽出する時のセレクタ
select_tag = "div"
select_class = "article_body"   # Yahooニュース用
select_class = "hatenablog-entry"   # はてなブログ用