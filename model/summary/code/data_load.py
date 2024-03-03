import torch
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import json

def load_dataset(path):
    columns = ['passage_id', 'passage', 'summary']
    total_df = pd.DataFrame(columns = columns)
    file_list = os.listdir(path)
    
    for file in tqdm(file_list, desc = f"read_data "):
        file_path = os.path.join(path, file)
        if file.endswith('.json'):
            with open(file_path, encoding='UTF-8') as  f:
                data = json.load(f)
    
            data = {k:[v] for k,v in data.items() if k in columns}
            data = pd.DataFrame(data)
        
        total_df = pd.concat([total_df, data], ignore_index=True)

    return total_df