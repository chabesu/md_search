from bs4 import BeautifulSoup
import re
import os
from flask import Flask, render_template, request, redirect, flash
import time
import markdown2

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    path = "#"  # mdファイルの格納場所を絶対パスで指定
    result = []

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        t1 = time.time()    # 処理前の時刻。検索時間測定用。

        # 検索する
        search_key = request.form.get('search_key')
        search = re.compile(search_key)

        for file in os.listdir(path):   # 指定したフォルダからmdファイルを検索
            base, ext = os.path.splitext(file)
            if ext == '.md':
                f = open(path + file, encoding="utf-8")
                md = f.read()
                htmlconv = markdown2.Markdown().convert(md)     # markdown形式をhtml形式に変換
                html = "<body>" + htmlconv + "</body>"          # bodyタグを付ける。検索対象をbodyタグ内と指定するため。
                soup = BeautifulSoup(html, "html.parser")
                elems = soup.find_all(text = search)
                judge = bool(elems)
                if judge:   # 検索対象のキーワードがある場合は、検索結果を表示するための配列を作成
                    file_name = file
                    url = path + file
                    contents = soup.find('body').text
                    # 検索文字の位置を特定して、検索文字の50文字前から300文字後を表示。
                    m = re.search(search, contents)
                    s = m.start()-50 if (m.start()-50) >= 0 else 0  # 検索文字が元から50文字以内の場合は0文字から表示する。
                    contents = soup.find('body').text[s:s+300].replace( '\n' , '' ) + "..." 
                    list = {"file_name":file_name, "url":url, "contents":contents}
                    result.append(list)

        t2 = time.time()    # 処理後の時刻
        elapsed_time = t2-t1    # 経過時間を計算

    return render_template('index.html', result=result, elapsed_time='{:.1g}'.format(elapsed_time), search_key=search_key)

if __name__ == "__main__":
    app.run(debug=True)



