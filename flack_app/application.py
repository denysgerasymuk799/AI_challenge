# from docx import Document
import json
import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# from routes import app
from flack_app.my_config import Config


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.from_object(Config)
db = SQLAlchemy(app)

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


@app.route("/")
def render_main_page():
    return redirect(url_for('input_profession'))


@app.route('/input_profession', methods=['POST', 'GET'])
def input_profession():
    if request.method == 'POST':
        job = request.values.get("job").lower()
        eng_job_titles = ["system administrator", "analyst", "business analyst",
                          "data scientist", "database administrator", "programmer"]
        ru_job_titles = ["системный администратор", "analyst", "business analyst", "data scientist",
                         "адміністратор баз даних", "программист php"]
        if job in eng_job_titles:
            job = ru_job_titles[eng_job_titles.index(job)]

        global skills

        with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
                user_data_json_from_file:
            user_data_json = {}
            user_data_json['profession'] = job
            json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)

        skills = skills_for_job(job)  # your function
        return redirect(url_for("middle"))
    else:
        return render_template("request.html")


def skills_for_job(job):
    """
    Test function
    :param job:
    :return:
    """
    # temp_dir = os.getcwd()
    # os.chdir('')
    # retrieve skills from database
    # filename = os.path.join(os.getcwd(), 'sea_db', 'courses_and_skills_db.ini')
    # list_from_db = get_parts(["job_title", "skills_list"], "skills_for_all_professions", filename=filename)
    if job.endswith("2"):
        job = job[:-1]
    list_from_db = Profession.query.filter_by(name=job).first().skills

    # os.chdir(temp_dir)

    title_profession = '+'.join(job.split())
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
    test function
    :param skills:
    :return:
    """
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        all_user_data = json.load(user_data_json_from_file)

    title_profession = '+'.join(all_user_data['profession'].split())
    courses_list_input_profession = {}
    # with open(os.path.join(os.getcwd(), 'user_data', title_profession + '.json'), 'r', encoding='utf-8') as \
    #         json_file:
    # course_list = json.load(json_file)
    skills_list = all_user_data["all_job_skills"]
    courses_dict = {}
    course_id = 0
    for skill in skills_list:
        if skill not in current_skills:
            courses = Skill.query.filter_by(name=skill).first().courses
            skill = skill.lower()
            courses_dict[skill] = []
            course_dict = {}
            for course in courses:
                course_id += 1
                course_dict["id"] = course_id
                course_dict["course_title"] = course.course_title
                course_dict["price"] = course.price
                course_dict["image"] = course.image
                course_dict["course_duration"] = course.course_duration
                course_dict["number_of_students"] = course.number_of_students
                course_dict["short_description"] = course.short_description
                course_dict["long_description"] = course.long_description
                course_dict["url"] = course.url

            courses_dict[skill].append(course_dict)

    #
    # id = 0
    # for i, skill in enumerate(courses_list_input_profession.keys()):
    #     for j, course in enumerate(courses_list_input_profession[skill]):
    #         courses_list_input_profession[skill][j]["name"] = course['course_title']
    #         courses_list_input_profession[skill][j]["id"] = "course-" + str(id)
    #         print('courses_list_input_profession[skill]', courses_list_input_profession[skill])
    #         id += 1
    print("courses_dict", courses_dict)
    return courses_dict


global skills
global courses


@app.route("/a")
def a():
    return render_template("skills.html")


@app.route('/courses', methods=['POST', 'GET'])
def index():
    return render_template("one_section.html", courses_list=courses)


@app.route('/selected', methods=['POST', 'GET'])
def selected():
    my_courses = []
    # data = request.form.getlist('checkbox')
    data = request.form
    print(data)
    session['my_courses'] = list(data.keys())
    for skill in courses.keys():
        for course in courses[skill]:
            if course['id'] in data:
                my_courses.append(course)
    print(my_courses)
    return render_template("selected.html", my_courses=my_courses)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
