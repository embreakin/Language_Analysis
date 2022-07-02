#必要なライブラリのインポート

from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)

import re
import numpy as np
import matplotlib.pyplot as plt

#--------------------------------------------

#このリストは言語解析ファイルの言語の列順に対応しているので書き換えてはいけない
LangAlphabets = ['E', 'C', 'F', 'S', 'G', 'SW', 'K', 'IN', 'A', 'R', 'H', 'I', 'P', 'J']

#この辞書は出力の順番に対応するものなので好きなように並べ替えて良い
LangNameDict = {'Japanese' : 'J', 'English' : 'E', 'German': 'G', 'French' : 'F', 'Spanish' : 'S', 'Chinese': 'C', 'Korean' : 'K', 'Italian' : 'I', 'Russian': 'R', 'Portuguese' : 'P', 'Arabic' : 'A', 'Hindi': 'H', 'Indonesian': 'IN', 'Swedish': 'SW' }

#--------------------------------------------
#各言語ファイルの行数を取得することで現時点での最新の各言語の語彙数をまず出力し確認

print('Current Number of Words Learned for Each Language')
for i in range(len(LangNameDict)):
  ss_name = list(LangNameDict.values())[i] + "Words"
  workbook = gc.open(ss_name)
  worksheet = workbook.worksheet("Sheet1")
  rownumber=len(worksheet.col_values(1))
  print("#", i+1, ": ", list(LangNameDict.keys())[i], rownumber)

print()
#--------------------------------------------
#言語解析ファイルの各言語の時系列データを図示

#年/月/日をシートから取得しリストを作成
name = "Language_Analysis"
LAworkbook = gc.open(name)
LAworksheet = LAworkbook.worksheet("Sheet1")
Datelist = LAworksheet.col_values(1)#シートの一列目取得
Datelist.pop(0) #0成分抽出
Date = []
for element in Datelist:
  # 正規表現ではバックスラッシュ (\) などの特殊文字をよく使うので、文字列の前に r を付けて生文字列 (raw string) にする
  element = re.search(r'.+/.+/.+:', element).group()[0:-1]
  Date.append(element)#Dateは年/月/日のリスト

#日にちのリストと同じ長さの整数のリストを作る。これをプロットに用いる。
DateNumberList = list(range(0, len(Date)))

#x軸目盛りに必要なリストを作成
XTicksNumberList = []#各月の初日のインデックスのリスト
XTicksLabelList = []#各月の初日の年/月/日のリスト
MItemList = []#/月/のリスト
for MIndex, MItem in enumerate(Date):
  MItem = re.search(r'/.+/', MItem).group()#/月/を取得
  if (MIndex == 0) or (MIndex == len(Date)-1):#最初と最後の年/月/日は必ずリストに含めるとする
    XTicksNumberList.append(MIndex)
    XTicksLabelList.append(Date[MIndex])
    MItemList.append(MItem)
  elif MItem != MItemList[MIndex-1]:#それ以外は月の初めだけリストに含める
    MItemList.append(MItem)
    if (MIndex < 10) or ((len(Date)-1) - MIndex < 10 ):#ただし最初と最後の年/月/日と月の初日の差が10日未満の時は目盛りが被って見にくくなるので除くべき。
      continue
    XTicksNumberList.append(MIndex)
    XTicksLabelList.append(Date[MIndex])
  else:
    MItemList.append(MItem)
  
#描画領域全体の指定
fig = plt.figure(figsize=(24,16), dpi=120, facecolor = "darkgray") 
fig.suptitle("Number of Words Learned for Each Language", fontsize = 25, x=0.5, y=0.95)
# 余白を設定
plt.subplots_adjust(wspace=0.2, hspace=0.6)#デフォルトは共に0.2

#言語解析ファイルの各言語の時系列データをまずLanglistAllに入れ二次元配列作成
LanglistAll = []
for i in range(len(LangAlphabets)):
  LanglistEach = LAworksheet.col_values(i+2)
  LanglistEach.pop(0)#0成分を抽出&除去
  LanglistEach = [int(s) for s in LanglistEach]#データをstrからintに全て変換
  LanglistAll.append(LanglistEach)

#サブプロットをforループにより図示していく
MaxYticksIntervalNumber = 10 # サブプロットのy軸の目盛りの間隔の最大数を設定
for i in range(len(LangNameDict)):
  plotname = "ax" + str(i)
  plotname  = fig.add_subplot(4, 4, i+1)
  LAIndex = LangAlphabets.index(list(LangNameDict.values())[i]) #LangNameDictの値('J"など)に対応するLangAlphabetsの要素のインデックスを取得
  plotname.plot(DateNumberList, LanglistAll[LAIndex], marker="o", color = "red", linestyle = "-", markersize=3)
  plotname.set_title(list(LangNameDict.keys())[i], fontsize = 15)#各サブプロットのタイトル
  #x軸の目盛り
  plotname.set_xticks(XTicksNumberList)
  plotname.set_xticklabels(XTicksLabelList, rotation=45)
  #y軸の目盛りをプロット毎に調整する
  start = LanglistAll[LAIndex][0]
  stop = LanglistAll[LAIndex][-1]
  step = (stop - start) / MaxYticksIntervalNumber
  if step == 0:
    plotname.set_yticks( [start] )#y軸のデータが一つの時はstep=0になるので場合分けする
  elif step <= 5:
    midpoint = (start+stop) // 2
    plotname.set_yticks( [start, midpoint , stop] ) #ステップサイズが小さい時は場合分けし３点だけ目盛りをふる
  else:
    plotname.set_ylim(start, stop)
    list_rd = list(map(round, np.arange(start, stop+step, step))) #目盛りは四捨五入する
    plotname.set_yticks( list_rd )

#ファイル保存
plt.savefig("LA.png") 
