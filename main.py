import streamlit as st
import pandas as pd
import nltk

"""
Flipping and swapping are both transformations that happen to a letter after it's encoded in morse and before it's decoded.

Flipping = reversing the sequence of dots and dashes

Swapping = dots turn into dashes and vice versa
"""

## read in csv of morse code and create dictionary
morse_df = pd.read_csv('morse.csv',header=None)
eng_to_morse = dict(zip(morse_df[morse_df.columns[0]],morse_df[morse_df.columns[1]]))
morse_to_eng = {v: k for k, v in eng_to_morse.items()}

## morse/english conversion functions

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

## reverse/swap morse words

def flip(eng_str):
    # reverse forward/backword
    return decrypt(encrypt(eng_str)[::-1])

def swap(eng_str,temp_char="#"):
    #if temp_char in eng_str:
    #    raise Exception('Use different temp_char.')
    return decrypt(encrypt(eng_str).replace('.',temp_char).replace('-','.').replace(temp_char,'-'))

def slip(eng_str,temp_char="#"):
    return flip(swap(eng_str,temp_char=temp_char))

## user input

txt = st.text_area(label='Enter text:',value="Hello world")

results = {
    'flipped':flip(txt),
    'swapped':swap(txt),
    'flipped & swapped':slip(txt)
}
st.write(results)


## generate corpus of words that can be reversed or swapped
st.write('Corpus of words that are still words if you flip and/or swap them:')

nltk.download('words')
from nltk.corpus import words
corpus = [word for word in words.words() if len(word) > 1]

if st.button('Regenerate corpus'):
    col,col_fl,col_sl = [],[],[]
    for i in corpus:
        fl = flip(i.lower())
        sl = swap(fl.lower())
        if sl in corpus:
            col.append(i)
            col_sl.append(sl)
            if fl in corpus:
                if i != fl:
                    col_fl.append(fl)
                else:
                    col_fl.append(None)
            else:
                col_fl.append(None)
        else:
            if fl in corpus:
                if fl not in col:
                    col.append(i)
                    col_sl.append(None)
                    if i != fl:
                        col_fl.append(fl)
                    else:
                        col_fl.append(None)
    d = {'word':col,'flipped':col_fl,'fl & sw':col_sl}
    df = pd.DataFrame(data=d)
    df.to_csv('slippy_words.csv',index=None)

df = pd.read_csv('slippy_words_old.csv')
df['len'] = [len(str(i)) for i in df['word']]
#df = df.drop(df[df['len'] < 2].index)
df = df.drop_duplicates()
df = df.sort_values(by=['len','fl & sw'],ascending=False)
df
