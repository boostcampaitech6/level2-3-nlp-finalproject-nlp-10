import torch
from torch.utils.data import TensorDataset
from tqdm import tqdm

def make_dataset(tokenizer, input_data, target_data):
    print("\nmake_dataset")
    max_seq_length = 1024
    doc_stride = 128
    i_input_ids, i_attention_mask, i_token_type_ids = [], [], []
    t_input_ids, t_attention_mask, t_token_type_ids = [], [], []
    i_overflow_mapping = []

    for data in tqdm(input_data.to_list(), desc=f"input data toknizing "):
        input_token = tokenizer(
                            data, 
                            max_length= max_seq_length,
                            padding="max_length",
                            #return_tensors='pt',
                            truncation=True,
                            # stride = doc_stride,
                            # return_overflowing_tokens=True,
                            # return_token_type_ids=False,
                            )
        
        i_input_ids.append(input_token['input_ids'])    #return_overflowing_tokens이 True면 차원이 하나 더 붙어서 나온다. 따라서 extend로 바꿔야함
        i_attention_mask.append(input_token['attention_mask'])
        i_token_type_ids.append(input_token['token_type_ids'])
        #i_overflow_mapping.extend(input_token['overflow_to_sample_mapping'])
    
    for data in tqdm(target_data.to_list(), desc=f"target data toknizing "):
        target_token = tokenizer(
                            data, 
                            max_length= max_seq_length,
                            padding="max_length",
                            #return_tensors='pt',
                            truncation=True,
                            #stride = doc_stride,
                            #return_overflowing_tokens=True,
                            #return_token_type_ids=False,
                            )
        
        t_input_ids.append(target_token['input_ids'])
        t_attention_mask.append(target_token['attention_mask'])
        t_token_type_ids.append(target_token['token_type_ids'])
    
    dataset = TensorDataset(torch.tensor(i_input_ids), torch.tensor(i_attention_mask), torch.tensor(i_token_type_ids),
                            torch.tensor(t_input_ids), torch.tensor(t_attention_mask), torch.tensor(t_token_type_ids),)
                            #torch.tensor(i_overflow_mapping))

    return dataset