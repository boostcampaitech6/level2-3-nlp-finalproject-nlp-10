from transformers import AutoTokenizer, set_seed
import torch
import pandas as pd
import numpy as np
import os
import random
import time

seed = 1997

random.seed(seed) # python random seed 고정
np.random.seed(seed) # numpy random seed 고정
torch.manual_seed(seed) # torch random seed 고정
torch.cuda.manual_seed_all(seed)
set_seed(seed)

test_dataset_path = '../dataset/custom_data'
test_data = pd.read_csv(os.path.join(test_dataset_path, "FIN_NEWS_SUMMARY.csv"))

length_penalty=1.0
max_length=300
min_length=30
num_beams=6
repetition_penalty=1.5
no_repeat_ngram_size = 15

context = test_data['contents']

model_name = "EbanLee/kobart-summary-v2"

tokenizer = AutoTokenizer.from_pretrained("../save_tokenizer")
# model = BartForConditionalGeneration.from_pretrained(model_name).to("cuda")
model = torch.load('../trained_model_1/model.pt')
model2 =torch.load('../trained_model/model.pt')
# T5_model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-base-korean-summarization')
# T5_tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-base-korean-summarization')

torch.cuda.empty_cache()

with torch.no_grad():
    model.eval()
    model2.eval()
    # T5_model.eval()
  
    model.to("cuda")
    model2.to("cuda")
    # T5_model.to("cuda")

    start_time = time.time()
    for i in range(17300,17370):
        print('\n\n')
        
        #if len(context[i])>1024:continue
        #input_ids = tokenizer.encode(context[i], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)
        inputs = tokenizer(context[i], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

        summary_text_ids = model.generate(
        input_ids=inputs['input_ids'].to("cuda"),
        attention_mask=inputs['attention_mask'].to("cuda"),
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=length_penalty,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        )

        summary_text_ids2 = model2.generate(
        input_ids=inputs['input_ids'].to("cuda"),
        attention_mask=inputs['attention_mask'].to("cuda"),
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        length_penalty=length_penalty,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        )

        print(i, ': ', context[i])
        print(len(tokenizer.tokenize(context[i])))
        print()
        print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
        print(len(summary_text_ids[0]))
        print()
        print(tokenizer.decode(summary_text_ids2[0], skip_special_tokens=True))
        print(len(summary_text_ids2[0]))
        print('')

        # inputs = T5_tokenizer(context[i], return_tensors="pt", padding="max_length", truncation=True, max_length=1026)

        # output = T5_model.generate(
        # input_ids=inputs['input_ids'].to("cuda"),
        # attention_mask=inputs['attention_mask'].to("cuda"),
        # bos_token_id=T5_tokenizer.bos_token_id,
        # eos_token_id=T5_tokenizer.eos_token_id,
        # length_penalty=length_penalty,
        # max_length=max_length,
        # min_length=min_length,
        # num_beams=num_beams,
        # repetition_penalty=repetition_penalty,
        # no_repeat_ngram_size=no_repeat_ngram_size,
        # )

        
        # print(T5_tokenizer.decode(output[0], skip_special_tokens=True))
        # print(len(output[0]))

    elapsed_time1 = time.time() - start_time
    print(f"duration : {elapsed_time1}")
    print('\n\n')
    model.to("cpu")
#-------------------------------------------------------------------------------------------------
    # start_time = time.time()
    # for i in range(1000,1100):
    #     inputs = tokenizer.encode(context[i], return_tensors='pt').to(device='cuda', non_blocking=True)

    #     output = T5_model.generate(inputs, do_sample=True, max_length=max_length)

    #     print(i, ': ', context[i])
    #     print(len(T5_tokenizer.tokenize(context[i])))
    #     print()
    #     # print(tokenizer.decode(summary_text_ids[0], skip_special_tokens=True))
    #     # print(len(summary_text_ids[0]))
    #     # print()
    #     print(T5_tokenizer.decode(output[0], skip_special_tokens=True))
    #     print(len(output[0]))
    #     print('\n\n')

    # elapsed_time2 = time.time() - start_time
    # print(f"duration : {elapsed_time1}")
    # print(f"duration : {elapsed_time2}")
    # print('\n\n')