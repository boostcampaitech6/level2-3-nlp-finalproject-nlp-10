#클러스터끼리의 코사인 시밀러리티 확인
import pandas as pd
import numpy as np
import os
from sklearn.cluster import DBSCAN
import hdbscan
from collections import Counter, defaultdict
import time
import argparse
import re
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity

dataset_path = '../dataset'
no_topic_path = os.path.join(dataset_path, 'no_topic')
file_name = "add_embedding_Sum_FIN_NEWS_SUMMARY.csv"
file_path = os.path.join(no_topic_path, file_name)

def hdbscan_process(corpus, corpus_embeddings, min_cluster_size=3, min_samples=3, method='eom'):
    cluster = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size,
                            min_samples=min_samples,
                            metric='euclidean',
                            allow_single_cluster=True,
                            cluster_selection_method=method,
                            ).fit(corpus_embeddings) #eom leaf

    docs_df = corpus
    docs_df['Topic'] = cluster.labels_
    #print(Counter(cluster.labels_), '\n')
    
    return docs_df, cluster.labels_

def dbscan_process(dataset, corpus_embeddings, eps=0.2, min_samples=2):
    c_model = DBSCAN(eps=0.2, min_samples=min_samples, metric = "cosine")
    result = c_model.fit_predict(corpus_embeddings)
    dataset['Topic']=result
    docs_df = dataset
    return docs_df, result

def check_numeric(input_str):
    try:
        num = int(input_str)
        return True
    except ValueError:
        return False

def check_cluster(docs_df):
    while(True):
        t_num = input(f"{Counter(docs_df['Topic'].to_list())}\nTopic_num (정수 아닌 입력 시 종료): ")
        if check_numeric(t_num):
            for idx in range(len(docs_df)):
                if docs_df['Topic'].iloc[idx] == int(t_num):
                    print(f"{idx}: {docs_df['datetime'].iloc[idx]}")
                    print(f"{docs_df['summary'].iloc[idx]}\n")

        else : break

def check_date_format(date_string):
    pattern = r'^\d{4}-\d{2}-\d{2}'
    if re.match(pattern, date_string):
        return True
    else:
        return False
    
def cluster_mean_embedding(docs_df):
    """클러스터들 평균 엠베딩 만들기(-1 제외)"""
    cluster_embedding = defaultdict(list)
    for idx in range(len(docs_df)):
        curr_cluster = docs_df['Topic'][idx]
        if curr_cluster != -1:
            cluster_embedding[curr_cluster].append(docs_df['embedding'][idx])
        
    for k in sorted(cluster_embedding.keys()):
        cluster_embedding[k] = np.mean(cluster_embedding[k], axis=0)
        print(f"{k} : {cluster_embedding[k].shape}")

    c_emb_df = pd.DataFrame(cluster_embedding)  #클러스터 하나당 엠베딩을 따로 저장하려면
    return c_emb_df
    """"""

data_df = pd.read_csv(file_path)
prev_time = "2024-1-8 00:00:00"
prev_time = datetime.strptime("2024-1-8", "%Y-%m-%d %H:%M:%S")
curr_time = prev_time + timedelta(days=0,hours=0,minutes=10)
curr_time = curr_time.replace(hour=8, minute=0, second=0)
data_df['datetime'] = data_df['datetime'].apply(lambda x: datetime.srtptime(x, "%Y-%m-%d %H:%M:%S"))

prev_df = data_df[data_df['datetime']<=prev_time].reset_index(drop=True)
curr_df = data_df[(data_df['datetime'].date()==curr_time.date()) and (data_df['datetime']<=curr_time)].reset_index(drop=True)

prev_embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), prev_df['embedding'].tolist()))
prev_df['embedding'] = prev_embeddings
curr_embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), curr_df['embedding'].tolist()))
curr_df['embedding'] = curr_embeddings

prev_df, prev_result = hdbscan_process(
                            prev_df,
                            prev_embeddings,
                            method='leaf',    #가장 높은 밀도
                            min_cluster_size=3,
                            min_samples=3,
                            )
curr_df, curr_result= dbscan_process(curr_df, curr_df['embedding'], eps=0.3, min_samples=2)

prev_cluster_emb_df = cluster_mean_embedding(prev_df)  #기존 데이터들의 클러스터들(0~)에 대해 평균 임베딩 생성
curr_cluster_emb_df = cluster_mean_embedding(curr_df)  #새로운 데이터들의 클러스터들(0~)에 대해 평균 임베딩 생성



