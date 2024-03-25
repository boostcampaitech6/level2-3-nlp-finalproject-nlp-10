import re
import hanja
from soynlp.normalizer import *

import pandas as pd


class Denoiser:
    def __init__(self, **kwargs):
        super(Denoiser, self).__init__(**kwargs)
    
    # 문장 양끝 따옴표 제거
    def strip_quotes(self, text):
        if text[0] == '"' and text[-1] == '"':
            text = text.strip('"')
        
        if text[0] == "'" and text[-1] == "'":
            text = text.strip("'")
        return text
        
    # 공백 제거
    def remove_space(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^\s+', '', text)
        text = re.sub(r'\s+$', '', text)
        text = re.sub(r'\t', ' ', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub(r'\r', ' ', text)
        return text
    
    # 따옴표 제거
    def remove_quote(self, text):
        text = re.sub(r'\'', '', text)
        text = re.sub(r'\`', '', text)
        text = re.sub(r'\‘', '', text)
        text = re.sub(r'\’', '', text)

        text = re.sub(r'\"', '', text)
        text = re.sub(r'\“', '', text)
        text = re.sub(r'\”', '', text)
        return text
    
    # () 괄호 안 제거 
    def remove_between_round_brackets(self, text):
        return re.sub(r'\([^)]*\)', '', text)          
    
    # {} 괄호 안 제거 
    def remove_between_curly_brackets(self, text):
        return re.sub(r'\{[^}]*\}', '', text)
        
    # [] 괄호 안 제거 
    def remove_between_square_brackets(self, text):
        return re.sub(r'\[[^]]*\]', '', text)  

    # <> 괄호 안 제거 
    def remove_between_angle_brackets(self, text):
        return re.sub(r'\<[^>]*\>', '', text)

    # url 제거
    def remove_url(self, text):
        text = re.sub(r'http[s]?://(?:[\t\n\r\f\v]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text) 
        text = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', '', text) 
        return text
    
    # 이메일 제거
    def remove_email(self, text):
        return re.sub(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$','', text)        
    
    # 날짜 제거
    def remove_date(self, text):
        return re.sub(r'\d+[.]\d+[.]\d+','', text)

    # 숫자 이용 문자 제거
    def remove_number_text(self, text):
        text = re.sub(r'[0-9]+%', '', text)
        text = re.sub(r'[0-9]+층', '', text)
        return text
    
    # 특수문자 제거    
    def remove_symbol(self, text):
        return re.sub(r'[^\w\s]', '', text)
    
    # 자음, 모음 제거
    def remove_consonants_vowels(self, text):
        text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ]+', '', text)
        return text

    # 클린봇 댓글 제거
    def remove_cleanbot_comment(self, text):
        if ('클린봇' in text) or ('가려진 댓글' in text):
            return ''
        else:
            return text
        
    # 일본어, 한자 제거
    def remove_japanese_chinese(self, text):
        text = re.sub(r'[ぁ-ゔ]+|[ァ-ヴー]+[々〆〤]', '', text)
        text = re.sub(r'[一-龥]+', '', text)
        return text
    
    def remove_sasul_sockbo(self, text):
        patterns = ['\[사설\]', '<사설>', '\(사설\)', '\[속보\]', '<속보>', '\(속보\)']
        replace_pattern = re.compile('|'.join(patterns))
        text = replace_pattern.sub(' ', text)
        return text
    
    def remove_points(self, text):
        text = re.sub(r'[.]{2,}', '.', text) 
        text = re.sub(r'[,]{2,}', ',', text) 
        text = re.sub(r'[.,]{2,}', '.', text) 
        return text
    
    
    # 내용 전처리
    def denoise(self, text):       
        text = str(text)
        if len(text) != 0:
            text = self.remove_space(text)
            text = self.remove_quote(text)
            text = self.remove_between_round_brackets(text)
            text = self.remove_between_curly_brackets(text)
            text = self.remove_between_square_brackets(text)
            text = self.remove_between_angle_brackets(text)
            text = self.remove_url(text)
            text = self.remove_email(text)
            text = self.remove_consonants_vowels(text)
            text = self.remove_cleanbot_comment(text)
            text = self.remove_japanese_chinese(text)

        return text
    
    def denoise_summary(self, text):
        text = self.remove_email(text) #이메일
        text = self.remove_date(text)
        text = self.remove_url(text)
        text = self.remove_sasul_sockbo(text)
        text = self.remove_points(text)
        text = self.remove_space(text)
        text = hanja.translate(text, 'combination-text')
        
        return text
        