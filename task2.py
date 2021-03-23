import statistics
import json
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

schools = {}


def search_class(sql, class_name):
    for class_group in schools[sql]:
        if class_group['class'] == class_name:
            return class_group


def search_student_in_class(sql, class_name, subject, st_name, st_surname):
    class_gr = search_class(sql, class_name)
    for cl in class_gr['subject']:
        if cl['name'] == subject:
            for st in cl['students']:
                if st['name'] == st_name and st['surname'] == st_surname:
                    return st


def add_school(school):
    schools[school] = []


def add_class(sql, class_name):
    schools[sql].append({"class": class_name, "subject": []})


def add_subjects(sql, class_name, subjects):
    class_gr = search_class(sql, class_name)
    for sub in subjects:
        class_gr['subject'].append({"name": sub, "students": []})


def add_student(sql, class_name, st_name, st_surname):
    class_gr = search_class(sql, class_name)
    for sub in class_gr['subject']:
        sub['students'].append({'name': st_name,
                                "surname": st_surname,
                                "grades": [], "attendance": []})


def add_grade_attend(sql, class_name, subject, st_name, st_surname, grades, attend):
    student = search_student_in_class(sql, class_name, subject, st_name, st_surname)
    student['grades'].extend(grades)
    student['attendance'].extend(attend)


def get_avg_stud(sql, class_name, subject, student_name, student_surname):
    st = search_student_in_class(sql, class_name, subject, student_name, student_surname)
    return round(statistics.mean(st['grades']), 2), round(100 * sum(st['attendance']) / len(st['attendance']))


def show_statistics_class(sql, class_name):
    logging.info('Displaying class average - {}'.format(class_name))
    class_gr = search_class(sql, class_name)
    tot_avg = 0
    tot_attend = 0
    stud = 0
    for sub in class_gr['subject']:
        logging.info('{}'.format(sub['name']))
        for student in sub['students']:
            result = get_avg_stud(sql, class_name, sub['name'], student['name'], student['surname'])
            stud += 1
            tot_avg += result[0]
            tot_attend += result[1]
            logging.info('Student {} {} average score - {} and attendance {}%'.format(student['name'],
                        student['surname'], result[0], result[1]))
    logging.info('Total class {} average score - {} and attendance {}%\n\n'.format(class_name, round(tot_avg/stud, 2), round(tot_attend/stud, 2)))


def show_statistics_student(school, class_name, student_name, student_surname):
    grades = 0
    attendance = 0
    subj = 0
    class_gr = search_class(school, class_name)
    for sub in class_gr['subject']:
        res = get_avg_stud(school, class_name, sub['name'], student_name, student_surname)
        subj += 1
        grades += res[0]
        attendance += res[1]
    logging.info('Student {} {} average score overall - {} and attendance {}%\n\n'.format(student_name, student_surname, round(grades / subj), round(attendance / subj)))


if __name__ == "__main__":
    add_school("Highschool")

    add_class("Highschool", "1A")
    add_subjects("Highschool", "1A", ['math', 'chemistry', 'physics'])

    add_student('Highschool', '1A', 'John', 'Smith')
    add_grade_attend('Highschool', '1A', 'math', 'John', 'Smith', [5, 4, 3, 2, 5], [1, 0, 1, 1, 1])
    add_grade_attend('Highschool', '1A', 'physics', 'John', 'Smith', [2, 4, 1, 2, 5], [1, 0, 0, 1, 1])
    add_grade_attend('Highschool', '1A', 'chemistry', 'John', 'Smith', [3, 3, 3, 2, 5], [1, 1, 1, 1, 1])

    add_student('Highschool', '1A', 'Oliver', 'Brown')
    add_grade_attend('Highschool', '1A', 'math', 'Oliver', 'Brown', [3, 4, 4, 4, 2], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1A', 'physics', 'Oliver', 'Brown', [4, 4, 4, 4, 2], [1, 0, 1, 1, 1])
    add_grade_attend('Highschool', '1A', 'chemistry', 'Oliver', 'Brown', [5, 4, 4, 4, 5], [1, 1, 1, 1, 1])

    add_student('Highschool', '1A', 'Amelia', 'Jones')
    add_grade_attend('Highschool', '1A', 'math', 'Amelia', 'Jones', [2, 5, 5, 4, 5], [1, 1, 0, 1, 1])
    add_grade_attend('Highschool', '1A', 'physics', 'Amelia', 'Jones', [3, 5, 4, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1A', 'chemistry', 'Amelia', 'Jones', [2, 3, 2, 4, 5], [1, 1, 0, 1, 1])

    add_class('Highschool', '1B')
    add_subjects('Highschool', '1B', ['math', 'physics', 'chemistry'])

    add_student('Highschool', '1B', 'Emily', 'Evans')
    add_grade_attend('Highschool', '1B', 'math', 'Emily', 'Evans', [4, 5, 3, 5, 5], [1, 0, 1, 0, 1])
    add_grade_attend('Highschool', '1B', 'physics', 'Emily', 'Evans', [4, 5, 3, 5, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1B', 'chemistry', 'Emily', 'Evans', [3, 1, 3, 5, 5], [1, 1, 1, 0, 1])

    add_student('Highschool', '1B', 'Jessica', 'Davis')
    add_grade_attend('Highschool', '1B', 'math', 'Jessica', 'Davis', [5, 5, 3, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1B', 'physics', 'Jessica', 'Davis', [2, 2, 3, 4, 5], [0, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1B', 'chemistry', 'Jessica', 'Davis', [4, 5, 3, 4, 5], [1, 1, 1, 1, 1])

    add_student('Highschool', '1B', 'Oscar', 'Jones')
    add_grade_attend('Highschool', '1B', 'math', 'Oscar', 'Jones', [5, 1, 2, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1B', 'physics', 'Oscar', 'Jones', [5, 5, 4, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Highschool', '1B', 'chemistry', 'Oscar', 'Jones', [1, 1, 2, 4, 5], [1, 1, 1, 1, 1])

    show_statistics_class('Highschool', '1A')
    show_statistics_student('Highschool', '1B', 'Emily', 'Evans')

    add_school("Junior Highschool")

    add_class("Junior Highschool", "3A")
    add_subjects("Junior Highschool", "3A", ['english', 'history', 'art'])

    add_student('Junior Highschool', '3A', 'Lily', 'Roberts')
    add_grade_attend('Junior Highschool', '3A', 'english', 'Lily', 'Roberts', [5, 4, 1, 2, 5], [1, 0, 1, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'history', 'Lily', 'Roberts', [5, 4, 1, 2, 5], [1, 0, 0, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'art', 'Lily', 'Roberts', [3, 3, 1, 2, 5], [0, 0, 1, 1, 1])

    add_student('Junior Highschool', '3A', 'George', 'Martin')
    add_grade_attend('Junior Highschool', '3A', 'english', 'George', 'Martin', [4, 4, 2, 5, 2], [0, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'history', 'George', 'Martin', [4, 2, 5, 4, 2], [1, 0, 1, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'art', 'George', 'Martin', [5, 4, 5, 4, 5], [1, 0, 1, 1, 1])

    add_student('Junior Highschool', '3A', 'Harry', 'Williams')
    add_grade_attend('Junior Highschool', '3A', 'english', 'Harry', 'Williams', [2, 5, 5, 4, 5], [1, 1, 0, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'history', 'Harry', 'Williams', [3, 5, 4, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '3A', 'art', 'Harry', 'Williams', [2, 3, 2, 4, 5], [1, 1, 0, 1, 1])

    add_class('Junior Highschool', '2B')
    add_subjects('Junior Highschool', '2B', ['math', 'science', 'literature'])

    add_student('Junior Highschool', '2B', 'Mia', 'Johnson')
    add_grade_attend('Junior Highschool', '2B', 'math', 'Mia', 'Johnson', [4, 5, 3, 2, 5], [1, 0, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'science', 'Mia', 'Johnson', [4, 5, 3, 2, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'literature', 'Mia', 'Johnson', [3, 1, 3, 1, 5], [1, 1, 1, 0, 1])

    add_student('Junior Highschool', '2B', 'Liam', 'Murphy')
    add_grade_attend('Junior Highschool', '2B', 'math', 'Liam', 'Murphy', [5, 5, 5, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'science', 'Liam', 'Murphy', [2, 2, 5, 4, 5], [0, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'literature', 'Liam', 'Murphy', [4, 4, 3, 4, 5], [1, 1, 1, 1, 1])

    add_student('Junior Highschool', '2B', 'Emma', 'Levin')
    add_grade_attend('Junior Highschool', '2B', 'math', 'Emma', 'Levin', [3, 1, 2, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'science', 'Emma', 'Levin', [4, 5, 4, 4, 5], [1, 1, 1, 1, 1])
    add_grade_attend('Junior Highschool', '2B', 'literature', 'Emma', 'Levin', [1, 5, 2, 4, 5], [1, 1, 1, 1, 1])

    show_statistics_class('Junior Highschool', '2B')
    show_statistics_student('Junior Highschool', '3A', 'George', 'Martin')

    with open('mydiary.json', 'w') as f:
        json.dump(schools, f, indent=4)

    with open('mydiary.json', 'r') as f:
        data = json.load(f)
    print(json.dumps(data, indent=4, sort_keys=True))
    f.close()