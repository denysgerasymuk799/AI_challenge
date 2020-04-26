from application import db


profession_to_skill = db.Table('profession_to_skill', db.Model.metadata,
    db.Column('profession_id', db.Integer, db.ForeignKey('profession.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
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
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Skill %r>' % self.name

if __name__ == "__main__":
    #p = Profession(name='SMM manager')
    #s1 = Skill(name='Team Work')
    #s2 = Skill(name='Google Analytics')
    #p.skills.append(s1)
    #p.skills.append(s2)
    #db.create_all()
    #db.session.commit()
    #db.session.add(p)
    #db.session.commit()
    p = Profession.query.filter_by(name='SMM manager').first()
    print(p.skills)