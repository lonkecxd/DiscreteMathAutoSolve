# encoding=utf-8
import jieba
import json
import jieba.analyse
import jieba.posseg as pseg
# import pyhanlp
import dialogflow_v2


def get_propositions(words_with_tags):
    users = filter(lambda x:x[1]=='PER',list(words_with_tags))
    propositions = []
    proposition = ''
    for word, tag in words_with_tags:
        if tag=='a' or tag=='n':
            proposition += word
            propositions.append(proposition)
            proposition = ''
        elif tag=='v':
            proposition += word
    return propositions

with open("data/db.json",'rb') as f:
    data = json.load(f)
questions = data['problems']
question1 = questions[0]
strs=list(question1['questions'].values())
jieba.enable_paddle()
jieba.load_userdict("data/userdict.txt")
# analyzer = PerceptronLexicalAnalyzer()
for str in strs:
    words1 = pseg.cut(str, use_paddle=True)
    for word, flag in words1:
        if flag in ['PER', 'n', 'nr', 'ng', 'nrfg', 'nrt', 'ns', 'nt', 'nz']:
            jieba.add_word(word, freq=10000, tag=flag)

    seg_list = jieba.cut(str)
    print("Default Mode: " + '/'.join(list(seg_list)))

    users = []
    propositions = []
    ops = []  # operations
    op = ''
    words = pseg.cut(str)
    preps = []
    conjs = []
    advs = []
    for word, flag in words:
        # if flag in ['ns', 'nr','a','n','v','vn','vd','i','PER']:
        print('%s %s' % (word, flag))
        if flag=='PER':
            users.append(word)
        elif flag == 'a' or flag == 'n':
            op += word
            ops.append(op)
            op = ''
        elif flag == 'v':
            op += word
        elif flag == 'p':
            preps.append(word)
        elif flag == 'c':
            conjs.append(word)
        elif flag == 'd':
            advs.append(word)
    for u in users:
        for o in ops:
            propositions.append(u+o)
            proposition = ''
    print(propositions)
    print(preps)
    print(conjs)
    print(advs)
    # kw = jieba.analyse.extract_tags(str, topK=20, withWeight=True, allowPOS=('ns', 'nr','n','a','v','vn','vd','d','i'))
    # for item in kw:
    #     print(item[0], item[1])
