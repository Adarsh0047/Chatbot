import pandas as pd
import numpy as np
from itertools import chain
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords
df = pd.read_csv("final_df.csv")
def find_ngram_frequency(text, n):
    ngram_counts = defaultdict(int)
    text = re.sub(r'[^\w\s]','',text.lower())
    words = text.split()
    for i in range(len(words)-n+1):
        ngram = ' '.join(words[i:i+n])
        ngram_counts[ngram] += 1
    return ngram_counts


def clean_text(skills):
    i = 0
    for skill in skills:
        if skill.startswith("\'") and skill.endswith("\'"):
            skills[i] = skill[1:-1]
        elif skill.startswith("\'") and not(skill.endswith("\'")):
            skills[i] = skill[1:]
        elif not(skill.startswith("\'")) and skill.endswith("\'"):
            skills[i] = skill[:-1]
        else:
            skills[i] = skill
        i += 1
    return skills


def find_ngram(text, gram):
    dirty_skills = text.strip('][').split(', ')
    skills = []
    for skill in dirty_skills:
        skills.append(skill)
    clean_skills = clean_text(skills)
    clean_skills = " ".join(clean_skills)
    clean_skills = re.sub(r'[^\w\s]','',clean_skills.lower())
    words = nltk.word_tokenize(clean_skills)
    return list(nltk.ngrams(words, gram))

stopwords = stopwords.words('english')
stopwords.extend(["knowledge", "good", "experience", "understanding", "developing", "strong"])

n_grams = {}
for index, row in df.iterrows():
    dirty_skills = row["SKILLS"].strip('][').split(', ')
    # print(dirty_skills)
    skills = []
    for skill in dirty_skills:
        skills.append(skill)
    clean_skills = clean_text(skills)
    # print(clean_skills)
    cleaned_text = " ".join(clean_skills)
    # print(cleaned_text)
    words = nltk.word_tokenize(cleaned_text)
    wordsFiltered = []
    for w in words:
        if w not in stopwords:
            wordsFiltered.append(w)
    uni_grams = list(nltk.ngrams(wordsFiltered, 1))
    for gram in uni_grams:
        gram1 = " ".join(gram)
        if gram1 not in n_grams:
            n_grams[gram1] = [row["COMPANY_NAME"]]
        else:
            n_grams[gram1].append(row["COMPANY_NAME"])
    bi_grams = list(nltk.ngrams(wordsFiltered, 2))
    for gram in bi_grams:
        gram1 = " ".join(gram)
        if gram1 not in n_grams:
            n_grams[gram1] = [row["COMPANY_NAME"]]
        else:
            n_grams[gram1].append(row["COMPANY_NAME"])
    tri_grams = list(nltk.ngrams(wordsFiltered, 3))
    for gram in bi_grams:
        gram1 = " ".join(gram)
        if gram1 not in n_grams:
            n_grams[gram1] = [row["COMPANY_NAME"]]
        else:
            n_grams[gram1].append(row["COMPANY_NAME"])