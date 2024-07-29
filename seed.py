from faker import Faker
from sqlalchemy.orm import Session
from models import Student, Group, Teacher, Subject, Grade
from database import SessionLocal
import random
from datetime import datetime

fake = Faker()

def create_groups(session: Session):
    for _ in range(3):
        group = Group(name=fake.word())
        session.add(group)
    session.commit()

def create_teachers(session: Session):
    for _ in range(5):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
    session.commit()

def create_subjects(session: Session):
    teachers = session.query(Teacher).all()
    for _ in range(8):
        subject = Subject(name=fake.word(), teacher_id=random.choice(teachers).id)
        session.add(subject)
    session.commit()

def create_students(session: Session):
    groups = session.query(Group).all()
    for _ in range(50):
        student = Student(fullname=fake.name(), group_id=random.choice(groups).id)
        session.add(student)
    session.commit()

def create_grades(session: Session):
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for _ in range(random.randint(1, 5)):
            grade = Grade(grade=random.randint(1, 10), date=fake.date_this_year(), student_id=student.id, subject_id=random.choice(subjects).id)
            session.add(grade)
    session.commit()

def seed_data():
    session = SessionLocal()
    create_groups(session)
    create_teachers(session)
    create_subjects(session)
    create_students(session)
    create_grades(session)
    session.close()

if __name__ == "__main__":
    seed_data()
