from flask import Flask, render_template, request
import pymysql

conn = pymysql.connect(host="localhost", user="root", passwd="", db="clman")
c = conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin', methods=['POST'])
def signin():
    global Email
    Email = request.form['username']
    global password
    password = request.form['password']
    a = c.execute("select Email,Password,Designation from admin where Email=(%s) and Password=(%s)", (Email, password))
    conn.commit()
    result = c.fetchone()
    if result[-1] == 'HOD':
        a = c.execute("select Name,dept,Designation,NOL,PF,PT,Reason,AlternateStaff from hod where Yes='No'")
        conn.commit()
        result = c.fetchone()
        global Name
        Name = result[0]
        global dept
        dept = result[1]
        global Designation
        Designation = result[2]
        global NOL
        NOL = result[3]
        global PF
        PF = result[4]
        global PT
        PT = result[5]
        global Reason
        Reason = result[6]
        global AlternateStaff
        AlternateStaff = result[7]
        return render_template('HOD.html', Name=Name, dept=dept, Designation=Designation, NOL=NOL, PF=PF, PT=PT,
                               Reason=Reason, AlternateStaff=AlternateStaff)
    elif result[-1] == 'Principal':
        a = c.execute("select Name,dept,Designation,NOL,PF,PT,Reason,AlternatStaff from principal where Yes='No'")
        conn.commit()
        result = c.fetchone()
        Name = result[0]
        dept = result[1]
        Designation = result[2]
        NOL = result[3]
        PF = result[4]
        PT = result[5]
        Reason = result[6]
        AlternatStaff = result[7]
        return render_template('Principal.html', Name=Name, dept=dept, Designation=Designation, NOL=NOL, PF=PF, PT=PT,
                               Reason=Reason, AlternatStaff=AlternatStaff)
    elif a != 0:
        return render_template('pass.html')
    else:
        return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    global Name
    Name = request.form['Name']
    global Email
    Email = request.form['email']
    global dept
    dept = request.form['dept']
    global Designation
    Designation = request.form['designation']
    global password
    password = request.form['passwd']
    Yes = 'No'
    c.execute("insert into admin (Name,Dept,Designation,Email,Password,Yes) values(%s,%s,%s,%s,%s,%s)",
              (Name, dept, Designation, Email, password, Yes))
    conn.commit()
    return render_template('index.html')


@app.route('/leave', methods=['POST'])
def leave():
    NOL = request.form['Natureofleave']
    PF = request.form['PeriodFrom']
    PT = request.form['PeriodTo']
    Reason = request.form['Reason']
    Alter = request.form['AlternateStaff']
    c.execute("select Name,dept,Designation from admin where Email=%s ", (Email))
    conn.commit()
    result = c.fetchone()
    name = result[0]
    dept = result[1]
    Designation = result[2]
    Yes = 'No'
    c.execute(
        "insert into hod(Name,dept,Designation,NOL,PF,PT,Reason,AlternateStaff,Yes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (name, dept, Designation, NOL, PF, PT, Reason, Alter, Yes))
    c.execute(
        "insert into admin(Name,dept,Designation,Natureofleave,PeriodFrom,PeriodTo,Reason,AlternateStaff,Yes,Email,Password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (name, dept, Designation, NOL, PF, PT, Reason, Alter, Yes, Email, password))
    conn.commit()
    return render_template('Onclear.html')


@app.route('/HOD', methods=['POST'])
def hod():
    Y = request.form['Y/N']
    c.execute("Update hod set Yes=%s where Name=%s", (Y, Name))
    if Y == 'Yes' or Y == 'YES':
        Y = 'No'
        c.execute("insert into principal values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                  (Name, dept, Designation, NOL, PF, PT, Reason, AlternateStaff, Y))
    conn.commit()
    return render_template('Onclear.html')


@app.route('/principal', methods=['POST'])
def principal():
    Y = request.form['Y/N']
    c.execute("Update principal set Yes=%s where Name=%s", (Y, Name))
    c.execute("Update admin set Yes=%s where Name=%s", (Y, Name))
    conn.commit()
    return render_template('Onclear.html')


if __name__ == "__main__":
    app.run(debug=True)
