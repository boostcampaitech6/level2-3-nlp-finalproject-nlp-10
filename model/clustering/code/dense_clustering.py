import pandas as pd
import os
import hdbscan
from collections import Counter
import time
import argparse

dataset_path = '../dataset'

parser = argparse.ArgumentParser(description="")
parser.add_argument("--make", default='False', type=str, help='make topic? False = read')
args = parser.parse_args()

if args.make == 'True':
    print("make_Topic")
    dataset = pd.read_csv(os.path.join(dataset_path, "add_embedding_Sum_FIN_NEWS_SUMMARY.csv"))
    embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), dataset['embedding'].tolist()))
    
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
        
        return docs_df, Counter(cluster.labels_)

    start_time = time.time()
    docs_df, cluster_labels = hdbscan_process(dataset, 
                            embeddings,
                            method='leaf',    #가장 높은 밀도
                            min_cluster_size=3,
                            min_samples=3,
                            )

    elapsed_time = time.time() - start_time
    print(f'duration : {elapsed_time}s\n')
    docs_df.to_csv(os.path.join(dataset_path,'add_Topic.csv'))

else:
    print("read_TopicData")
    docs_df = pd.read_csv(os.path.join(dataset_path, 'add_Topic.csv'))
    cluster_labels = Counter(docs_df['Topic'].to_list())
    embeddings = list(map(lambda x : list(map(lambda y : float(y), x[1:-1].split(','))), docs_df['embedding'].tolist()))

times = docs_df['datetime'].unique()

print(f'\nstart ~ end : {times[0]} ~ {times[-1]}')
print(f'num_docs : {len(embeddings)}')

def check_numeric(input_str):
    try:
        num = int(input_str)
        return True
    except ValueError:
        return False

while(True):
    t_num = input(f'{cluster_labels}\nTopic_num (정수 아닌 입력 시 종료): ')
    if check_numeric(t_num):
        for idx in range(len(docs_df)):
            if docs_df['Topic'].iloc[idx] == int(t_num):
                print(f"{idx}: {docs_df['datetime'].iloc[idx]}")
                print(f"{docs_df['summary'].iloc[idx]}\n")

        # for idx in range(len(docs_df)):
        #     print(f"{docs_df[docs_df['Topic']==int(t_num)]['datetime'].iloc[idx]}")
        #     print(f"{docs_df[docs_df['Topic']==int(t_num)]['summary'].iloc[idx]}\n")

    else : break