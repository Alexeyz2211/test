from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from db import Base


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False)


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True, nullable=False)
    students = relationship("Student", backref="group")


class Subject(Base):
    __tablename__ = "subject"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teachers = relationship("Teacher", backref="subject")
