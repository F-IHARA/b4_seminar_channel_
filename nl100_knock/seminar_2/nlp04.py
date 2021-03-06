# -*- coding: utf-8 -*-
"""NLP04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19rIq4uy48ZeJcz2kiFZO_ZPikaeNupZz
"""

# 30 下川
import MeCab
with open("neko.txt") as file:
    text = file.read()
    mecab = MeCab.Tagger("-Ochasen")
    mecab_text = mecab.parse(text)
    with open("neko.txt.mecab", mode="w") as write_file:
        write_file.write(mecab_text)

morpheme_list = [[]]
with open('neko.txt.mecab') as file:
    lines = file.readlines()
    # 行数
    count = 0
    
    for line in lines:
        word = line.split('\t')
        # 表層形しかないものがあったため長さで変えた
        if len(word) < 2:
            continue
        if word[3]:
            pos = word[3].split('-')
            if len(pos)==1:
                pos.append(None)
        else:
            pos = [None, None]
        morpheme = {
            'surface' : word[0],
            'base' : word[2],
            'pos' : pos[0],
            'pos1' : pos[1]
        }
        morpheme_list[count].append(morpheme)
        # １行ごとにリストに入れる
        if word[0] == "。":
            morpheme_list.append([])
            count+=1
print(morpheme_list[:5])

# 31 下川
verb_surface = []
for words in morpheme_list:
    for word in words:
        if word["pos"] == "動詞":
            verb_surface.append(word["surface"])
print(verb_surface)

#34 田嶋

with open('neko.txt.mecab', 'r', encoding='utf-8') as f:
    #行数が多いので1文ずつ
    for line in f:
        cols1 = line.split('\t')
        if(len(cols1) < 2):
            break
        cols2 = cols1[1].split(',')
        dic = {'surface': cols1[0], 'base': cols2[6], 'pos': cols2[0], 'pos1': cols2[1]}
        word_list.append(dic)

noun_sequence = []
            
noun = ''            
for word in word_list:
    if word['pos'] == '名詞':
        noun += word['surface']
    else:
        if noun != '':
            noun_sequence.append(noun)
            noun = ''
      
print(noun_sequence)

#35　田嶋

from collections import Counter
word_frequency= []
word_counter = Counter()

for word in word_list:
    word_frequency.append(word['surface'])
        
c = Counter(word_frequency)
print(c.most_common())

#37 岸本

import codecs #UnicodeDecodeError回避用
import re
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

def data_to_list(data): #MeCabデータを１行ごと（形態素ごと）にリスト化する
    data = [data,""][int("EOS" in data)].strip("\n") #EOSを省く　&　改行記号を省く
    return re.split("\t|,",data) #区切ってリストに

def list_to_dic(list): #形態素ごとに作られるリストからsurface,base,pos,pos1を辞書として取り出す
    return {"surface":list[0],"base":list[7],"pos":list[1],"pos1":list[2]} if len(list) != 1 else None #リストの要素数が1のもの（文章の最後など）を省く

all_list = [] #全文の解析データを格納する場所
partial_list = [] #1文の解析データを格納する場所、all_listに加えたら新規作成する

with codecs.open("neko.txt.mecab","r","utf-8","ignore") as f: #utf-8以外の文字を無視できる
    for i , data in enumerate(f): #enumerate関数で解析結果を取り出す
        dic = list_to_dic(data_to_list(data)) #変換
        if type(dic) is dict: 
            partial_list.append(dic)
            if dic['surface'] in ("。","!","?","！","？","」","\u3000"): #「句点など＝１文終了の合図」☞　partial_listをall_listに加えた上で初期化する
                all_list.append(partial_list)
                partial_list = [] 
        else: #NoneTypeの処理
            all_list.append(partial_list)
            partial_list = [] 

all_list = [s for s in all_list if s != []] #all_list内の空のリストを削除


#問題の内容はここから
cat_freq_dict = {}
cat_all_list = []

for partial_list in all_list:
    for dic in partial_list:
        if dic["surface"] == "猫":
            cat_all_list.append(partial_list) #「猫」が含まれる文のみを抽出
            break

for partial_list in cat_all_list:
    partial_list = [dic for dic in partial_list if dic["pos"] != "記号" ] #記号を除去
    partial_list = [dic for dic in partial_list if dic["surface"] != "猫"] #「猫」を除去
    partial_list = [dic for dic in partial_list if dic["pos"] != "助詞" ] #助詞を除去
    partial_list = [dic for dic in partial_list if dic["pos"] != "助動詞" ] #助動詞を除去
    for dic in partial_list:
        if dic["surface"] in cat_freq_dict: #既出の単語ならば
            cat_freq_dict[dic["surface"]] += 1 #カウントする
        else:
            cat_freq_dict.update({dic["surface"]:1}) #新出の単語なら新規登録する

cat_freq = sorted(cat_freq_dict.items(), key=lambda x:x[1], reverse=True) 

left = np.array(["             "]*10)
height = np.array([0]*10)

for i in range(10):
    left[i] = cat_freq[i][0]
    height[i] = cat_freq[i][1]

plt.bar(left, height)
plt.title("「猫」と共起頻度の高い上位10語")
plt.xlabel("「猫」と共起頻度の高い語")
plt.ylabel("出現頻度")
plt.show()

#39 岸本

freq_dict = {}

for partial_list in all_list:
    partial_list = [dic for dic in partial_list if dic["pos"] != "記号"] #記号を除去
    for dic in partial_list:
        if dic["surface"] in freq_dict: #既出の単語ならば
            freq_dict[dic["surface"]] += 1 #カウントする
        else:
            freq_dict.update({dic["surface"]:1}) #新出の単語なら新規登録する

#key,value共に表示するのでitems()でタプル化、keyにlambda x:x[1]を入れることでvalueでソート可能に、reverse=Trueで降順にする
freq = sorted(freq_dict.items(), key=lambda x:x[1], reverse=True) 


#問題の内容はここから
left = np.array([0]*len(freq))
height = np.array([0]*len(freq))

for i in range(len(freq)):
    left[i] = i+1 #順位
    height[i] = freq[i][1]

plt.plot(left, height)
plt.xscale('log') #両対数
plt.yscale('log') #両対数
plt.title("Zipfの法則")
plt.xlabel("単語の出現頻度順位")
plt.ylabel("出現頻度")
plt.show()