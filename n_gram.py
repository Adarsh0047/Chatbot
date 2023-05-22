import pandas as pd
import numpy as np
from collections import defaultdict
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
df = pd.read_csv("final_df.csv")
# def find_ngram_frequency(text, n):
#     ngram_counts = defaultdict(int)
#     text = re.sub(r'[^\w\s]','',text.lower())
#     words = text.split()
#     for i in range(len(words)-n+1):
#         ngram = ' '.join(words[i:i+n])
#         ngram_counts[ngram] += 1
#     return ngram_counts


def clean_text(skills):
    i = 0
    for skill in skills:
        # print(skill)
        for ele in punctuation:
            skill = skill.replace(ele, " ")
        # print(skill)
        # what are the ai jobs in coimbatore?
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


# def find_ngram(text, gram):
#     dirty_skills = text.strip('][').split(', ')
#     skills = []
#     for skill in dirty_skills:
#         skills.append(skill)
#     clean_skills = clean_text(skills)
#     clean_skills = " ".join(clean_skills)
#     clean_skills = re.sub(r'[^\w\s]','',clean_skills.lower())
#     words = nltk.word_tokenize(clean_skills)
#     return list(nltk.ngrams(words, gram))

stopwords = stopwords.words('english')
stopwords.extend(["knowledge", "good", "experience", "understanding", "developing", "strong"])

def find_ngram(col):
    n_grams = {}
    for index, row in df.iterrows():
        dirty_skills = row[col].strip('][').split(', ')
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
            if w.lower() not in stopwords:
                wordsFiltered.append(w.lower())
        uni_grams = list(nltk.ngrams(wordsFiltered, 1))
        for gram in uni_grams:
            gram1 = " ".join(gram)
            if gram1 not in n_grams:
                n_grams[gram1] = [{row["COMPANY_NAME"]:row["LOCATION"]}]
            else:
                n_grams[gram1].append([{row["COMPANY_NAME"]:row["LOCATION"]}])
        bi_grams = list(nltk.ngrams(wordsFiltered, 2))
        for gram in bi_grams:
            gram1 = " ".join(gram)
            if gram1 not in n_grams:
                n_grams[gram1] = [{row["COMPANY_NAME"]:row["LOCATION"]}]
            else:
                n_grams[gram1].append([{row["COMPANY_NAME"]:row["LOCATION"]}])
        tri_grams = list(nltk.ngrams(wordsFiltered, 3))
        for gram in tri_grams:
            gram1 = " ".join(gram)
            if gram1 not in n_grams:
                n_grams[gram1] = [{row["COMPANY_NAME"]:row["LOCATION"]}]
            else:
                n_grams[gram1].append([{row["COMPANY_NAME"]:row["LOCATION"]}])
    return n_grams

skill_dict = find_ngram("SKILLS")
user_input = "Computer Vision"
title_dict = find_ngram("TITLE")
def match_location(input, location, dictionary):
    for companies in dictionary[input.lower()]:
        # print(companies)
        for k,v in companies.items():
            if location.lower() in v.lower():
                return k
