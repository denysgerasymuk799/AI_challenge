import json

def get_file_data():
    corpus = []
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
    return corpus

def microsoft_api(body):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'e0ad072721ac448e8ecfe797c3b220a7',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'showStats': 'False',
    })

    try:
        conn = http.client.HTTPSConnection('sea-ucu.cognitiveservices.azure.com')
        body = str(body).encode('utf-8')
        conn.request("POST", "/text/analytics/v3.0-preview.1/keyPhrases?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()

        data = eval(data.decode('utf-8'))

        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def format_json_on_send(corpus):
    data = {}
    id_num = 1

    data["documents"] = []

    for elem in corpus:
        data["documents"].append({"id": str(id_num), "text": elem})
        id_num += 1

    return data

def sort_dict(dict_of_words):
    list_of_values = list(dict_of_words.values())

    list_of_values = sorted(list_of_values)
    list_of_values.reverse()

    list_of_rez = []
    for count in list_of_values:
        for value in dict_of_words:
            if dict_of_words[value] == count:
                list_of_rez.append(value)
                del(dict_of_words[value])
                break

    return list_of_rez


if __name__ == '__main__':
    corpus = get_file_data()
    data = format_json_on_send(corpus)
    id = 1

    temp_data = {"documents": []}
    ready_skills = []

    for elem_data in data["documents"]:
        temp_data["documents"].append(elem_data)

        if id == 10:
            id = 0
            ready_skills.append(microsoft_api(temp_data))

            temp_data = {"documents": []}

        id += 1

    ready_skills.append(microsoft_api(temp_data))

    skills_dict = {}

    for elem in ready_skills:
        try:
            for document in elem["documents"]:
                for skill in document["keyPhrases"]:
                    try:
                        skills_dict[skill] += 1
                    except KeyError:
                        skills_dict[skill] = 1
        except KeyError:
            pass

    list_of_skills_sorted = sort_dict(skills_dict)

    filee = open('skills_data.txt', 'w')

    for elem in list_of_skills_sorted:
        filee.write(elem + "\n")

    filee.close()