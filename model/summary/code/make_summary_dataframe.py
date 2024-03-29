import os
from tqdm import tqdm, trange
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from preprocess import pre_processing

def make_summary_data(model, tokenizer, dataset_path, device):
    file_list = os.listdir(dataset_path)
    name_end = 'RY.csv'
    
    batch_size = 64
    length_penalty=1.0
    max_length=300
    min_length=12
    num_beams=6
    repetition_penalty=1.5
    no_repeat_ngram_size = 15

    model.to(device)
    model.eval()

    for file in file_list:
        if not file.endswith(name_end):
            continue
            
        file_path = os.path.join(dataset_path, file)
        total_data = pd.read_csv(file_path)

        if 'summary' in total_data.columns:
            total_data = total_data.drop(columns=['summary'], axis=1)   #데이터 받고 요약 있으면 없애주기
        
        #input_ids = tokenizer(total_data['contents'].to_list(), return_tensors="pt", padding="max_length", truncation=True, max_length=1024)['input_ids']

        input_ids = []
        input_mask = []
        no_text_ids = []
        for idx in trange(len(total_data), desc=f'tokenizing '):
            text = pre_processing(total_data['contents'].iloc[idx])
            text_len = len(tokenizer.tokenize(text))
            
            if text_len<min_length+50:
                text = total_data['title'].iloc[idx] + '. ' + text

            tokens = tokenizer(text, padding="max_length", truncation=True, max_length=1024)
            input_ids.append(tokens['input_ids'])
            input_mask.append(tokens['attention_mask'])

            if len(tokenizer.tokenize(text))<min_length+50:
                no_text_ids.append(idx)

        print(f'\nShort Text: {len(no_text_ids)}\n')

        input_dataset = TensorDataset(torch.tensor(input_ids),torch.tensor(input_mask))
        data_loader = DataLoader(input_dataset, batch_size=batch_size, shuffle=False)

        s_list = []

        for batch in tqdm(data_loader, desc=f'{file} summarizing '):
            summary_text_ids = model.generate(
                                        input_ids=batch[0].to(device),
                                        attention_mask=batch[1].to(device),
                                        bos_token_id=model.config.bos_token_id,
                                        eos_token_id=model.config.eos_token_id,
                                        length_penalty=length_penalty,
                                        max_length=max_length,
                                        min_length=min_length,
                                        num_beams=num_beams,
                                        repetition_penalty=repetition_penalty,
                                        # no_repeat_ngram_size = no_repeat_ngram_size,  #사용하면 속도가 느려진다.
                                        ).to('cpu')


            for ids in summary_text_ids:
                output = tokenizer.decode(ids, skip_special_tokens=True)
                output = output.replace("\n", " ")
                s_list.append(output)
        
        for idx in no_text_ids:
            s_list[idx] = pre_processing(total_data['title'].iloc[idx])

        df_sum = pd.DataFrame({'summary' : s_list})

        total_data = pd.concat([total_data, df_sum], axis=1)
        total_data.to_csv(os.path.join("../../embedding/dataset", f'Sum_{file}'), index=False)
        print('\nAdd summary data finish!\n')
            