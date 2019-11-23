from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
@app.route('/student_courses')
def students_courses():
    """ info from db """
    db_path = 'E:/SSW-810B/810_startup.db'
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {db_path}"
    else:
        query = "SELECT instructors.CWID, instructors.Name, instructors.Dept, grades.Course, COUNT(*) AS CNT FROM instructors JOIN grades ON CWID = InstructorCWID GROUP BY Name, Dept, Course"

        data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'students': students}
                for cwid, name, department, course, students in db.execute(query)]
        db.close()

        return render_template(
            'students_table.html',
            title='Stevens Repository',
            table_title="Courses and student counts",
            instructors=data
        )



app.run(debug=True)
