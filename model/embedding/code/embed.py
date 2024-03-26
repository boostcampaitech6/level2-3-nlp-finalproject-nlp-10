from sentence_transformers import SentenceTransformer
import pandas as pd
import os
import time

dataset_path = "../dataset"
file_list = os.listdir(dataset_path)
name_end = ".csv"

model = SentenceTransformer('leewaay/kpf-bert-base-klueNLI-klueSTS-MSL512').to("cuda")
model.eval()

start_time = time.time()
for file_name in file_list:
    if not file_name.endswith(name_end):
        continue
    
    df = pd.read_csv(os.path.join(dataset_path, file_name))

    embeddings = model.encode(df['summary']).tolist()
    df['embedding'] = embeddings
    new_df = df
    new_df.head()

duration = time.time()-start_time

print(f'data_len : {len(new_df)}')
print(f'{duration=}')
new_df.to_csv("../../clustering/dataset/no_topic/add_embedding_"+file_name, index=False)
print("save finish")
print(new_df.head())
