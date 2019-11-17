"""
HW11
@author: Zeyu Wu
Date: 2019-11-13 15:31:40
"""
from HW08_Zeyu_Wu import file_reading_gen
from prettytable import PrettyTable
from collections import defaultdict
import sqlite3
import os


class Student:
    """ class for student """
    PT_FIELDS = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

    def __init__(self, cwid, name, major_name, major):
        """ define attributes for student """
        self._cwid = cwid
        self._name = name
        self._major_name = major_name
        self._major = major
        self._course = defaultdict(str)  # store grade for the course

    def add_course(self, course, grade):
        """ add courses and grades for student """
        self._course[course] += grade
        return self._course[course]

    def pt_row(self):
        """ return student information for pt """
        passed = self._major.passing_grades(self._course)
        rem_required = self._major.remaining_required(self._course)
        rem_elective = self._major.remaining_elective(self._course)
        if rem_required == set():
            rem_required = None
        return [self._cwid, self._name, self._major_name, sorted(passed), rem_required, rem_elective]


class Instructor:
    """ class for instructor """
    PT_FIELDS = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid, name, department):
        """ define attributes for instructor """
        self._cwid = cwid
        self._name = name
        self._department = department
        self._courses = defaultdict(int)  # store the number of students in the course

    def add_student_number(self, course):
        """ add the number of students for each course for instructor """
        self._courses[course] += 1
        return self._courses[course]

    def pt_row(self):
        """ return instructor information for pt """
        for course, students, in self._courses.items():
            yield [self._cwid, self._name, self._department, course, students]

    def pt_row_db(self, path):
        """ return instructor information from .db """
        try:
            db = sqlite3.connect(path)
        except sqlite3.OperationalError:
            print(f"{path} can't be opened!")
        else:
            return list(db.execute("""SELECT instructors.CWID, instructors.Name, instructors.Dept, grades.Course, COUNT(*) AS CNT FROM instructors JOIN grades ON CWID = InstructorCWID GROUP BY Name, Dept, Course"""))


class Repository:
    """ class for repository """
    def __init__(self, path, willing=False):
        self._students = dict()
        self._instructors = dict()
        self._majors = dict()
        self._get_majors(os.path.join(path, 'majors.txt'))  # TODO: complete this
        self._get_student(os.path.join(path, 'students.txt'))
        self._get_instructor(os.path.join(path, 'instructors.txt'))
        self._get_grades(os.path.join(path, 'grades.txt'))
        if willing:
            self.prettytable_major()  # TODO: complete method: pt_mjr
            self.prettytable_instructor()
            self.prettytable_ins_db(os.path.join(path, '810_startup.db'))
            self.prettytable_student()

    def _get_student(self, path):
        """ get student information """
        try:
            for cwid, name, major_name in file_reading_gen(path, 3, sep='\t', header=True):
                if cwid not in self._students:
                    if major_name not in self._majors:
                        print(f"{major_name} not exist in majors.txt!")
                    else:
                        self._students[cwid] = Student(cwid, name, major_name, self._majors[major_name])
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_instructor(self, path):
        """ get instructor information """
        try:
            for cwid, name, department in file_reading_gen(path, 3, sep='\t', header=True):
                self._instructors[cwid] = Instructor(cwid, name, department)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_grades(self, path):
        """ get grades from grades.txt """
        try:
            for student_cwid, course, grade, instructor_cwid in file_reading_gen(path, 4, sep='\t', header=True):
                if student_cwid in self._students:
                    self._students[student_cwid].add_course(course, grade)
                else:
                    print(f"Found grade for unknown student {student_cwid}")
                if instructor_cwid in self._instructors:
                    self._instructors[instructor_cwid].add_student_number(course)
                else:
                    print(f"Found student for unknown instructor {instructor_cwid}")
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def _get_majors(self, path):  # TODO: deal with the function
        """ get major information """
        try:
            for major, flag, course in file_reading_gen(path, 3, sep='\t', header=True):  # TODO: here!
                if major not in self._majors:
                    self._majors[major] = Major(major)  # TODO: here!
                self._majors[major].add_course(flag, course)
        except FileNotFoundError as fnfe:
            print(fnfe)
        except ValueError as ve:
            print(ve)

    def prettytable_student(self):
        """ use PrettyTable to print student information """
        pt = PrettyTable()
        pt.field_names = Student.PT_FIELDS
        for student in self._students.values():
            pt.add_row(student.pt_row())
        print("Student Summary\n", pt)

    def prettytable_instructor(self):
        """ use PrettyTable to print instructor information """
        pt = PrettyTable()
        pt.field_names = Instructor.PT_FIELDS
        for instructor in self._instructors.values():
            for row in instructor.pt_row():
                pt.add_row(row)
        print("Instructor Summary\n", pt)

    def prettytable_major(self):
        """ use PrettyTable to print major information """
        pt = PrettyTable()
        pt.field_names = Major.PT_FIELDS
        for major in self._majors.values():
            pt.add_row(major.pt_row())
        print("Major Summary\n", pt)

    def prettytable_ins_db(self, path):
        """ prettytable for information from the db """
        pt = PrettyTable()
        pt.field_names = Instructor.PT_FIELDS
        for row in Instructor.pt_row_db(self, path):
            pt.add_row(row)
        print("Instructor Summary by .db\n", pt)


class Major:
    """ class for major """
    PT_FIELDS = ['Major', 'Required', 'Electives']
    PASSING_GRADES = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, major):
        """ define attributes for major """
        self._major = major
        self._required = set()
        self._electives = set()

    def add_course(self, flag, course):  # TODO: Every time disappears???
        """ add course for required or elective """
        if flag.upper() == 'R':
            self._required.add(course)
        elif flag.upper() == 'E':
            self._electives.add(course)
        else:
            raise ValueError(f"Unexpected flag {flag} founded!")

    def remaining_required(self, courses):  # TODO
        """ for remaining required course """
        remain_req = list(self._required)[:]
        for course, grade in courses.items():
            if course in self._required:
                if grade in self.PASSING_GRADES:
                    remain_req.remove(course)
        return set(remain_req)

    def remaining_elective(self, courses):  # TODO
        """ for remaining elective course """
        remain_elc = list(self._electives)[:]
        for course, grade in courses.items():
            if course in remain_elc:
                if grade in self.PASSING_GRADES:
                    remain_elc.remove(course)
        if len(remain_elc) != len(self._electives):
            return None
        else:
            return set(remain_elc)

    def passing_grades(self, courses):
        """ return a set of completed courses """
        return [course for course, grade in courses.items() if grade in Major.PASSING_GRADES]

    def pt_row(self):
        """ return major information for pt """
        return [self._major, self._required, self._electives]


def main():
    """ run the code """
    stevens = Repository("E:/SSW-810B/HW11", willing=True)  # files from Canvas


if __name__ == '__main__':
    main()
