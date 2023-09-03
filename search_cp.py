#【システム概要】約５秒で検索ワードがヒットしたテキストファイルを立ち上げる

import glob
import os
import subprocess
import difflib
from chardet import detect

# 一番上の階層のディレクトリのパス
current_dirname = r'C:\Users\s-shunsuke.a.kuzawa\Desktop\tousin'
#current_dirname = r""
# 検索ワードを参照
ff = open('input.txt', 'r', encoding = 'utf-8')
word = ff.read()
# 検索ワードを取得
word_list = word.split()
ff.close()

# ヒットしたテキストファイルのURLの格納リスト
url_list = ['\n']
# ディレクトリ格納リスト
folder_list = ['']

cnt=0
while True:
    # 未参照のディレクトリが無ければ終了
    if len(folder_list) == 0:
        break
    else:
        # ディレクトリ名を取り出す
        dir_option = folder_list.pop(0)
        # ディレクトリ名＝＞ディレクトリパスにする
        dir_path = current_dirname + dir_option
        ##dir_path = dir_option
        # カレントディレクトリに移動
        print(dir_path)
        os.chdir(dir_path)
        # カレントディレクトリにあるテキストファイル名を全て取得
        txtfile = glob.glob('*.txt')
        # カレントディレクトリにあるディレクトリをパスとして全て取得
        files_path = [g for g in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path,g))]

        while True:
            if len(files_path) == 0:
                break
            else:
                child_files_dir = files_path.pop(0)
                # 取得したディレクトリをディレクトリ格納リストに格納
                folder_list.append(dir_option+"\\"+child_files_dir)
            
        for filename in txtfile:
            # input.txtは検索対象外
            if 'input.txt' in filename:
                continue
            # ファイル名＝＞ファイルパスにする
            file_path = os.path.join(dir_path, filename)
            # 検索ワードのリストのチェックリスト作成
            flag_list = [False]*len(word_list)
            # テキストファイルの情報取得
            with open(file_path,'rb') as f:
                b = f.read()
            # テキストファイルの文字コード取得
            str_encode = detect(b)
            type_encode = str_encode['encoding']
            # 文字コードが以下の時は読み取れないのでスルー
            if type_encode == 'Windows-1254' or type_encode == 'None':
                break
            # テキストファイルを読み取りで開く
            with open(file_path, encoding=type_encode,errors='ignore') as f:
                lines = f.readlines()
                # 行を取り出す
                for line in lines:
                    # 文字の一致をチェック
                    for i,word in enumerate(word_list):
                        
                        if word in line:
                            flag_list[i]=True
                # チェックリストがすべてTrueならテキストファイルを開く
                if all(flag_list):
                    subprocess.Popen(['explorer',file_path],shell=True)
                    url_list.append(file_path + '\n')
                    cnt += 1
            # 15件ヒットしたら終了        
            if cnt >= 15:
                break
        # 15件ヒットしたら終了  
        if cnt >= 15:
            break

# 検索件数によって表示する文言
mongon = []
if cnt == 0:
    mongon.append('\n お探しのキーワードが含まれるファイルは見つかりませんでした \n')
elif cnt >= 15:
    mongon.append('\n １５件以上ヒットしましたので、表示できていないファイルがございます\n')
else:
    cnt_str = str(cnt)
    mongon.append('\n 検索結果：'+cnt_str+'件')

#カレントディレクトリに移動
os.chdir(current_dirname)
ff = open('output.txt', 'a',encoding="utf-8")
# 文言を書き込み
ff.writelines(mongon)
# ヒットしたパスを書き込み
ff.writelines(url_list)
ff.close()
# テキストファイルに入力
subprocess.Popen(['explorer',current_dirname + '\output.txt'],shell=True)