import streamlit as st
import pandas as pd
import nltk
from nltk.corpus import words

df = pd.read_csv('morse.csv',header=None)
eng_to_morse = dict(zip(df[df.columns[0]],df[df.columns[1]]))
morse_to_eng = {v: k for k, v in eng_to_morse.items()}

def decrypt(morse_str,char_break='/',word_break='//',capitalize=True):
    morse_words = morse_str.split(word_break)
    eng_words = [''.join([morse_to_eng[char] for char in word.split(char_break)]) for word in morse_words]
    eng = ' '.join(eng_words)
    if capitalize:
        return eng.capitalize()
    else:
        return eng

def encrypt(plain_str,char_break='/',word_break='//'):
    eng_words = plain_str.upper().split(' ')
    morse_words = [char_break.join([eng_to_morse[char] for char in word]) for word in eng_words]
    return word_break.join(morse_words)

def flip(eng_str):
    # reverse forward/backword
    return decrypt(encrypt(eng_str)[::-1])

def swap(eng_str,temp_char="#"):
    #if temp_char in eng_str:
    #    raise Exception('Use different temp_char.')
    return decrypt(encrypt(eng_str).replace('.',temp_char).replace('-','.').replace(temp_char,'-'))

def slip(eng_str,temp_char="#"):
    return flip(swap(eng_str,temp_char=temp_char))

txt = st.text_area(label='Enter text:',value="Hello world")

results = {
    'flip':flip(txt),
    'swap':swap(txt),
    'flip & swap':slip(txt)
}
st.write(results)

corpus = words.words()
#st.write(len(corpus))
#flipped = [flip(i) for i in corpus]
#swapped = [swap(i) for i in corpus]
#slipped = [slip(i) for i in flipped]

if st.button('Generate corpus'):
    col,col_fl,col_sl = [],[],[]
    for i in corpus:
        fl = flip(i).lower()
        if fl in corpus:
            col.append(i)
            col_fl.append(fl)
            sl = swap(fl).lower()
            if sl in corpus:
                col_sl.append(sl)
            else:
                col_sl.append(None)
    d = {'word':col,'flipped':col_fl,'flipped & swapped':col_sl}
    slippy_word_df = pd.DataFrame(data=d)
    slippy_word_df.to_csv('slippy_words.csv',index=None)

slippy_word_df = pd.read_csv('slippy_words.csv')
slippy_word_df