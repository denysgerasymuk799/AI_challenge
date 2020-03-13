import json
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
with open("C:\\Users\\volod\\Downloads\\Telegram Desktop\\coursera_courses_for_profession.json", encoding='utf-8') as f:# файл з курсами
    skills = json.load(f)


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        job = request.values.get("job")
        #return redirect(url_for("user", usr=job))
        return redirect(url_for("index"))
    else:
        return render_template("request.html")
        #return render_template("skills.html", skills=["asccd", "dfvbrsbt", "drsgverg", "wfqwergw"])


@app.route('/courses', methods=['POST', 'GET'])
def index():
    return render_template("one_section.html", skills=skills)


if __name__ == '__main__':
    app.run(debug=True)
