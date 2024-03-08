import os
from tqdm import tqdm
import pandas as pd

def make_summary_data(model, tokenizer, dataset_path, device):
    file_list = os.listdir(dataset_path)
    name_end = 'RY.csv'
    model.to(device)

    for file in file_list:
        if not file.endswith(name_end):
            continue
            
        file_path = os.path.join(dataset_path, file)
        total_data = pd.read_csv(file_path)
        if 'summary' in total_data.columns:
            total_data = total_data.drop(['summary'], axis=1)   #데이터 받고 요약 있으면 없애주기
        
        #total_data = total_data.iloc[:4000]  #몇개만 떼서 실험
            
        s_list = []

        for data in tqdm(total_data['contents'].to_list(), desc=f'{file} summarizing '):
            input_ids = tokenizer.encode(data, return_tensors="pt", padding="max_length", truncation=True, max_length=1024).to(device)

            summary_text_ids = model.generate(
                                        input_ids=input_ids,
                                        bos_token_id=model.config.bos_token_id,
                                        eos_token_id=model.config.eos_token_id,
                                        length_penalty=2.0,
                                        max_length=256,
                                        min_length=30,
                                        num_beams=6,
                                        repetition_penalty=2.0,
                                        ).to('cpu')

            output = tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
            s_list.append(output)

        df_sum = pd.DataFrame({'summary' : s_list})
        curr_data = pd.concat([curr_data, df_sum], axis=1)

        curr_data.to_csv(os.path.join("../../embedding/dataset", f'Sum_{file}'), index=False)
        print('\nAdd summary data finish!\n')
            