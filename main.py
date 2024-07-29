import argparse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Student, Group, Teacher, Subject, Grade


def create_student(session: Session, fullname: str, group_id: int):
    student = Student(fullname=fullname, group_id=group_id)
    session.add(student)
    session.commit()


def list_students(session: Session):
    return session.query(Student).all()


def update_student(session: Session, student_id: int, fullname: str):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        student.fullname = fullname
        session.commit()


def remove_student(session: Session, student_id: int):
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        session.delete(student)
        session.commit()


def main():
    parser = argparse.ArgumentParser(description="CRUD operations for database models.")
    parser.add_argument('--action', '-a', required=True, choices=['create', 'list', 'update', 'remove'])
    parser.add_argument('--model', '-m', required=True, choices=['Student', 'Group', 'Teacher', 'Subject', 'Grade'])
    parser.add_argument('--name', '-n')
    parser.add_argument('--group_id', type=int)
    parser.add_argument('--id', type=int)
    parser.add_argument('--student_id', type=int)
    parser.add_argument('--subject_id', type=int)
    parser.add_argument('--teacher_id', type=int)

    args = parser.parse_args()
    session = SessionLocal()

    if args.model == 'Student':
        if args.action == 'create':
            create_student(session, args.name, args.group_id)
        elif args.action == 'list':
            students = list_students(session)
            for student in students:
                print(f"ID: {student.id}, Name: {student.fullname}")
        elif args.action == 'update':
            update_student(session, args.id, args.name)
        elif args.action == 'remove':
            remove_student(session, args.id)

    # Реалізуйте інші моделі аналогічно

    session.close()


if __name__ == "__main__":
    main()
