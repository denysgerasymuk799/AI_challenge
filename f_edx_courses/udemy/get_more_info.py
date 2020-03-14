import requests
from bs4 import BeautifulSoup
from pprint import pprint


HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"
        }


def get_more_info(URL, course_name):
    def generate_page(url):
        response = requests.get(url,
                                headers=HEADERS)

        page_text = response.text
        soup = BeautifulSoup(page_text, 'html.parser')
        with open("tmp_files/tmp.html", 'w') as res_file:
            res_file.write(soup.prettify())

    def get_students_number():
        found = False
        with open("tmp_files/tmp.html") as html_file:
            for line in html_file:
                line = "".join(line.split(" "))
                line = "".join(line.split("\n"))
                if "enrollment" in line:
                    found = True
                    continue
                if found:
                    if not line.startswith("<"):
                        line.replace("enrolled", '')
                        for i in range(len(line)):
                            if line[i].isdigit() or line[i] == ',':
                                continue
                            else:
                                line = line[:i] + " " + line[i:]
                                return line
                    else:
                        found = False
            return ""

    def get_descriptions():
        with open("tmp_files/tmp.html", 'r') as tmp_file:
            text = tmp_file.read()

        soup = BeautifulSoup(text, "html.parser")
        TEXT = soup.get_text()
        TEXT = TEXT.split('\n')
        for line in TEXT:
            if "".join(line.split(" ")) == "":
                TEXT.remove(line)

        short_description = ""
        long_description = ""
        for i in range(len(TEXT)):
            if "What you'll learn" in TEXT[i]:
                i += 1
                while ("Requirements" not in TEXT[i]) and ("Description" not in TEXT[i]) \
                        and ("Show more" not in TEXT[i]):
                    short_description += TEXT[i] + '\n'
                    i += 1
            if "Description" in TEXT[i]:
                i += 1
                while "Show more" not in TEXT[i] and "Featured review" not in TEXT[i] \
                        and "Curriculum" not in TEXT[i]:
                    long_description += TEXT[i] + '\n'
                    i += 1
            i += 1

        return short_description, long_description

    generate_page(URL)

    print(f"    Currently parsing: {course_name}")
    descriptions = get_descriptions()
    short_description = descriptions[0]
    long_description = descriptions[1]
    number_of_students = get_students_number()

    # handling situation when I'm banned
    if number_of_students == "" and long_description == "" and short_description == "":
        print("    404: ACCESS DENIED!")
        return {}

    # creating result
    result = {"number_of_students": number_of_students,
              "short_description": short_description,
              "long_description": long_description
              }

    return result


if __name__ == '__main__':
    res = get_more_info("https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/")
    pprint(res)