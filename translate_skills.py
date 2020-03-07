from googletrans import Translator

file = open('skills_data.txt')

data = file.read().split('\n')

file.close()

file = open('translated_skills.txt', 'w')

counter = 1

for elem in data:
    try:
        translator = Translator()

        trans_skill = translator.translate(elem).text
        file.write(trans_skill + '\n')
        print("OK!")
        counter += 1

        if counter > 2000:
            break
    except:
        print("Error!!!")
        print(elem)
        print(counter)
        break

file.close()