import sys
import click
from db import Base, engine, Session

from models import Student, Group, Subject, Teacher


@click.group()
@click.version_option("1.0.0")
def main():
    """A CVE Search and Lookup CLI"""
    print("Приветствую")
    pass


@main.command()
def create_group():
    """Создает запись о группе в базе данных"""
    group_data = {}
    while "number" not in group_data:
        number = input("Введите номер группы: ")
        if len(number) == 0:
            click.echo("Введите несколько символов.")
        else:
            group_data["number"] = number
    with Session() as session:
        session.add(Group(**group_data))
        session.commit()
        click.echo("Группа успешно добавлена.")


@main.command()
def create_subject():
    """Создает запись о предмете в базе данных"""
    subject_data = {}
    while "name" not in subject_data:
        name = input("Введите название предмата: ")
        if len(name) == 0:
            click.echo("Введите несколько символов.")
        else:
            subject_data["name"] = name
    with Session() as session:
        session.add(Subject(**subject_data))
        session.commit()
        click.echo("Предмет успешно добавлен.")


@main.command()
def create_student():
    """Создает запись о студенте в базе данных"""
    student_data = {}
    while "name" not in student_data:
        name = input("Введите имя студента: ")
        if len(name) < 5:
            click.echo("Имя студента должно быть больше 5 символов")
        else:
            student_data["name"] = name

    with Session() as session:
        groups = session.query(Group).all()
        if not groups:
            click.echo("Сначала нужно создать группу.")
            return
        group_mapper = {g.number: g for g in groups}
        while "group_id" not in student_data:
            click.echo("Доступные группы : " + ", ".join(group_mapper.keys()))
            group_number = input("Введите группу из списка: ")
            if group_number not in group_mapper:
                click.echo("Вы ввели группу не из списка.")
                continue
            student_data["group_id"] = group_mapper[group_number].id
        session.add(Student(**student_data))
        session.commit()
        click.echo("Студент успешно добавлен.")


@main.command()
def create_teacher():
    """Создает запись о преподователе в базе данных"""
    teacher_data = {}
    while "name" not in teacher_data:
        name = input("Введите имя препадователя: ")
        if len(name) == 0:
            click.echo("Введите несколько символов.")
        else:
            teacher_data["name"] = name

    with Session() as session:
        subjects = session.query(Subject).all()
        if not subjects:
            click.echo("Сначала нужно создать предмет.")
            return
        subject_mapper = {s.name: s for s in subjects}
        while "subject_id" not in teacher_data:
            click.echo("Доступные предметы: " + ", ".join(subject_mapper.keys()))
            subject_name = input("Введите предмет из списка: ")
            if subject_name not in subject_mapper:
                click.echo("Вы ввели имя не из списка.")
                continue
            teacher_data["subject_id"] = subject_mapper[subject_name].id
        session.add(Teacher(**teacher_data))
        session.commit()
        click.echo("Преподователь успешно добавлен.")


@main.command()
def get_students():
    """Показывает всех студентов"""
    with Session() as session:
        students = session.query(Student).all()
        students = [f"ID: {s.id}. Имя студента: {s.name}" for s in students]
        click.echo(students)


@main.command()
def get_teachers():
    """Покказывает всех преподователей"""
    with Session() as session:
        teachers = session.query(Teacher).all()
        teachers = [f"ID: {t.id}. Имя преподователя: {t.name}" for t in teachers]
        click.echo(teachers)


@main.command()
def get_subjects():
    """Показывает все имющиеся предметы"""
    with Session() as session:
        subjects = session.query(Subject).all()
        subjects = [f"ID: {s.id}. Наименование предмета: {s.name}" for s in subjects]
        click.echo(subjects)


@main.command()
def get_groups():
    """Показывает все имеющиеся группы"""
    with Session() as session:
        groups = session.query(Group).all()
        groups = [f"ID: {g.id}. Номер: {g.number}" for g in groups]
        click.echo(groups)


@main.command()
@click.option("-st", required=True, type=int)
def delete_student(st):
    """Удаляет из базы данных студента"""
    with Session() as session:
        student = session.query(Student).get(st)
        if not student:
            click.echo("Вы ввели номер не существующего студента")
            return
        session.delete(student)
        session.commit()
        click.echo(f"Студент {student.name} с ID {st} успешно удален.")


@main.command()
@click.option("-t", required=True, type=int)
def delete_teacher(t):
    """Удаляет из базы данных преподователя"""
    with Session() as session:
        teacher = session.query(Teacher).get(t)
        if not teacher:
            click.echo("Вы ввели номер не существующего преподователя")
            return
        session.delete(teacher)
        session.commit()
        click.echo(f"Преподователь {teacher.name} с ID {t} успешно удален.")


@main.command()
@click.option("-g", required=True, type=int)
def delete_group(g):
    """Удаляет из базы данных группу"""
    with Session() as session:
        group = session.query(Group).get(g)
        if not group:
            click.echo("Вы ввели номер не существующей группы.")
            return
        session.delete(group)
        session.commit()
        click.echo(f"Группа {group.number} с ID {g} успешно удалена.")


@main.command()
@click.option("-s", required=True, type=int)
def delete_subject(s):
    """Удаляет из базы данных предмет"""
    with Session() as session:
        subject = session.query(Subject).get(s)
        if not subject:
            click.echo("Вы ввели номер не существующего предмета.")
            return
        session.delete(subject)
        session.commit()
        click.echo(f"Предмет {subject.name} с ID {s} успешно удален.")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    args = sys.argv
    main()
