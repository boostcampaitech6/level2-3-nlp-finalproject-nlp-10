import sklearn
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import pandas as pd
import rank_bm25
from rank_bm25 import BM25Okapi
from sklearn.preprocessing import StandardScaler
from konlpy.tag import Okt, Hannanum, Kkma

#news = pd.read_csv('news.csv')
news = pd.read_csv('samsung_feb.csv')
print(news.head())

#news = news[:1000]
print(len(news))
news_contexts = news['contents']
print(f'{len(news_contexts)=}')

from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

model_name = "ainize/kobart-news"

tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
okt=Okt()
model = BartForConditionalGeneration.from_pretrained(model_name)

cnt=0
idx=[]
for i in range(len(news_contexts)):
  #tokens=tokenizer.tokenize(news_contexts[i])
  tokens=okt.morphs(news_contexts[i])
  if len(tokens)>512:
    cnt+=1
    idx.append(i)

print(cnt)
print(idx)

import re

news_contexts = news['contents']
print(news_contexts[956])

def remove_space(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+', '', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    return text

# 따옴표 제거
def remove_quote(text):
    text = re.sub(r'\'', ' ', text)
    text = re.sub(r'\`', ' ', text)
    text = re.sub(r'\‘', ' ', text)
    text = re.sub(r'\’', ' ', text)

    text = re.sub(r'\"', ' ', text)
    text = re.sub(r'\“', ' ', text)
    text = re.sub(r'\”', ' ', text)
    return text

# () 괄호 안 제거
def remove_between_round_brackets(text):
    return re.sub(r'\([^)]*\)', ' ', text)

# {} 괄호 안 제거
def remove_between_curly_brackets(text):
    return re.sub(r'\{[^}]*\}', ' ', text)

# [] 괄호 안 제거
def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', ' ', text)

# <> 괄호 안 제거
def remove_between_angle_brackets(text):
    return re.sub(r'\<[^>]*\>', ' ', text)

# url 제거
def remove_url(text):
    text = re.sub(r'http[s]?://(?:[\t\n\r\f\v]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    text = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', ' ', text)
    return text

# 이메일 제거
def remove_email(text):
    return re.sub(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',' ', text)

# 날짜 제거
def remove_date(text):
    return re.sub(r'\d+[.]\d+[.]\d+',' ', text)

# 숫자 이용 문자 제거
def remove_number_text(text):
    text = re.sub(r'[0-9]+%', ' ', text)
    text = re.sub(r'[0-9]+층', ' ', text)
    return text

# 특수문자 제거
def remove_symbol(text):
    return re.sub(r'[^\w\s.,]', ' ', text)

# 자음, 모음 제거
def remove_consonants_vowels(text):
    text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ]+', ' ', text)
    return text

# 앞에 날리기
def remove_to_callback(news):
    callback_list = []
    try :
        for b in re.finditer('flash_removeCallback()',news):
            callback_list.append(b.end())
        news = news[callback_list[0]:]
    except :
        news = news
    return news

# 뒤에 날리기
def remove_from_back_third_triangle(news):
    triangle_list = []
    for a in re.finditer('▶',news):
        triangle_list.append(a.start())
    if len(triangle_list) >= 3:
        news = news[:triangle_list[-3]]
    elif len(triangle_list) == 2:
        news = news[:triangle_list[-2]]
    elif len(triangle_list) == 1:
        news = news[:triangle_list[-1]]
    return news

def remove_float(news):
    return re.sub(r'[0-9]+.[0-9]*',' ', news)

def remove_journalist(news):
    return re.sub(r'[가-핳]{2,4}\s+기자[^가-핳]+',' ', news)

def remove_points(text):
    text = re.sub(r'[.]{2,}', '.', text) 
    text = re.sub(r'[,]{2,}', ',', text) 
    text = re.sub(r'[.,]{2,}', '.', text) 
    return text

def pre_processing(txt):
    txt = remove_to_callback(txt)
    txt = remove_from_back_third_triangle(txt)
    txt = remove_email(txt)
    #txt = remove_date(txt)
    txt = remove_quote(txt)
    txt = remove_url(txt)
    txt = remove_number_text(txt)
    txt = remove_consonants_vowels(txt)
    txt = remove_between_round_brackets(txt)
    txt = remove_between_curly_brackets(txt)
    txt = remove_between_square_brackets(txt)
    txt = remove_between_angle_brackets(txt)
    txt = remove_journalist(txt)
    txt = remove_float(txt)
    txt = remove_symbol(txt)
    txt = remove_points(txt)
    txt = remove_space(txt)
    return txt

news_contexts = list(map(pre_processing, news_contexts))

"""#TF-IDF"""

#tfidf_vectorizer = TfidfVectorizer(tokenizer = tokenizer.tokenize, min_df = 3, ngram_range=(1,3))
tfidf_vectorizer = TfidfVectorizer(tokenizer = okt.morphs, min_df = 3, ngram_range=(1,2))
tfidf_vectorizer.fit(news_contexts)
context_vector = tfidf_vectorizer.transform(news_contexts).toarray()

# scaler = StandardScaler()
# context_vector = scaler.fit_transform(context_vector)
# print(tfidf_vectorizer.vocabulary_)

print(len(context_vector[8]))

"""#BM-25"""

# tokenized_corpus = [okt.morphs(c) for c in news_contexts]
# bm25 = BM25Okapi(tokenized_corpus)

# print(len(bm25.get_scores(tokenized_corpus[0])))

#context_vector = [bm25.get_scores(c) for c in tokenized_corpus]

scaler = StandardScaler()
context_vector = scaler.fit_transform(context_vector)
print(tfidf_vectorizer.vocabulary_)

print(type(context_vector))
print(len(context_vector))
print(len(context_vector[0]), len(context_vector[100]), len(context_vector[1000]))

model = DBSCAN(eps=0.6, min_samples=3, metric = "cosine")
result = model.fit_predict(context_vector)
train_extract={}
train_extract['cluster1st'] = result

print('군집개수 :', result.max())
train_extract

print(result[51])

from collections import Counter
counter = Counter(result)
print(sorted(counter.items(), reverse=True, key = lambda x: x[1]))

#for i,_ in sorted(counter.items(), reverse=True, key = lambda x: x[1]):

for i, c in enumerate(result):
  if c==27:

    print('idx:', i,'  -> ', news_contexts[i])
    #print('length :',len(tokenizer.tokenize(news_contexts[i])))
    print('length :',len(okt.morphs(news_contexts[i])))
    print()



for i, c in enumerate(result[:5000]):
  if c==59:

    print('idx:', i,'  -> ', news_contexts[i])
    print('length :',len(tokenizer.tokenize(news_contexts[i])))
    print()

