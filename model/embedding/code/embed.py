from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import pandas as pd
import os

dataset_path = "../dataset"
file_list = os.listdir(dataset_path)
name_end = "RY.csv"

model = SentenceTransformer('leewaay/kpf-bert-base-klueNLI-klueSTS-MSL512').to("cuda")
model.eval()

for file_name in file_list:
    if not file_name.endswith(name_end):
            continue
    
    df = pd.read_csv(os.path.join(dataset_path, file_name))

    embeddings = model.encode(df['summary'])

    e_df = pd.DataFrame({'embedding':embeddings.tolist()})
    new_df = pd.concat([df, e_df], axis=1)

    new_df.to_csv("../../clustering/dataset/add_embedding_"+file_name, index=False)
    print("save finish")
    print(new_df.head())
