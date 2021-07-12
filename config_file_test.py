# coding: utf-8
import configparser
# ファイルの存在チェック用モジュール
import os
import errno


# configparserの宣言とiniファイルの読み込み

config_ini = configparser.ConfigParser()
config_ini_path = 'config.ini'

# 指定したiniファイルが存在しない場合、エラー発生
if not os.path.exists(config_ini_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
# 読み込み
config_ini.read(config_ini_path, encoding='utf-8')

read_default = config_ini['DEFAULT']
var4 = read_default.get('User')

print('var4 :', var4)