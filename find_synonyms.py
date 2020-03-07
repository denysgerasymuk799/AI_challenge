import json
from nltk.corpus import wordnet
def synonyms(word):
    synonyms = []
    word = word.replace(","," ") if "," in word else word
    lst = word.split()
    synonyms.extend(lst)
    for i in range(len(lst)):
        for syn in wordnet.synsets(lst[i]):
            for l in syn.lemmas():
                synonyms.append(l.name())
        synonyms = list(synonyms)

        for i in range(len(synonyms)):
            synonyms.append(synonyms[i] + "s")
    synonyms = set(synonyms)
    return list(synonyms)[0:5]

def get_data():
    file = open('translated_skills.txt')
    data = file.read().split('\n')
    file.close()

    return data


if __name__ == '__main__':
    data = get_data()
    counter = 1

    file = open("synonyms.txt", 'w')
    file.write("{")

    for elem in data:
        if len(elem) < 100:
            file.write(elem + ": " + str(synonyms(elem)) + ",\n")
            print(elem)

    file.write("}")
    file.close()