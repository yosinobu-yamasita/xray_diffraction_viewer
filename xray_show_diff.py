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
plt_Y_mode= read_default.get('PltMode')
if plt_Y_mode!="all":
    # plt_y_limit = read_default.getint("PltYLimit")
    plt_y_limit_xmax = read_default.getint("PltYLimit_Xmax")
    plt_y_limit_xmin = read_default.getint("PltYLimit_Xmin")
    
log_min_limit= read_default.getint('LogLimit')
base_fle = read_default.get("BaseFile")

# ベースファイル指定
typ = [('DATファイル','*dat')] 
# base_fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir, title="base file") 
base_csv_name = base_fle
print("読み込みベースファイル:",base_fle)
base_file_name =(os.path.splitext(os.path.basename(base_fle))[0])

# ファイル指定
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
csv_name = fle
print("読み込みファイル:",fle)
file_name =(os.path.splitext(os.path.basename(fle))[0])

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# 日本語出力対応
plt.rcParams['font.family'] = 'MS Gothic'

#CSVファイルをUTF-8形式で読み込む
base_df_score = pd.read_csv(base_csv_name, encoding = 'UTF8', engine='python', names=("2sita", "cps"), sep="   ")
df_score = pd.read_csv(csv_name, encoding = 'UTF8', engine='python', names=("2sita", "cps"), sep="   ")
#dataを出力
# df_score[0:10]

# 移動平均を作成
base_df_score["cps移動平均"]=df_score["cps"].rolling(average_num).mean().round(1)
df_score["cps移動平均"]=df_score["cps"].rolling(average_num).mean().round(1)
# df_score[0:10]

# baseとの差分を作成
df_score["cps_base_diff"]= df_score["cps"]-base_df_score["cps"]
# 表示データ抜き出し
x=df_score["2sita"]
y=df_score["cps"]
y_rolling=df_score["cps移動平均"]
y_diff= df_score["cps_base_diff"]

# グラフの作成、表示、保存（PDF）
# 6.4、4.8
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111) 
# ax.scatter(x, y, label="測定値")
ax.scatter(x, y_diff, label="測定値-base")
ax.plot(x, y_rolling,color="r", label=str(average_num)+"データ移動平均")
ax.set_title(file_name)
ax.set_xlabel("2θ")
ax.set_ylabel("cps")
plt.legend()
plt.grid()


# 表示の調整
plt_mode = "nomal"
pdf_name= file_name+"_X線回折_diff.pdf"
ax.set_xlim(20,30)
if df_score["cps移動平均"].max()>log_min_limit:
    ax.set_yscale('log')
    plt_mode ="log"
    pdf_name= file_name+"_X線回折_log_diff.pdf"

if (plt_Y_mode !="all")and("plt_y_limit_xmax" in locals()):
    plt_y_limit_xmax_num = min(int((plt_y_limit_xmax-df_score["2sita"][0])/0.02),len(df_score["2sita"]))
    plt_y_limit_xmin_num = max(int((plt_y_limit_xmin-df_score["2sita"][0])/0.02),0)
    ax.set_ylim(-50,df_score["cps"][plt_y_limit_xmin:plt_y_limit_xmax_num].max()*1.1)


# figureをセーブする
pp = PdfPages(os.path.dirname(fle)+"/"+pdf_name)
pp.savefig()
pp.close()
print("グラフPDF保存:",pdf_name)

# 終了処理
plt.show()
plt.close()