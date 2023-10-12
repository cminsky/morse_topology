import streamlit as st
import pandas as pd

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

test = encrypt("Hello World!")
test

test = decrypt("...././.-../.-../---//.--/---/.-./.-../-../-.-.--")
test