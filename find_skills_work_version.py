from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

corpus = []

tfidf = TfidfVectorizer(stop_words='english')

for i in range(1, 280):
    try:
        file = open("vacancy_text_pages/vacancy_page" + str(i))
        flag = False
        str_to_app = ""
        for line in file:
            if flag:
                line = line.strip()
                str_to_app += line

            if line.startswith("Опис"):
                flag = True
            if line.startswith("Відгукнутися"):
                flag = False

        corpus.append(str_to_app)

    except:
        pass


X = tfidf.fit_transform(corpus)
feature_names = np.array(tfidf.get_feature_names())

responses = tfidf.transform(corpus)


def get_top_tf_idf_words(response, top_n):
    sorted_nzs = np.argsort(response.data)[:-(top_n+1):-1]
    return feature_names[response.indices[sorted_nzs]]

list_of_words = [get_top_tf_idf_words(response,1) for response in responses]

dict_of_words = {}

for elem in list_of_words:
    for word in elem:
        try:
            dict_of_words[word] += 1
        except:
            dict_of_words[word] = 1


def sort_dict(dict_of_words):
    list_of_values = list(dict_of_words.values())

    file = open("result.txt", 'w')

    list_of_values = sorted(list_of_values)
    list_of_values.reverse()

    for count in list_of_values:
        for value in dict_of_words:
            if dict_of_words[value] == count:
                file.write(value + "\t" + str(count) + "\n")
                del dict_of_words[value]
                break

    file.close()


sort_dict(dict_of_words)

str_of_words = " ".join(list(dict_of_words.keys()))
str_of_words = tfidf.transform([str_of_words])
print(get_top_tf_idf_words(str_of_words,10))
