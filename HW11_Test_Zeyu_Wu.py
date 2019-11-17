"""
Tset for HW11
@author: Zeyu Wu
Date: 2019-11-16 16:32:16
"""
from HW11_Zeyu_Wu import Repository
import unittest


class TestResult(unittest.TestCase):
    """ test case for hw11 """

    def test_hw11(self):
        """ test info from hw11 """
        path = 'E:/SSW-810B/HW11'
        stevens = Repository(path, willing=False)
        """ test student """
        stu_test = []
        for cwid, student in stevens._students.items():
            if cwid == '10103':
                stu_test.append(student.pt_row())
        self.assertEqual(stu_test, [['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], {'SSW 555', 'SSW 540'}, None]])

        """ test instructor """
        ins = stevens._instructors['98764']
        self.assertEqual(ins._cwid, '98764')
        self.assertEqual(ins._name, 'Cohen, R')
        self.assertEqual(ins._department, 'SFEN')
        self.assertEqual(dict(ins._courses), {'CS 546': 1})

        """ test major """
        maj = stevens._majors['SFEN']
        self.assertEqual(maj._major, 'SFEN')
        self.assertEqual(maj._required, {'SSW 540', 'SSW 555', 'SSW 810'})
        self.assertEqual(maj._electives, {'CS 501', 'CS 546'})

        """ test stu_req&stu_ele """
        for cwid, student in stevens._students.items():
            if cwid == '10103':
                self.assertEqual(list(student.pt_row()), ['10103',  'Jobs, S',  'SFEN',  ['CS 501', 'SSW 810'],  {'SSW 555', 'SSW 540'},  None])

        """ test ins from db """
        db_file = 'E:/SSW-810B/HW11/810_startup.db'
        ins_db = stevens._instructors['98764']
        self.assertEqual(ins_db.pt_row_db(db_file), [('98764', 'Cohen, R', 'SFEN', 'CS 546', 1), ('98762', 'Hawking, S', 'CS', 'CS 501', 1), ('98762', 'Hawking, S', 'CS', 'CS 546', 1), ('98762', 'Hawking, S', 'CS', 'CS 570', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4)])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
