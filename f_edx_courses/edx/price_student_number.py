from bs4 import BeautifulSoup


def get_price():
    html_file = open("tmp_files/description.html", 'r', encoding="utf-8")
    data = html_file.read()
    html_file.close()
    soup = BeautifulSoup(data, 'html.parser')

    flag = False
    price = ""
    for teg in soup.find_all('span'):
        if "Price:" in teg:
            flag = True
            continue
        if flag:
            price = str(teg)
            break

    price = price.replace("<span>", '')
    price = price.replace("</span>", '')

    return price


def get_student_number():
    html_file = open("tmp_files/description.html", 'r', encoding="utf-8")
    data = html_file.read()
    html_file.close()
    soup = BeautifulSoup(data, 'html.parser')

    number = ""
    spans = soup.find_all('span')
    for i in range(len(spans)):
        if "already enrolled!" in str(spans[i]):
            number = str(spans[i])
            break

    if not number:
        return number

    number = number.replace("<span>", '')
    number = number.split(">")[1]
    number = number.replace("</span", '')
    number.replace(',', '.')
    return number + " students"


if __name__ == '__main__':
    print(get_student_number())



