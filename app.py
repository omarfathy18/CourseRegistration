from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'CourseRegistration'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
db = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        new_line = db.connection.cursor()
        new_line.execute('select email from users')
        real_email = new_line.fetchall()
        list1 = []
        for i in real_email:
            list1.append(i['email'])
        if email in list1:
            new_line.execute(f'select pwd from users where email="{email}"')
            real_pwd = new_line.fetchone()
            real_pwd = real_pwd['pwd']
            if pwd == real_pwd:
                new_line.execute(f'select code from users where email="{email}"')
                code = new_line.fetchone()['code']
                session['user'] = code
                return redirect('/final')
            else:
                flash('incorrect password')
                return redirect('/')
        else:
            flash('email not found')
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name1 = request.form['name1']
        name2 = request.form['name2']
        name = name1 + ' ' + name2
        email = request.form['email']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        usercode = request.form['code']
        new_line = db.connection.cursor()
        new_line.execute('select email from users')
        list1 = [email['email'] for email in new_line]
        if email in list1:
            flash('Used email try another one')
            return redirect('/register')
        while True:
            if pwd1 == pwd2:
                break
            else:
                flash('Passwords are not the same')
                return redirect('/register')
        new_line.execute('select code from users')
        list1 = [code['code'] for code in new_line]
        if usercode in list1:
            flash("This is not your code")
            return redirect('/register')
        else:
            sql = 'insert into users (name,email,pwd,code) values (%s,%s,%s,%s)'
            values = (name, email, pwd1, usercode)
            new_line.execute(sql, values)
            new_line.execute(f'create table courses{usercode} as select * from courses')
            new_line.execute(f'create table registered{usercode} like registered')
            db.connection.commit()
            return redirect('/')
    else:
        return render_template('register.html')


@app.route('/courses', methods=['POST', 'GET'])
def courses():
    if request.method == 'POST':
        usercode = session['user']
        date1 = date.today()
        date1 = str(date1)
        date1 = date1.split('-')
        date1.reverse()
        date1 = '-'.join(date1)
        if date1 <= '15-10-2022':
            new_line = db.connection.cursor()
            new_line.execute(f'select * from courses{usercode}')
            courses = new_line.fetchall()
            new_line.execute(f'select * from registered{usercode}')
            registered = new_line.fetchall()
            hours = 0
            number = 0
            for i in registered:
                hours = hours + int(i['hours'])
                number = number + 1
            return render_template('courses.html', courses=courses, registered=registered, hours=hours, number=number)
        else:
            flash("You can't change courses now The deadline was 15-10-2022")
            return redirect('/final')
    else:
        if 'user' in session:
            usercode = session['user']
            date1 = date.today()
            date1 = str(date1)
            date1 = date1.split('-')
            date1.reverse()
            date1 = '-'.join(date1)
            if date1 <= '15-10-2022':
                new_line = db.connection.cursor()
                new_line.execute(f'select * from courses{usercode}')
                courses = new_line.fetchall()
                new_line.execute(f'select * from registered{usercode}')
                registered = new_line.fetchall()
                hours = 0
                number = 0
                for i in registered:
                    hours = hours + int(i['hours'])
                    number = number + 1
                return render_template('courses.html', courses=courses, registered=registered, hours=hours, number=number)
            else:
                flash("You can't change courses now...the deadline was 15-10-2022")
                return render_template('final.html')
        else:
            flash('Please login first')
            return redirect('/')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        code = request.form['code']
        usercode = session['user']
        new_line = db.connection.cursor()
        new_line.execute(f'select * from registered{usercode}')
        list1 = new_line.fetchall()
        c = 0
        for i in list1:
            c = c + 1
        if c == 5:
            flash("You can't register more than 5 courses")
            return redirect('/courses')
        else:
            usercode = session['user']
            new_line.execute(f'select * from courses{usercode} where code="{code}"')
            course = new_line.fetchall()[0]
            r_code = course['code']
            r_name = course['name']
            r_dr = course['dr']
            r_hours = course['hours']
            r_degree = course['degree']
            new_line = db.connection.cursor()
            new_line.execute(f'delete from courses{usercode} where code="{code}"')
            db.connection.commit()
            sql = f'insert into registered{usercode} (code,name,dr,hours,degree) values (%s,%s,%s,%s,%s)'
            values = (r_code, r_name, r_dr, r_hours, r_degree)
            new_line.execute(sql, values)
            db.connection.commit()
            flash(f'Added {code} Successfully')
            return redirect('/courses')
    else:
        return redirect('/courses')


@app.route('/drop', methods=['POST', 'GET'])
def drop():
    if request.method == 'POST':
        code = request.form['code']
        usercode = session['user']
        new_line = db.connection.cursor()
        new_line.execute(f'select * from registered{usercode} where code="{code}"')
        course = new_line.fetchall()[0]
        r_code = course['code']
        r_name = course['name']
        r_dr = course['dr']
        r_hours = course['hours']
        r_degree = course['degree']
        new_line = db.connection.cursor()
        new_line.execute(f'delete from registered{usercode} where code="{code}"')
        db.connection.commit()
        sql = f'insert into courses{usercode} (code,name,dr,hours,degree) values (%s,%s,%s,%s,%s)'
        values = (r_code, r_name, r_dr, r_hours, r_degree)
        new_line.execute(sql, values)
        db.connection.commit()
        flash(f'Dropped {code} Successfully')
        return redirect('/courses')
    else:
        return redirect('/courses')


@app.route('/final', methods=['POST', 'GET'])
def final():
    if request.method == 'POST':
        usercode = session['user']
        new_line = db.connection.cursor()
        new_line.execute(f'select * from registered{usercode}')
        registered = new_line.fetchall()
        hours = 0
        number = 0
        for i in registered:
            hours = hours + int(i['hours'])
            number = number + 1
        new_line.execute(f'select * from registered{usercode}')
        registered = new_line.fetchall()
        return render_template('final.html', hours=hours, number=number, registered=registered)
    else:
        if 'user' in session:
            usercode = session['user']
            new_line = db.connection.cursor()
            new_line.execute(f'select * from registered{usercode}')
            registered = new_line.fetchall()
            hours = 0
            number = 0
            for i in registered:
                hours = hours + int(i['hours'])
                number = number + 1
            return render_template('final.html', hours=hours, number=number, registered=registered)
        else:
            flash('Please login first')
            return redirect('/')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash('You have logged out')
        return redirect('/')
    else:
        flash('No user in session')
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
