from flask_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_app import login

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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    subscription = db.Column(db.String(40))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User( username: {self.username}, email: {self.email})"

# additional-------------------------------------------------------------------
# our relationship tables
profession_to_skill2 = db.Table('profession_to_skill2', db.Model.metadata,
                               db.Column('profession_id', db.Integer, db.ForeignKey('profession2.id')),
                               db.Column('skill_id', db.Integer, db.ForeignKey('skill2.id'))
                               )

skill_to_courses2 = db.Table('skill_to_courses2', db.Model.metadata,
                            db.Column('skill_id', db.Integer, db.ForeignKey('skill2.id')),
                            db.Column('course_id', db.Integer, db.ForeignKey('course2.id'))
                            )


class Profession2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    skills = db.relationship("Skill2",
                             secondary=profession_to_skill2)

    def __repr__(self):
        return '<Profession2 %r>' % self.name


class Skill2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    courses = db.relationship("Course2",
                              secondary=skill_to_courses2)

    def __repr__(self):
        return '<Skill2 %r>' % self.name


class Course2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(3000), unique=True, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=True)
    image = db.Column(db.String(500), unique=False, nullable=True)
    course_duration = db.Column(db.String(80), unique=False, nullable=True)
    number_of_students = db.Column(db.String(80), unique=False, nullable=True)
    short_description = db.Column(db.String(50000), unique=False, nullable=True)
    long_description = db.Column(db.String(100000), unique=False, nullable=True)
    url = db.Column(db.String(1000), unique=True, nullable=True)

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


@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


if __name__ == "__main__":
    # db.create_all()
    pass