from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

from models.Contact import Base
from models.Student import Student
from models.Professor import Professor

from exceptions.InvalidNameError import InvalidNameError
from exceptions.InvalidUsernameError import InvalidUsernameError
from exceptions.InvalidExtensionError import InvalidExtensionError
from exceptions.InvalidDepartmentError import InvalidDepartmentError
from exceptions.InvalidMajorError import InvalidMajorError

from log.Log import Log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from constants import constants

import os

from datetime import datetime


app = Flask(__name__)

engine = create_engine(constants.DATABASE_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

# Professor Endpoints

professorsURL = '/professors'
professorID = '/<int:professor_id>'

def queryProfessors():
    return session.query(Professor).all()


def getProfessor(professor_id):
    return session.query(Professor).filter_by(id=professor_id).one()


@app.route('/')
def home():
    return render_template('home.html')


@app.route(professorsURL)
def showProfessors():
    log(str(request.url_rule), request.method)
    return render_template('professors.html', professors=queryProfessors())


@app.route(professorsURL + '/json')
def showProfessorsJSON():
    log(str(request.url_rule), request.method)
    return jsonify(professors=[p.serialize for p in queryProfessors()])


@app.route(professorsURL + professorID)
def showProfessor(professor_id):
    log(professorsURL + '/' + str(professor_id), request.method)
    return render_template('professor.html', professor=getProfessor(professor_id))


@app.route(professorsURL + professorID + '/json')
def showProfessorJSON(professor_id):
    log(professorsURL + '/' + str(professor_id) + '/json', request.method)
    return jsonify(Professor=getProfessor(professor_id).serialize)


@app.route(professorsURL + '/new', methods=['GET', 'POST'])
def newProfessor():
    log(str(request.url_rule), request.method)
    if request.method == 'POST':
        try:
            newProf = Professor(name=request.form['name'],
                                username=request.form['username'],
                                extension=request.form['extension'],
                                department=request.form['department'])
            session.add(newProf)
            session.commit()
        except (InvalidNameError, InvalidUsernameError, InvalidExtensionError, InvalidDepartmentError) as e:
            session.rollback()
            flash(str(e))
            return redirect(url_for('showProfessors'), 400)
        except IntegrityError:
            session.rollback()
            flash(request.form['username'] + constants.DUPLICATE_USERNAME)
            return redirect(url_for('showProfessors'), 400)

        return redirect(url_for('showProfessors'), 201)
    else:
        return render_template('newProfessor.html')


@app.route(professorsURL + professorID + '/delete', methods=['GET', 'POST'])
def deleteProfessor(professor_id):
    log(professorsURL + '/' + str(professor_id) + '/delete', request.method)
    professor = getProfessor(professor_id)
    if request.method == 'POST':
        session.delete(professor)
        session.commit()
        return redirect(url_for('showProfessors'))
    else:
        return render_template('deleteProfessor.html', professor=professor)


@app.route(professorsURL + professorID + '/edit', methods=['GET', 'POST'])
def editProfessor(professor_id):
    log(professorsURL + '/' + str(professor_id) + '/edit', request.method)
    professor = getProfessor(professor_id)
    if request.method == 'POST':
        try:
            if request.form['name']:
                professor.name = request.form['name']
            if request.form['username']:
                professor.username = request.form['username']
            if request.form['extension']:
                professor.extension = request.form['extension']
            if request.form['department']:
                professor.department = request.form['department']

            session.add(professor)
            session.commit()
            return redirect(url_for('showProfessors'))
        except (InvalidNameError, InvalidUsernameError, InvalidExtensionError, InvalidDepartmentError) as e:
            session.rollback()
            flash('Error: ' + str(e))
            return render_template('professor.html', professor=getProfessor(professor_id)), 400
        except IntegrityError:
            session.rollback()
            flash(request.form['username'] + constants.DUPLICATE_USERNAME)
            return render_template('professor.html', professor=getProfessor(professor_id)), 400
    else:
        return render_template('editProfessor.html', professor=professor)

# Student Endpoints

studentsURL = '/students'
studentID = '/<int:student_id>'

def queryStudents():
    return session.query(Student).all()


def getStudent(student_id):
    return session.query(Student).filter_by(id=student_id).one()


@app.route('/students')
def showStudents():
    log(str(request.url_rule), request.method)
    return render_template('students.html', students=queryStudents())


@app.route('/students/json')
def showStudentsJSON():
    log(str(request.url_rule), request.method)
    return jsonify(students=[s.serialize for s in queryStudents()])


@app.route('/students/new', methods=['GET', 'POST'])
def newStudent():
    log(str(request.url_rule), request.method)
    if request.method == 'POST':
        try:
            newStudent = Student(name=request.form['name'],
                                 username=request.form['username'],
                                 major=request.form['major'])
            print(newStudent.username)
            session.add(newStudent)
            session.commit()
        except (InvalidNameError, InvalidUsernameError, InvalidMajorError) as e:
            session.rollback()
            flash('Error: ' + str(e))
            return redirect(url_for('showStudents'), 400)
        except IntegrityError:
            session.rollback()
            flash(request.form['username'] + constants.DUPLICATE_USERNAME)
            return redirect(url_for('showStudents'), 400)
        return redirect(url_for('showStudents'), 201)
    else:
        return render_template('newStudent.html')


@app.route('/students/<int:student_id>')
def showStudent(student_id):
    log(studentsURL + '/' + str(student_id), request.method)
    return render_template('student.html', student=getStudent(student_id))


@app.route('/students/<int:student_id>/json')
def showStudentJSON(student_id):
    log(studentsURL + '/' + str(student_id) + '/json', request.method)
    return jsonify(Student=getStudent(student_id).serialize)


@app.route('/students/<int:student_id>/delete', methods=['GET', 'POST'])
def deleteStudent(student_id):
    log(studentsURL + '/' + str(student_id) + '/delete', request.method)
    student = getStudent(student_id)
    if request.method == 'POST':
        session.delete(student)
        session.commit()
        return redirect(url_for('showStudents'))
    else:
        return render_template('deleteStudent.html', student=student)


@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def editStudent(student_id):
    log(studentsURL + '/' + str(student_id) + '/edit', request.method)
    student = getStudent(student_id)
    if request.method == 'POST':
        try:
            if request.form['name']:
                student.name = request.form['name']
            if request.form['username']:
                student.username = request.form['username']
            if request.form['major']:
                student.major = request.form['major']

            session.add(student)
            session.commit()
            return redirect(url_for('showStudents'))
        except (InvalidNameError, InvalidUsernameError, InvalidMajorError) as e:
            session.rollback()
            flash('Error: ' + str(e))
            return render_template('student.html', student=getStudent(student_id)), 400
        except IntegrityError:
            session.rollback()
            flash(request.form['username'] + constants.DUPLICATE_USERNAME)
            return render_template('student.html', student=getStudent(student_id)), 400
    else:
        return render_template('editStudent.html', student=student)

# Logging

def log(url, method):
    log = Log()

    log.time = datetime.now()
    log.url = url
    log.method = method

    log_file = open(constants.LOG_FILE, "a")

    log_file.write(str(log.url) + "\t" + log.method + "\t" + log.time.strftime('%Y-%m-%d %H:%M:%S') + "\n")

    log_file.close()

def makeLogFile():
    filename = constants.LOG_FILE

    if os.path.isfile(filename):
        os.remove(filename)

    file = open(filename, 'w+')
    file.close()

if __name__ == '__main__':

    makeLogFile()

    app.secret_key = 'secret_key'

    app.run(debug=True)
