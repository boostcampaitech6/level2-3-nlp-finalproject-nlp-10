import torch
from torch.utils.data import TensorDataset

def make_dataset(tokenizer, input_data, target_data):
    max_seq_length = 1024
    doc_stride = 128

    input_token = tokenizer(
                        input_data.to_list(), 
                        max_length= max_seq_length,
                        padding="max_length",
                        return_tensors='pt',
                        truncation=True,
                        stride = doc_stride,
                        return_overflowing_tokens=True,
                        #return_token_type_ids=False,
                        )
    

    target_token = tokenizer(
                        target_data.to_list(), 
                        max_length= max_seq_length,
                        padding="max_length",
                        return_tensors='pt',
                        truncation=True,
                        stride = doc_stride,
                        #return_token_type_ids=False,
                        )
    
    
    dataset = TensorDataset(input_token['input_ids'], input_token['attention_mask'], input_token['token_type_ids'],
                            target_token['input_ids'], target_token['attention_mask'], target_token['token_type_ids'],
                            input_token['overflow_to_sample_mapping'])

    return dataset