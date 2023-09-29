# -*- coding: utf-8 -*-
"""
Copyright 2023 Wannaphong Phatthiyaphaibun

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pythainlp.util import normalize
from pythainlp import thai_lead_vowels,thai_digits,thai_below_vowels,thai_above_vowels,thai_follow_vowels,thai_characters,thai_tonemarks,thai_consonants
from pythainlp.corpus import thai_words
from pythainlp.tokenize import Tokenizer,Trie
import re
from fixthaipdf.dict import replace_list
from fixthaipdf.more_dict import replace_list_after_clean

replace_list+=[(i.replace("า","ำ"),i) for i in list(thai_words()) if "า" in i]
replace_list+=[(i.replace("ำ","า"),i) for i in list(thai_words()) if "ำ" in i]
replace_list+=[(i.replace("ำ","้ำ"),i) for i in list(thai_words()) if "ำ" in i]

d={i:j for i,j in replace_list}
_list_d=set(d.keys())
not_change=set(["ทำ","กระทำ"])

def replace_w(w):
    if w in _list_d and w not in not_change:
        return d[w]
    return w

word_list = list(thai_words())+[i for i,_ in replace_list]+[i for _,i in replace_list]
trie_word = Trie(word_list)
tokenizer=Tokenizer(trie_word)
thai_characters_without_dig = ''.join([i for i in thai_characters if i not in thai_digits])


replace_list_after_clean_key = set([i for i,_ in replace_list_after_clean])
d2={i:j for i,j in replace_list_after_clean}
word_list_2 = list(thai_words())+[i for i,_ in replace_list_after_clean]
trie_word_2 = Trie(word_list_2)
tokenizer2=Tokenizer(trie_word_2,engine="mm")

def _clean_missing_1(text):
    text = text.replace("\uf70a","่") # ไม้เอก
    text = text.replace("\uf70b","้") # ไม้โท
    text = text.replace("\uf70c","๊") # ไม้ตรี
    text = text.replace("\uf70e","์") # 
    text = text.replace("\uf710","้")
    text = text.replace("\uf712","็")
    text = text.replace("\uf705","๋")
    text = text.replace("\xa0","\n")
    text = text.replace("","ิ")
    text = text.replace("","ี")
    text = text.replace("","ื")
    text = text.replace("","์")
    text = "".join([replace_w(w) for w in tokenizer.word_tokenize(text)])
    text = re.sub(f"([{thai_lead_vowels}])[ \t]","\\1", text)
    text = re.sub(f"[ \t]([{thai_above_vowels}])","\\1", text)
    text = re.sub(f"[ \t]([{thai_follow_vowels}])","\\1", text)
    text = re.sub(f"[ำ]([{thai_above_vowels}])","\\1ำ", text)
    text = re.sub(f"([{thai_above_vowels}])[ \t]([{thai_consonants}])","\\1\\2", text)
    text = re.sub(f"([{thai_characters}])[ \t]([{thai_below_vowels}])","\\1\\2", text)
    text = "".join([replace_w(w) for w in tokenizer.word_tokenize(text)])
    text = re.sub(f"([{thai_tonemarks}])[ \t]+([{thai_consonants}])","\\1\\2", text) # thai_below_vowels
    text = re.sub(f"([{thai_characters}])[ \t]+([{thai_tonemarks}])","\\1\\2", text)
    text = text.replace(" )",")")
    text = text.replace("( ","(")
    text = text.replace(" ”","”")
    text = text.replace("“ ","“")
    text = text.replace(" ์","์")
    return normalize(text)


def _clean_after_1(text):
    _text=[]
    for w in tokenizer2.word_tokenize(text):
        if w in replace_list_after_clean_key:
            _text.append(d2[w])
        else:
            _text.append(w)
    return ''.join(_text)

def clean(text: str)->str:
    text = _clean_missing_1(text)
    text = _clean_after_1(text)
    return text