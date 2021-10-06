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
# typ = [('CSVファイル','*.csv')] 
typ = [('DATファイル','*dat')] 
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
csv_name = fle
print("読み込みファイル:",fle)
print(os.path.splitext(os.path.basename(fle))[0])
実験number =re.findall(r"\d+", os.path.splitext(os.path.basename(fle))[0])[0]
file_name =(os.path.splitext(os.path.basename(fle))[0])
# csv_name ="YYNo"+実験number+"_4pd.csv"