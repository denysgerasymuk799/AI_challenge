# from docx import Document
import json
import os
import string
from pprint import pprint

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from my_config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)

# our relationship tables
profession_to_skill = db.Table('profession_to_skill', db.Model.metadata,
                               db.Column('profession_id', db.Integer, db.ForeignKey('profession.id')),
                               db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
                               )

skill_to_courses = db.Table('skill_to_courses', db.Model.metadata,
                            db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')),
                            db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
                            )


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    skills = db.relationship("Skill",
                             secondary=profession_to_skill)

    def __repr__(self):
        return '<Profession %r>' % self.name


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    courses = db.relationship("Course",
                              secondary=skill_to_courses)

    def __repr__(self):
        return '<Skill %r>' % self.name


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(300), unique=True, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=True)
    image = db.Column(db.String(500), unique=False, nullable=True)
    course_duration = db.Column(db.String(80), unique=False, nullable=True)
    number_of_students = db.Column(db.String(80), unique=False, nullable=True)
    short_description = db.Column(db.String(5000), unique=False, nullable=True)
    long_description = db.Column(db.String(10000), unique=False, nullable=True)
    url = db.Column(db.String(300), unique=True, nullable=True)

    def __repr__(self):
        return '<Course - {};; {};; {};; {};; {};; {};; {};; {}>'.format(self.course_title, self.price, self.image,
                                                                         self.course_duration, self.number_of_students,
                                                                         self.short_description, self.long_description,
                                                                         self.url)

    def get_dict(self):
        return {"course_title": self.course_title, "price": self.price,
                "image": self.image, "course_duration": self.course_duration,
                "number_of_students": self.number_of_students, "short_description": self.short_description,
                "long_description": self.long_description, "url": self.url}


@app.route("/", methods=['POST', 'GET'])
def render_main_page():
    search_skills = request.form.getlist("chosen_skills")
    selected_courses = request.form.getlist("course_name")
    print(search_skills)
    print(selected_courses)

    courses_for_skills_lst = []
    if not search_skills:
        search_skills = ["SQL"]

    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
            user_data_json_from_file:
        user_data_json = {'main_page_skills': search_skills}
        if selected_courses:
            user_data_json['selected_courses'] = selected_courses
            json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)
            return redirect(url_for("selected_from_main"))
        else:

            json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)

    for skill in search_skills:
        print("skill", skill)
        courses_db = Skill.query.filter_by(name=skill).first().courses
        courses_db = price_filter(courses_db)
        courses_db = duration_filter(courses_db)
        courses_db = certificate_filter(courses_db)
        for course_dict in courses_db:
            print(course_dict.url)

        courses_for_skills_lst.append(courses_db)

    skills = Skill.query.all()
    sorted_skills_by_letter = {}

    for letter in string.ascii_lowercase:
        sorted_skills_by_letter[letter] = []

    for skill in skills:
        sorted_skills_by_letter[str(skill.name).lower()[0]].append(skill)

    return render_template("all_courses_page.html", courses_for_skills_lst=courses_for_skills_lst,
                           sorted_skills_by_letter=sorted_skills_by_letter)
    # return redirect(url_for('input_profession'))


def start_login():
    return redirect(url_for('login'))


def function_for_login(*args):
    return True


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        address = request.form.get("address")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        if function_for_login(address, password, re_password):
            return redirect(url_for('input_profession'))
    return render_template("login.html")


def function_for_register(*args):
    return True


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        address = request.form.get("address")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        if function_for_register(address, password, re_password):
            return redirect(url_for('login'))
    return render_template("register.html")
=======

@app.route('/input_profession', methods=['POST', 'GET'])
def input_profession():
    with open('translation.json') as json_file:
        dct = json.load(json_file)
    if request.method == 'POST':
        temp_job = request.form.get("select-profession")
        job = dct.get(temp_job, temp_job).lower()

        global skills

        with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
                user_data_json_from_file:
            user_data_json = json.load(user_data_json_from_file)

        with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
                user_data_json_from_file:
            user_data_json = {'profession': job}
            json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)

        skills = skills_for_job(job)  # your function
        return redirect(url_for("middle"))
    else:
        return render_template("request.html", job_list=list(dct.keys()))


def skills_for_job(job):
    """
    :param job: str from user input
    :return: a list of skills for this profession from db
    """
    if job.endswith("2"):
        job = job[:-1]
    list_from_db = Profession.query.filter_by(name=job).first().skills

    result_skill_list = []
    print("list_from_db", list_from_db)
    for skill_db in list_from_db:
        skill_db = str(skill_db)
        skill_start = skill_db.find("'")
        skill_end = skill_db.rfind("'")
        skill = skill_db[skill_start + 1: skill_end]
        result_skill_list.append(skill)

    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)
        all_user_data["all_job_skills"] = result_skill_list

    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
            user_data_json_from_file:
        json.dump(all_user_data, user_data_json_from_file, indent=4)

    return result_skill_list


@app.route('/skills', methods=['POST', 'GET'])
def middle():
    """
     a function for page, where you choose courses you already have
    :return: get courses from db based on filtered skills for input profession
    """
    if request.method == 'POST':
        current_skills = request.form.getlist("chosen_skills")
        print(current_skills)

        global courses
        with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
                user_data_json_from_file:
            user_data_json = json.load(user_data_json_from_file)
            user_data_json['current_skills'] = current_skills

        with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
                user_data_json_from_file:
            json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)

        courses = get_courses(current_skills)  # your function

        return redirect(url_for("index"))
    else:
        return render_template("skills.html", skills=skills)


def get_courses(current_skills):
    """
    :param skills: a list of user skills which he input
    :return: a dict of courses for the special skill
    """
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)

    skills_list = all_user_data["all_job_skills"]
    courses_dict = {}
    course_id = 0
    for skill in skills_list:
        if skill not in current_skills:
            courses_db = Skill.query.filter_by(name=skill).first().courses
            skill = skill.lower()
            courses_dict[skill] = []
            course_dict = {}
            for course in courses_db:
                course_id += 1
                course_dict["id"] = str(course_id)
                course_dict["course_title"] = course.course_title
                course_dict["price"] = course.price
                course_dict["image"] = course.image
                course_dict["course_duration"] = course.course_duration
                course_dict["number_of_students"] = course.number_of_students
                course_dict["short_description"] = course.short_description
                course_dict["long_description"] = course.long_description
                course_dict["url"] = course.url

            courses_dict[skill].append(course_dict)

    print("courses_dict", courses_dict)

    # use this filter for every courses for skill
    courses_dict = students_filter(courses_dict)

    return courses_dict


global skills
global courses


@app.route("/a")
def a():
    return render_template("skills.html")


@app.route('/courses', methods=['POST', 'GET'])
def index():
    """

    :return: make a section - for special skill you have a list of courses in html
    """
    return render_template("one_section.html", courses_list=courses)


@app.route('/selected_from_main', methods=['POST', 'GET'])
def selected_from_main():
    """

    :return: a function to page where you can view your selected courses
    """
    selected_courses = request.form.getlist("course_name")

    print(selected_courses)
    my_courses = []
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        user_data_json = json.load(user_data_json_from_file)

    skill_names = user_data_json["main_page_skills"]
    # course_names = user_data_json["selected_courses"]
    print(skill_names)
    # print(course_names)
    for skill in skill_names:
        print("skill", skill)
        courses_db = Skill.query.filter_by(name=skill).first().courses
        for course in courses_db:
            if course.course_title in course_names:
                my_courses.append(course)
    print(my_courses)
    return render_template("selected_from_main.html", my_courses=my_courses)


@app.route('/selected', methods=['POST', 'GET'])
def selected():
    """

    :return: a function to page where you can view your selected courses
    """
    my_courses = []
    data = request.form
    session['my_courses'] = list(data.keys())
    for skill in courses.keys():
        for course in courses[skill]:
            if course['id'] in session['my_courses']:
                my_courses.append(course)
    print(my_courses)
    return render_template("selected.html", my_courses=my_courses)


@app.route('/price_plans', methods=['POST', 'GET'])
def price_plans():
    return render_template("view_plans.html")


def students_filter(courses_dict):
    """

    :param courses_dict:
    :return: filtered by number of students dict of courses
    """
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)

    skills_list = all_user_data["all_job_skills"]
    print(courses_dict)
    for skill in skills_list:
        try:
            skill = skill.lower()
            courses_dict[skill] = filter_param(courses_dict[skill])
        except KeyError:
            continue

    return courses_dict


def filter_param(courses_lst):
    """
    filter a list of courses by a number of students
    :param courses_lst:
    :return:
    """
    rest_courses = []
    position = 0
    while position != len(courses_lst):
        if not "," in courses_lst[position]['number_of_students']:
            rest_courses.append(courses_lst.pop(position))

        else:
            position += 1

    courses_lst = sorted(courses_lst,
                         key=lambda courses_lst: int("".join(courses_lst["number_of_students"].split()[0].split(","))),
                         reverse=True)
    courses_lst += rest_courses

    # for checking results
    for course in courses_lst:
        print(course["course_title"])
        print(course["number_of_students"])
        print()

    return courses_lst


def price_filter(courses_db):
    """

    :return: a list of special courses with parameter
    """
    for position in range(len(courses_db)):
        if courses_db[position].price.lower() == "free":
            courses_db[position].price = "mix free"

        else:
            courses_db[position].price = "mix payed"

    return courses_db


def duration_filter(courses_lst):
    """

    :param courses_lst:
    :return: a result filtered list
    """
    duration_dict = {
        "0-10_hours": (0, 10),
        "10-20_hours": (11, 20),
        "20-30_hours": (21, 30),
        "30+_hours": (31, 40)
    }
    for position in range(len(courses_lst)):
        course_duration = courses_lst[position].course_duration.lower()
        if "minutes" in course_duration:
            course_duration = int(course_duration.split()[0]) / 60
        elif "approx." in course_duration:
            course_duration = int(course_duration.split()[1])
        elif "week" in course_duration:
            course_duration = 35
        elif course_duration.strip() == "yes":
            course_duration = 7
        elif "-" in course_duration and "hours" in course_duration:
            course_duration = int(course_duration.split("-")[0])
        elif "hour" in course_duration:
            course_duration = int(course_duration.split()[0])

        else:
            dict_durations = {"https://www.tutorialspoint.com/": 12,
                              "https://udemy.com/course/": 32,
                              "https://techdevguide.withgoogle.com/": 7}

            for site in dict_durations.keys():
                if site in course_duration:
                    course_duration = dict_durations[site]
                    break

        if course_duration == "":
            course_duration = 32

        for course_time in duration_dict.keys():
            min_duration, max_duration = duration_dict[course_time]
            if min_duration <= course_duration <= max_duration:
                courses_lst[position].price += " " + course_time
                break

        # courses_db[position].price = " " + courses_db[position].skill

    return courses_lst


def certificate_filter(courses_lst):
    """

    :param courses_lst:
    :return: a result list with courses in which url is one item from with_certificates list
    """
    with_certificates = ["https://alison.com/", "https://www.edx.org/", "https://www.codecademy.com/",
                         "https://udemy.com/", "https://www.coursera.org/"]

    for position in range(len(courses_lst)):
        flag_with_cerf = 0

        for site in with_certificates:
            if courses_lst[position].url.startswith(site):
                courses_lst[position].price += " with_cerf"
                flag_with_cerf = 1
                break

        if flag_with_cerf == 0:
            courses_lst[position].price += " without_cerf"

    return courses_lst


if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()
