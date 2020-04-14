# encoding=utf-8
import jieba
import json
with open("data/questions.json",'rb') as f:
    questions = json.load(f)
question1 = questions[0]
strs=list(question1['problems'].values())
for str in strs:
    seg_list = jieba.cut(str) # 使用paddle模式
    print("Default Mode: " + '/'.join(list(seg_list)))