import re
import hanja

def remove_space(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+', '', text)
    text = re.sub(r'\s+$', '', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\r', ' ', text)
    return text

# 따옴표 변환
def remove_quote(text):
    text = re.sub(r'\'+', '\'', text)
    text = re.sub(r'\`+', '\'', text)
    text = re.sub(r'\‘+', '\'', text)
    text = re.sub(r'\’+', '\'', text)

    text = re.sub(r'\"+', '\"', text)
    text = re.sub(r'\“+', '\"', text)
    text = re.sub(r'\”+', '\"', text)
    return text

# () 괄호 안 제거
def remove_between_round_brackets(text):
    return re.sub(r'\([^)]*\)', ' ', text)

# {} 괄호 안 제거
def remove_between_curly_brackets(text):
    return re.sub(r'\{[^}]*\}', ' ', text)

# [] 괄호 안 제거
def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', ' ', text)

# <> 괄호 안 제거
def remove_between_angle_brackets(text):
    return re.sub(r'\<[^>]*\>', ' ', text)

# url 제거
def remove_url(text):
    text = re.sub(r'http[s]?://(?:[\t\n\r\f\v]|[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    text = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', ' ', text)
    return text

# 이메일 제거
def remove_email(text):
    return re.sub(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',' ', text)

# 날짜 제거
def remove_date(text):
    return re.sub(r'\d+[.]\d+[.]\d+',' ', text)

# 숫자 이용 문자 제거
def remove_number_text(text):
    text = re.sub(r'[0-9]+%', ' ', text)
    text = re.sub(r'[0-9]+층', ' ', text)
    return text

# 특수문자 제거
def remove_symbol(text):
    return re.sub(r'[^\w\s.,]', ' ', text)

# 자음, 모음 제거
def remove_consonants_vowels(text):
    text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ]+', ' ', text)
    return text

# 앞에 날리기
def remove_to_callback(news):
    callback_list = []
    try :
        for b in re.finditer('flash_removeCallback()',news):
            callback_list.append(b.end())
        news = news[callback_list[0]:]
    except :
        news = news
    return news

# 뒤에 날리기
def remove_from_back_third_triangle(news):
    triangle_list = []
    for a in re.finditer('▶',news):
        triangle_list.append(a.start())
    if len(triangle_list) >= 3:
        news = news[:triangle_list[-3]]
    elif len(triangle_list) == 2:
        news = news[:triangle_list[-2]]
    elif len(triangle_list) == 1:
        news = news[:triangle_list[-1]]
    return news

def remove_float(news):
    return re.sub(r'[0-9]+.[0-9]*',' ', news)

def remove_journalist(news):
    return re.sub(r'[가-핳]{2,4}\s+기자[^가-핳]+',' ', news)

def remove_points(text):
    text = re.sub(r'[.]{2,}', '.', text) 
    text = re.sub(r'[,]{2,}', ',', text) 
    text = re.sub(r'[.,]{2,}', '.', text) 
    return text

def pre_processing(txt):
    # txt = remove_to_callback(txt)
    # txt = remove_from_back_third_triangle(txt)
    txt = remove_email(txt) #이메일
    txt = remove_date(txt)
    # txt = remove_quote(txt) #따옴표
    txt = remove_url(txt)   #URL
    # txt = remove_number_text(txt)
    # txt = remove_consonants_vowels(txt) #단일 자음 모음
    # txt = remove_between_round_brackets(txt)
    # txt = remove_between_curly_brackets(txt)    #{}안에 제거
    # txt = remove_between_square_brackets(txt)   #[]안에 제거
    # txt = remove_between_angle_brackets(txt)
    # txt = remove_journalist(txt)    
    # txt = remove_float(txt)
    # txt = remove_symbol(txt)
    txt = txt.replace('[사설]', ' ')
    txt = txt.replace('<사설>', ' ')
    txt = txt.replace('(사설)', ' ')
    txt = txt.replace('[속보]', ' ')
    txt = txt.replace('<속보>', ' ')
    txt = txt.replace('(속보)', ' ')
    txt = remove_points(txt)
    txt = remove_space(txt)
    txt = hanja.translate(txt, 'combination-text')

    return txt