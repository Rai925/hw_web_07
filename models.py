from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    subjects = relationship("Subject", back_populates="teacher")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    students = relationship("Student", back_populates="group")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    # Визначаємо реляцію
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True, index=True)
    grade = Column(Numeric(precision=5, scale=2))
    date = Column(DateTime)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
