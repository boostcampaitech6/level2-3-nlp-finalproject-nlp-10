import pandas as pd
import os
from sklearn.cluster import DBSCAN
import hdbscan
from collections import Counter
import time
import argparse
import re

dataset_path = '../dataset'

parser = argparse.ArgumentParser(description="")
parser.add_argument("--make_cluster", default='False', type=str, help='False = read')   #클러스터링을 할지 원래있던 클러스터링데이터를 읽을지
parser.add_argument("--make_file", default='False', type=str, help='make topic?')   #토픽 추가한 데이터를 만들지
args = parser.parse_args()

# HDBSCAN 실행
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
    
    return docs_df

def check_numeric(input_str):
    try:
        num = int(input_str)
        return True
    except ValueError:
        return False

def check_cluster(docs_df):     #요기요기요기!!!!!!
    while(True):
        t_num = input(f"{Counter(docs_df['Topic'].to_list())}\nTopic_num (정수 아닌 입력 시 종료): ")
        if check_numeric(t_num):
            for idx in range(len(docs_df)):
                if docs_df['Topic'].iloc[idx] == int(t_num):
                    print(f"{idx}: {docs_df['datetime'].iloc[idx]}")
                    print(f"{docs_df['summary'].iloc[idx]}\n")

            # for idx in range(len(docs_df)):
            #     print(f"{docs_df[docs_df['Topic']==int(t_num)]['datetime'].iloc[idx]}")
            #     print(f"{docs_df[docs_df['Topic']==int(t_num)]['summary'].iloc[idx]}\n")

        else : break

def check_date_format(date_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date_string):
        return True
    else:
        return False


if args.make_cluster == 'True' or 'true':
    print("make_Topic")
    dataset = pd.read_csv(os.path.join(dataset_path, "add_embedding_Sum_FIN_NEWS_SUMMARY.csv"))
    while(True):
        selected_date = input(f'클러스터링 할 날짜(예시 : 2024-02-23, 전체는 \'All\'입력):')

        if check_date_format(selected_date):
            sub_dataset = dataset[pd.to_datetime(dataset['datetime']).dt.date == pd.to_datetime(selected_date).date()]
            sub_dataset = sub_dataset[sub_dataset['relate_stock'].apply(lambda x: '삼성전자' in x)]#############

        elif selected_date=='All':
            sub_dataset = dataset

        else :break

        embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), sub_dataset['embedding'].tolist()))

        start_time = time.time()

        while(True):
            c_algo = input('(\'hdb\' : HDBSCAN, \'db\' : DBSCAN) :')
            if c_algo == 'hdb' or 'HDB' or 'db' or 'DB':
                break
            else: print(f'ektl 입력해주세요.')

        #c_algo = 'db'

        if c_algo=='hdb':
            docs_df = hdbscan_process(sub_dataset, 
                                    embeddings,
                                    #method='leaf',    #가장 높은 밀도
                                    min_cluster_size=2,
                                    min_samples=4,
                                    )
            
        elif c_algo=='db':
            c_model = DBSCAN(eps=0.2, min_samples=2, metric = "cosine")
            result = c_model.fit_predict(embeddings)
            sub_dataset['Topic']=result
            docs_df = sub_dataset

        elapsed_time = time.time() - start_time
        print(f'duration : {elapsed_time}s\n')
        
        if args.make_file == 'True':docs_df.to_csv(os.path.join(dataset_path,'add_Topic.csv'))

        times = docs_df['datetime'].unique()

        print(f'start ~ end : {times[0]} ~ {times[-1]}')
        print(f'num_docs : {len(embeddings)}')

        check_cluster(docs_df)

else:
    print("read_TopicData")
    docs_df = pd.read_csv(os.path.join(dataset_path, 'add_Topic.csv'))
    cluster_labels = Counter(docs_df['Topic'].to_list())
    embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), docs_df['embedding'].tolist()))

    times = docs_df['datetime'].unique()

    print(f'\nstart ~ end : {times[0]} ~ {times[-1]}')
    print(f'num_docs : {len(embeddings)}')

    check_cluster(docs_df)