import json
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


def get_courses(skills):
    """
    test function
    :param skills:
    :return:
    """
    with open("C:\\Users\\volod\\Downloads\\Telegram Desktop\\coursera_courses_for_profession.json",
              encoding='utf-8') as f:
        course_list = json.load(f)
    return course_list


def skills_for_job(job):
    """
    Test function
    :param job:
    :return:
    """
    return ["kd jbhkudshb", "kdjfhvbuky", "dfihvoiuefgvoiu", "hsudbuygw", "skjdhcbkjh", job]


global skills
global courses


@app.route("/a")
def a():
    return render_template("skills.html")


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        job = request.values.get("job")
        global skills
        skills = skills_for_job(job)  # your function
        return redirect(url_for("middle"))
    else:
        return render_template("request.html")


@app.route('/skills', methods=['POST', 'GET'])
def middle():
    if request.method == 'POST':
        current_skills = request.form.getlist("chosen_skills")
        print(current_skills)
        global courses
        courses = get_courses(current_skills)  # your function
        return redirect(url_for("index"))
    else:
        return render_template("skills.html", skills=skills)


@app.route('/courses', methods=['POST', 'GET'])
def index():
    return render_template("one_section.html", courses_list=courses)


if __name__ == '__main__':
    app.run(debug=True)
