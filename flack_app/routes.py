from flask import render_template, redirect, url_for, request, session
from flack_app.application import app
from flack_app.tools import get_courses, skills_for_job, get_user_info, write_user_data


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

        user_data_json = {'profession': job}
        write_user_data(user_data_json)

        skills = skills_for_job(job)  # your function
        all_user_data = get_user_info()
        all_user_data["skills_for_job"] = skills
        write_user_data(all_user_data)

        return redirect(url_for("middle"))
    else:
        return render_template("request.html")


@app.route('/skills', methods=['POST', 'GET'])
def middle():
    """
     a function for page, where you choose courses you already have
    :return: get courses from db based on filtered skills for input profession
    """
    if request.method == 'POST':
        current_skills = request.form.getlist("chosen_skills")
        print(current_skills)

        user_data_json = get_user_info()
        user_data_json['current_skills'] = current_skills
        write_user_data(user_data_json)

        courses = get_courses(current_skills)  # your function
        all_user_info = get_user_info()
        all_user_info["courses"] = courses
        write_user_data(all_user_info)


        return redirect(url_for("index"))
    else:
        skills = get_user_info()["skills_for_job"]
        return render_template("skills.html", skills=skills)


@app.route("/a")
def a():
    return render_template("skills.html")


@app.route('/courses', methods=['POST', 'GET'])
def index():
    """

    :return: make a section - for special skill you have a list of courses in html
    """
    courses = get_user_info()["courses"]
    return render_template("one_section.html", courses_list=courses)


@app.route('/selected', methods=['POST', 'GET'])
def selected():
    """

    :return: a function to page where you can view your selected courses
    """
    my_courses = []
    data = request.form
    session['my_courses'] = list(data.keys())

    courses = get_user_info()["courses"]
    for skill in courses.keys():
        for course in courses[skill]:
            if course['id'] in session['my_courses']:
                my_courses.append(course)
    print(my_courses)
    return render_template("selected.html", my_courses=my_courses)

