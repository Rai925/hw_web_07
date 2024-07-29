from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Student, Grade, Subject, Teacher, Group

from sqlalchemy.orm import aliased
def select_1(session: Session):
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id)\
        .order_by(desc('avg_grade')).limit(5).all()

def select_2(session: Session, subject_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).filter(Grade.subject_id == subject_id)\
        .group_by(Student.id).order_by(desc('avg_grade')).first()

def select_3(session: Session, subject_id: int):
    """Знайти середній бал у групах з певного предмета."""
    return session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == subject_id)\
        .group_by(Group.id).all()

def select_4(session: Session):
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    return session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).scalar()

def select_5(session: Session, teacher_id: int):
    """Знайти які курси читає певний викладач."""
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()

def select_6(session: Session, group_id: int):
    """Знайти список студентів у певній групі."""
    return session.query(Student.fullname).filter(Student.group_id == group_id).all()

def select_7(session: Session, group_id: int, subject_id: int):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    return session.query(Student.fullname, Grade.grade)\
        .join(Group).filter(Student.group_id == group_id)\
        .join(Grade).filter(Grade.subject_id == subject_id).all()

def select_8(session: Session, teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()

def select_9(session: Session, student_id: int):
    """Знайти список курсів, які відвідує певний студент."""
    return session.query(Subject.name).join(Grade).filter(Grade.student_id == student_id).distinct().all()


def select_10(session: Session, student_id: int, teacher_id: int):
    """Знайти список курсів, які певному студенту читає певний викладач."""
    # Створюємо псевдоніми для таблиць
    SubjectAlias = aliased(Subject)
    GradeAlias = aliased(Grade)

    return session.query(Subject.name) \
        .join(GradeAlias, Subject.id == GradeAlias.subject_id) \
        .filter(GradeAlias.student_id == student_id) \
        .join(SubjectAlias, SubjectAlias.id == GradeAlias.subject_id) \
        .filter(SubjectAlias.teacher_id == teacher_id) \
        .distinct().all()

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/my-postgres"

    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Перевірка функцій
    print("Top 5 students by average grade:")
    print(select_1(session))

    print("\nStudent with highest average grade for a specific subject (subject_id=1):")
    print(select_2(session, 1))

    print("\nAverage grades by group for a specific subject (subject_id=1):")
    print(select_3(session, 1))

    print("\nOverall average grade:")
    print(select_4(session))

    print("\nSubjects taught by a specific teacher (teacher_id=1):")
    print(select_5(session, 1))

    print("\nStudents in a specific group (group_id=1):")
    print(select_6(session, 1))

    print("\nGrades of students in a specific group and subject:")
    print(select_7(session, 1, 1))

    print("\nAverage grade for subjects taught by a specific teacher (teacher_id=1):")
    print(select_8(session, 1))

    print("\nSubjects taken by a specific student (student_id=1):")
    print(select_9(session, 1))

    print("\nSubjects taken by a student taught by a specific teacher:")
    print(select_10(session, 1, 1))
