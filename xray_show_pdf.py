
# coding: utf-8
# ver20210701
# change
# log と線形の自動切換え
# ファイル名変更（xray_show_pdf.pyに）

# In[1]:

import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.font_manager as fm

# 日本語出力対応
plt.rcParams['font.family'] = 'IPAexGothic'


# In[2]:

# ファイル指定
実験number ="006"
csv_name ="YYNo"+実験number+"_4pd.csv"

#CSVファイルをUTF-8形式で読み込む
df_score = pd.read_csv(csv_name,encoding = 'UTF8')
#dataを出力
# df_score[0:10]


# In[3]:

average_num=5
df_score["cps移動平均"]=df_score["cps"].rolling(average_num).mean().round(1)
df_score[0:10]


# In[5]:
# 表示データ抜き出し
x=df_score["2sita"]
y=df_score["cps"]
y_rolling=df_score["cps移動平均"]


# In[20]:
# グラフの作成、表示、保存（PDF）
# figureの初期化
fig = plt.figure()
# Figure内にAxesを追加()
ax = fig.add_subplot(111) 
ax.scatter(x, y, label="測定値")
ax.plot(x, y_rolling,color="r", label="移動平均")
ax.set_title("YYNo"+実験number)
ax.set_xlabel("2θ")
ax.set_ylabel("cps")
plt_mode = "nomal"
if df_score["cps移動平均"].max()>10000:
    ax.set_yscale('log')
    plt_mode ="log"

# 凡例の表示
plt.legend()

if plt_mode=="log":
    pp = PdfPages("YYNo"+実験number+"X線回折_log.pdf")
else:
    pp = PdfPages("YYNo"+実験number+"X線回折.pdf")
# figureをセーブする
pp.savefig()

# pdfファイルをクローズする。
pp.close()

plt.tight_layout()
plt.show()
plt.close()