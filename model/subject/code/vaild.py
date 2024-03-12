import torch
import pandas as pd
from transformers import AutoTokenizer, BartForConditionalGeneration
import os
from tqdm import tqdm

dataset_path = "../dataset"
dataset_name = "paper_valid_dataset.json"

model = torch.load('../trained_model/model.pt')
tokenizer = AutoTokenizer.from_pretrained('../save_tokenizer')


valid_data_path = os.path.join(dataset_path, dataset_name)

def check_numeric(txt):
    try:
        num = int(txt)
        return True
    except ValueError:
        return False

if valid_data_path.endswith('.json'):
    df = pd.read_json(valid_data_path)['documents']
    total = {'title' : [], 'context' : [], 'summary' : []}
    for d in tqdm(df, desc=f"make_df "):
        total['title'].append(d['title'])

        total['summary'].append(d['abstractive'])

        total_s=''
        for texts in d['text']:
            for text in texts:
                total_s+=text['sentence']
        total['context'].append(total_s)

    valid_df = pd.DataFrame(total)

elif valid_data_path.endswith('.csv'):
    valid_df = pd.read_csv(valid_data_path)

while(True):
    idx = input(f"주제를 찾고싶은 문장의 INDEX입력(0~{len(valid_df)-1}, 종료 : exit) :")
    if not check_numeric(idx):
        if idx == 'exit':
            break
        else:
            continue
    
    else:
        if idx>=len(valid_df):
            print("인덱스가 벗어났습니다")
            continue
        else:
            curr_data = valid_df.iloc[idx]  #title, summary, context들이 있음

    context_intput_ids = tokenizer.encode(curr_data['context'], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)
    summary_intput_ids = tokenizer.encode(curr_data['summary'], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

    summary_text_ids = model.generate(
                        input_ids=summary_intput_ids,
                        bos_token_id=model.config.bos_token_id,
                        eos_token_id=model.config.eos_token_id,
                        length_penalty=1.0,
                        max_length=50,
                        min_length=3,
                        num_beams=6,
                        repetition_penalty=2.0,
                        )

    context_text_ids = model.generate(
                        input_ids=context_intput_ids,
                        bos_token_id=model.config.bos_token_id,
                        eos_token_id=model.config.eos_token_id,
                        length_penalty=1.0,
                        max_length=50,
                        min_length=3,
                        num_beams=6,
                        repetition_penalty=2.0,
                        )
    
    print("idx : ", idx)
    print(f"본문 : {curr_data['context']}")
    print(f"본문 주제 : {tokenizer.decode(context_text_ids[0], skip_special_tokens=True)}")
    print(f"요약문 : {curr_data['summary']}")
    print(f"요약문 주제 : {tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)}")
    print('---'*30)
