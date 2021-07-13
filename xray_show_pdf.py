# coding: utf-8
from tkinter import filedialog
import os
import re
import configparser
import errno

# configparserの宣言とiniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini_path = 'config.ini'
if not os.path.exists(config_ini_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
config_ini.read(config_ini_path, encoding='utf-8')

read_default = config_ini['YAMASITA']
dir = read_default.get('Dir')
average_num= read_default.getint('MoveAve')
log_min_limit= read_default.getint('LogLimit')

# ファイル指定
typ = [('CSVファイル','*.csv')] 
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
csv_name = fle
print("読み込みファイル:",fle)
実験number =re.findall(r"\d+", os.path.splitext(os.path.basename(fle))[0])[0]
# csv_name ="YYNo"+実験number+"_4pd.csv"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# 日本語出力対応
plt.rcParams['font.family'] = 'IPAexGothic'

#CSVファイルをUTF-8形式で読み込む
df_score = pd.read_csv(csv_name,encoding = 'UTF8',engine='python')
#dataを出力
# df_score[0:10]

# 移動平均を作成
df_score["cps移動平均"]=df_score["cps"].rolling(average_num).mean().round(1)
# df_score[0:10]

# 表示データ抜き出し
x=df_score["2sita"]
y=df_score["cps"]
y_rolling=df_score["cps移動平均"]

# グラフの作成、表示、保存（PDF）
fig = plt.figure()
ax = fig.add_subplot(111) 
ax.scatter(x, y, label="測定値")
ax.plot(x, y_rolling,color="r", label=str(average_num)+"データ移動平均")
ax.set_title("YYNo"+実験number)
ax.set_xlabel("2θ")
ax.set_ylabel("cps")
plt.legend()
plt.grid()

# 表示の調整
plt_mode = "nomal"
pdf_name= "YYNo"+実験number+"_X線回折.pdf"
if df_score["cps移動平均"].max()>log_min_limit:
    ax.set_yscale('log')
    plt_mode ="log"
    pdf_name= "YYNo"+実験number+"_X線回折_log.pdf"

# figureをセーブする
pp = PdfPages(os.path.dirname(fle)+"/"+pdf_name)
pp.savefig()
pp.close()
print("グラフPDF保存:",pdf_name)

# 終了処理
plt.show()
plt.close()