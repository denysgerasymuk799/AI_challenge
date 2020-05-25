import json
import os

from flask import Blueprint, render_template, request, redirect, url_for, session

from models import Profession

input_profession_page = Blueprint('input_profession', __name__, template_folder='templates')


@input_profession_page.route('/input_profession', methods=['POST', 'GET'])
def input_profession():
    if request.method == 'POST':
        job = request.values.get("job").lower()
        eng_job_titles = ["system administrator", "analyst", "business analyst",
                          "data scientist", "database administrator", "programmer"]
        ru_job_titles = ["системный администратор2", "analyst2", "business analyst2", "data scientist2",
                         "адміністратор баз даних2", "программист php2"]
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
    with open(os.path.join(os.getcwd(), 'user_data', title_profession + '.json'), 'r', encoding='utf-8') as \
            json_file:
        course_list = json.load(json_file)
        for skill in course_list.keys():
            if skill not in current_skills:
                courses_list_input_profession[skill] = course_list[skill]
                print("courses_list_input_profession[skill]", courses_list_input_profession[skill])

    id = 0
    for i, skill in enumerate(courses_list_input_profession.keys()):
        for j, course in enumerate(courses_list_input_profession[skill]):
            print('courses_list_input_profession[skill]', courses_list_input_profession[skill])
            courses_list_input_profession[skill][j]["name"] = course['course_title']
            courses_list_input_profession[skill][j]["id"] = "course-" + str(id)
            id += 1
    return courses_list_input_profession


def skills_for_job(job):
    """
    Test function
    :param job:
    :return:
    """
    temp_dir = os.getcwd()
    os.chdir('')
    # retrieve skills from database
    filename = os.path.join(os.getcwd(), 'sea_db', 'courses_and_skills_db.ini')
    # list_from_db = get_parts(["job_title", "skills_list"], "skills_for_all_professions", filename=filename)
    if job.endswith("2"):
        job = job[:-1]
    list_from_db = Profession.query.filter_by(name=job).first()

    os.chdir(temp_dir)

    title_profession = '+'.join(job.split())
    result_skill_list = []
    for tuple_data in list_from_db:
        title_profession_from_db, list_skills = tuple_data
        if title_profession_from_db == title_profession:
            result_skill_list = list_skills
            break

    return result_skill_list


global skills
global courses


@input_profession_page.route("/a")
def a():
    return render_template("skills.html")


@input_profession_page.route('/skills', methods=['POST', 'GET'])
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


@input_profession_page.route('/courses', methods=['POST', 'GET'])
def index():
    return render_template("one_section.html", courses_list=courses)


@input_profession_page.route('/selected', methods=['POST', 'GET'])
def selected():
    my_courses = []
    data = request.form
    session['my_courses'] = list(data.keys())
    for skill in courses.keys():
        for course in courses[skill]:
            if course['id'] in data:
                my_courses.append(course)
    print(my_courses)
    return render_template("selected.html", my_courses=my_courses)
