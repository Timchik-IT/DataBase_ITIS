import random
import sqlalchemy as sql
from faker import Faker

engine = sql.create_engine('postgresql://postgres:12345678@localhost/Lab1')
connection = engine.connect()

metadata = sql.MetaData()
fake = Faker()

groups = sql.Table(
    "groups", metadata,
    sql.Column('groupnumber', sql.Integer, primary_key=True),
    sql.Column('specialty', sql.String),
    sql.Column('department', sql.String),
    sql.Column('numberofstudents', sql.Integer)
)

teachers = sql.Table(
    "teachers", metadata,
    sql.Column('teachercode', sql.Integer, primary_key=True),
    sql.Column('lastname', sql.String),
    sql.Column('firstname', sql.String),
    sql.Column('middlename', sql.String),
    sql.Column('phone', sql.String),
    sql.Column('experience', sql.Integer)
)

workload = sql.Table(
    "workload", metadata,
    sql.Column('teachercode', sql.Integer),
    sql.Column('groupnumber', sql.Integer),
    sql.Column('hours', sql.Integer),
    sql.Column('subject', sql.String),
    sql.Column('lessontype', sql.String),
    sql.Column('payment', sql.Float)
)

for i in range(1, 501):
    group_data = {
        'specialty': fake.text()[:255],
        'department': fake.text()[:255],
        'numberofstudents': random.randint(15, 30)
    }
    
    connection.execute(groups.insert().values(groupnumber=i, **group_data))
    connection.commit()

for i in range(1, 501):
    teachers_data = {
        'lastname': fake.text()[:255],
        'firstname': fake.text()[:255],
        'middlename': fake.text()[:255],
        'phone': fake.text()[:20],
        'experience': random.randint(1, 20)
    }
    connection.execute(teachers.insert().values(teachercode=i, **teachers_data))
    connection.commit()

for i in range(1, 501):
    workload_data = {
        'teachercode': random.randint(1, 50),
        'groupnumber': random.randint(1, 50),
        'hours': random.randint(1, 10),
        'subject': fake.text()[:255],
        'lessontype': fake.text()[:50],
        'payment': random.randint(1, 20)
    }
    connection.execute(workload.insert().values(**workload_data))
    connection.commit()
