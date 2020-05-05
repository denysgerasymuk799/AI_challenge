import json
import os
import sqlite3
from . import db
from flask_debugtoolbar.panels import sqlalchemy

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
    name = db.Column(db.String(80), unique=True, nullable=False)
    skills = db.relationship("Skill",
                             secondary=profession_to_skill)

    def __repr__(self):
        return '<Profession %r>' % self.name


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    courses = db.relationship("Course",
                              secondary=skill_to_courses)

    def __repr__(self):
        return '<Skill %r>' % self.name


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=True)
    image = db.Column(db.String(100), unique=False, nullable=True)
    course_duration = db.Column(db.String(80), unique=False, nullable=True)
    number_of_students = db.Column(db.String(80), unique=False, nullable=True)
    short_description = db.Column(db.String(200), unique=False, nullable=True)
    long_description = db.Column(db.String(1200), unique=False, nullable=True)
    url = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return '<Course %r, %r, %r, %r, %r, %r, %r, %r>' % self.course_title, self.price,\
               self.image, self.course_duration, self.number_of_students, self.short_description, \
               self.long_description, self.url


if __name__ == "__main__":
    pass
    # p = Profession(name='SMM manager')
    # s1 = Skill(name='Team Work')
    # s2 = Skill(name='Google Analytics')
    # p.skills.append(s1)
    # p.skills.append(s2)
    # db.create_all()
    # db.session.commit()
    # # db.session.add(p)
    # # db.session.commit()
    # p = Profession.query.filter_by(name='SMM manager').first()
    # print(p)
    # print(p.skills)
