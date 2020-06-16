import string
from flask import render_template, request, redirect, \
    url_for, session, jsonify, make_response, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask_app import app, db
from flask_app.forms import LoginForm, RegistrationForm
from flask_app.models import Skill, User
from flask_app.tools import *


@app.route("/", methods=['POST', 'GET'])
def start():
    # return render_template("skills_updated.html")
    return redirect(url_for("render_main_page"))


@app.route("/render_main_page", methods=['POST', 'GET'])
def render_main_page():
    search_skills = request.form.getlist("chosen_skills")
    print(search_skills)

    courses_for_skills_lst = []
    if not search_skills:
        search_skills = ["SQL"]

    # write_user_data writes user_data_json to file
    user_data_json = {'main_page_skills': search_skills}
    write_user_data(user_data_json)

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


@app.route("/save_request", methods=['POST', 'GET'])
def save_request():
    req = request.get_json()
    print(req)

    res = make_response(jsonify(req), 200)
    print(res)

    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as json_file:
        user_data_json = json.load(json_file)
        if req is not None:
            selected_courses = []

            for course in req.values():
                selected_courses.append(course)

            print(selected_courses)
            user_data_json['selected_courses'] = selected_courses

    write_user_data(user_data_json)

    # with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'w', encoding='utf-8') as \
    #         user_data_json_from_file:
    #     json.dump(user_data_json, user_data_json_from_file, indent=4, ensure_ascii=False)

    return redirect(url_for("selected_from_main"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("render_main_page"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(1, form.username.data, user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print(2, form.remember_me.data)
        return redirect(url_for("render_main_page"))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("render_main_page"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, subscription="Free")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/input_profession', methods=['POST', 'GET'])
@login_required
def input_profession():
    dct = get_translation()
    if request.method == 'POST':
        temp_job = request.form.get("select-profession")
        job = dct.get(temp_job, temp_job).lower()

        user_data_json = {'profession': job, "all_job_skills": skills_for_job(job)}
        write_user_data(user_data_json)

        return redirect(url_for("middle"))
    else:
        return render_template("request.html", job_list=list(dct.keys()))


@app.route('/skills', methods=['POST', 'GET'])
@login_required
def middle():
    """
     a function for page, where you choose courses you already have
    :return: get courses from db based on filtered skills for input profession
    """
    user_data_json = get_user_info()
    if request.method == 'POST':
        current_skills = request.form.getlist("chosen_skills")
        print(current_skills)

        user_data_json['current_skills'] = current_skills
        user_data_json["courses"] = get_courses(current_skills)  # your function

        write_user_data(user_data_json)
        return redirect(url_for("index"))
    else:
        return render_template("skills_updated.html", skills=user_data_json["all_job_skills"])


@app.route("/a")
def a():
    return render_template("skills_updated.html")


@app.route('/courses', methods=['POST', 'GET'])
@login_required
def index():
    """

    :return: make a section - for special skill you have a list of courses in html
    """
    courses = get_user_info()["courses"]
    return render_template("one_section.html", courses_list=courses)


@app.route('/selected_from_main', methods=['POST', 'GET'])
@login_required
def selected_from_main():
    """

    :return: a function to page where you can view your selected courses
    """
    print()
    print("hello selected_from_main")
    # req = request.get_json()
    #
    # print(req)
    # req = dict(req)
    #
    # res = make_response(jsonify(req), 200)
    # print(res)
    # selected_courses = req.values()
    # print(selected_courses)

    my_courses = []
    with open(os.path.join(os.getcwd(), 'user_data', 'user_data.json'), 'r', encoding='utf-8') as \
            user_data_json_from_file:
        user_data_json = json.load(user_data_json_from_file)

    skill_names = user_data_json["main_page_skills"]
    course_names = user_data_json["selected_courses"]
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
@login_required
def selected():
    """

    :return: a function to page where you can view your selected courses
    """
    courses = get_user_info()["courses"]
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
@login_required
def price_plans():
    return render_template("view_plans.html")
