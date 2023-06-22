import pandas as pd
import string
from itertools import chain
df = pd.read_csv("final_df.csv")
unique_skills = []
for index, row in df.iterrows():
    skills = row["SKILLS"].strip('][').split(', ')
    for skill in skills:
        unique_skills.append(skills)
unique_skills = list(chain.from_iterable(unique_skills))
i = 0
for skill in unique_skills:
    if skill.startswith("\'") and skill.endswith("\'"):
        unique_skills[i] = skill[1:-1]
    elif skill.startswith("\'") and not(skill.endswith("\'")):
        unique_skills[i] = skill[1:]
    elif not(skill.startswith("\'")) and skill.endswith("\'"):
        unique_skills[i] = skill[:-1]
    else:
        unique_skills[i] = skill
    i += 1
unique_skills = list(set(unique_skills))
for skill in unique_skills:
    if skill.startswith("\'") and skill.endswith("\'"):
        print(skill)
unique_skills = [skill.lower() for skill in unique_skills]
def remove_punct(word):
    for punctuation in [".", ","]:
        word = word.replace(punctuation, '')
    return word
unique_skills = [remove_punct(skill) for skill in unique_skills]
with open('unq_words.txt','w') as file:
	file.write('\n'.join(unique_skills))