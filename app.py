import csv
from random import randint
from grpc import insecure_channel
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for, flash, session
import numpy as np
import mysql.connector
import os
import pandas as pd
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
import docx2txt
from pyresparser import ResumeParser
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.neighbors import _dist_metrics
# from sklearn.neighbors import _dist_metrics
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['uploadfolder'] = "static/"

mydb = mysql.connector.connect(host="jobseeker.mysql.database.azure.com",port=3306, user="DBadmin", passwd="DBpassword123", database="job_mapper")
cursor = mydb.cursor(buffered=True)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/signup')
def signup():
    return render_template('job_seeker/signup.html')

@app.route('/j_register', methods=["GET", "POST"])
def j_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        mobile = request.form['mobile']
        address = request.form['address']
        gender = request.form['gender']
        age = request.form['age']
        state = request.form['state']
        district = request.form['district']
        image = request.files['image']
        resume = request.files['resume']

        fn1=image.filename
        mypath1=os.path.join('static/photos/', fn1)
        image.save(mypath1)

        fn2=resume.filename
        mypath2=os.path.join('static/resumes/', fn2)
        resume.save(mypath2)

        if password == c_password:
            query = "SELECT UPPER(email) FROM job_seeker"
            cursor.execute(query)
            email_data = cursor.fetchall()
            email_data_list = []
            if email_data:
                for i in email_data:
                    email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO job_seeker (name, email, pwd, pno, gender, age, addr, state, dist, pgoto, resume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (name, email, password, mobile, gender, age, address, state, district, mypath1, mypath2)
                cursor.execute(query, values)
                mydb.commit()

                return render_template('job_seeker/j_login.html', message = "Sucessfully Registered!")
            return render_template('job_seeker/j_register.html', message="This email ID is already exists!")
        return render_template('job_seeker/j_register.html', message="Conform password is not match!")
    return render_template('job_seeker/j_register.html')

@app.route('/j_login', methods=["GET", "POST"])
def j_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM job_seeker"
        cursor.execute(query)
        email_data = cursor.fetchall()
        print(11111111111111, email_data)
        email_data_list = []
        if email_data:
            for i in email_data:
                email_data_list.append(i[0])
        print(2222222222, email_data_list)

        if email.upper() in email_data_list:
            query = "SELECT UPPER(pwd) FROM job_seeker WHERE email = %s"
            values = (email,)
            cursor.execute(query, values)
            password__data = cursor.fetchall()
            if password.upper() == password__data[0][0]:
                job_seeker_email = email
                session['job_seeker_email'] = job_seeker_email

                return render_template('job_seeker/job_seekerhome.html')
            return render_template('job_seeker/j_login.html', message= "Invalid Password!!")
        return render_template('job_seeker/j_login.html', message= "This email ID does not exist!")
    return render_template('job_seeker/j_login.html')


@app.route('/signupback', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']

        pno = request.form['pno']
        addr = request.form['addr']
        state = request.form['state']
        d_name = request.form['d_name']
        gender = request.form['gender']

        age = int(request.form['age'])

        file = request.files['filen']
        file_name = file.filename
        print(file_name)
        path = os.path.join(app.config['uploadfolder'], 'profiles/' + file_name)
        print(path)
        file.save(path)

        # f = open(path + file_name,'wb')
        # f.write(file)
        # f.close()

        voters = pd.read_sql_query('SELECT * FROM job_seeker', mydb)
        all_emails = voters.email.values
        if age >= 19:
            if (email in all_emails):
                flash(r'Already Registered', "warning")
            elif pwd == cpwd:
                sql = 'INSERT INTO job_seeker (name, email, pwd, pno , gender, age, addr, state, dist,pgoto) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s)'
                cur = mydb.cursor()
                cur.execute(sql, (name, email, pwd, pno, gender, age, addr, state, d_name, path))
                mydb.commit()
                cur.close()
                flash("Account created successfully", "success")
                return render_template("job_seeker/signup.html")
            else:
                flash("password & confirm password not match", "danger")
        else:
            flash("if age less than 18 than not eligible for voting", "info")
    return render_template('job_seeker/signup.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signinback', methods=['POST', 'GET'])
def signinback():
    if request.method == 'POST':
        username = request.form['email']
        password1 = request.form['pwd']

        sql = "select * from job_seeker where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('signin.html')
        else:
            # session['cid'] = username
            if len(results) > 0:
                session['name'] = results[0][1]
                session['email'] = results[0][2]
                sql = "select * from job_seeker where email='" + username + "'"
                x = pd.read_sql_query(sql, mydb)
                print(x)
                x = x.drop(['id'], axis=1)
                flash("Welcome ", "success")
                print("==============")
                image = results[0][-2]
                print(image)
                return render_template('job_seekerhome.html', msg=results[0][1], image=image, row_val=x.values.tolist())
    return render_template('signin.html')


@app.route('/signinback1', methods=['POST', 'GET'])
def signinback1():
    if request.method == 'POST':
        username = request.form['email']
        password1 = request.form['pwd']

        sql = "select * from employee where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('signin.html')
        else:
            # session['cid'] = username
            if len(results) > 0:
                session['name'] = results[0][1]
                session['email'] = results[0][2]
                session['cname'] = results[0][4]
                sql = "select * from employee where email='" + username + "'"
                x = pd.read_sql_query(sql, mydb)
                print(x)
                x = x.drop(['id'], axis=1)
                flash("Welcome ", "success")
                print("==============")
                image = results[0][-2]
                print(image)
                return render_template('employee/emphome.html', msg=results[0][1], image=image, row_val=x.values.tolist())

    return render_template('signin1.html')


@app.route('/signup1')
def signup1():
    return render_template('employee/signup1.html')

@app.route('/e_register', methods=["GET", "POST"])
def e_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        company = request.form['company']
        job = request.form['job']
        mobile = request.form['mobile']
        address = request.form['address']
        gender = request.form['gender']
        age = request.form['age']
        state = request.form['state']
        district = request.form['district']
        image = request.files['image']
        fn=image.filename
        mypath=os.path.join('static/photos/', fn)
        image.save(mypath)

        if password == c_password:
            query = "SELECT UPPER(email) FROM employee"
            cursor.execute(query)
            email_data = cursor.fetchall()
            email_data_list = []
            if email_data:
                for i in email_data:
                    email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO employee (name, email, pwd, cname, roll, pno, addr, gender, age, state, dist, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (name, email, password, company, job, mobile, address, gender, age, state, district, mypath)
                cursor.execute(query, values)
                mydb.commit()

                return render_template('employee/e_login.html', message = "Sucessfully Registered!")
            return render_template('employee/e_register.html', message="This email ID is already exists!")
        return render_template('employee/e_register.html', message="Conform password is not match!")
    return render_template('employee/e_register.html')


@app.route('/e_login', methods=["GET", "POST"])
def e_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM employee"
        cursor.execute(query)
        email_data = cursor.fetchall()
        email_data_list = []
        if email_data:
            for i in email_data:
                email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(pwd) FROM employee WHERE email = %s"
            values = (email,)
            cursor.execute(query, values)
            password__data = cursor.fetchall()
            if password.upper() == password__data[0][0]:
                employee_email = email
                session['employee_email'] = employee_email

                return render_template('employee/emphome.html')
            return render_template('employee/e_login.html', message= "Invalid Password!!")
        return render_template('employee/e_login.html', message= "This email ID does not exist!")
    return render_template('employee/e_login.html')


@app.route('/signupback1', methods=['POST', 'GET'])
def signupback1():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']

        pno = request.form['pno']
        addr = request.form['addr']
        state = request.form['state']
        d_name = request.form['d_name']
        gender = request.form['gender']
        cname = request.form['cname']
        roll = request.form['roll']
        age = int(request.form['age'])
        file = request.files['filen']
        file_name = file.filename
        print(file_name)
        print(app.config['uploadfolder'])
        path = os.path.join(app.config['uploadfolder'], 'profiles/' + file_name)
        print(path)
        file.save(path)
        print("============================================================================")

        voters = pd.read_sql_query('SELECT * FROM employee', mydb)
        all_emails = voters.email.values
        if age >= 19:
            if (email in all_emails):
                flash(r'Already Registered', "warning")
            elif pwd == cpwd:
                sql = 'INSERT INTO employee (name, email, pwd,cname,roll, pno ,addr, gender, age, state, dist,photo) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)'
                cur = mydb.cursor()
                cur.execute(sql, (name, email, pwd, cname, roll, pno, addr, gender, age, state, d_name, path))
                mydb.commit()
                cur.close()
                flash("Account created successfully", "success")
                return render_template("employee/signup1.html")
            else:
                flash("password & confirm password not match", "danger")
        else:
            flash("if age less than 18 than not eligible for voting", "info")
    return render_template('employee/signup1.html')


@app.route("/signinback2", methods=["POST", "GET"])
def signinback2():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['password']
        if email == 'admin@gmail.com' and pwd == 'admin':
            return render_template('admin/adminhome.html')
        else:
            message = "Invalid Credentials Please Try Again"
            return render_template('admin/signin2.html', message = message)
    return render_template("admin/signin2.html")


@app.route('/upload')
def upload():
    return render_template("job_seeker/upload.html")


@app.route('/signin1home')
def signin1home():
    return render_template("job_seeker/signin1home.html")


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if request.method == "POST":
        file = request.files['f1']
        file_name = file.filename
        path = os.path.join(app.config['uploadfolder'], 'resumes/' + file_name)
        file.save(path)
        job_seeker_email = session['job_seeker_email']
        sql = "UPDATE job_seeker SET resume = %s WHERE email = %s"
        val = (path, job_seeker_email)
        cursor.execute(sql, val)
        mydb.commit()

        return render_template("job_seeker/upload.html", message = "Successfully Updated Resume!")


@app.route('/signin1')
def signin1():
    return render_template('signin1.html')


@app.route('/signin2')
def signin2():
    return render_template('admin/signin2.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route("/forgetback",methods=['POST','GET'])
def forgetback():
    if request.method=="POST":
        empemail = request.form['email']
        sql = "select * from employee where email='%s'"%(empemail)
        cursor.execute(sql)
        data = cursor.fetchall()
        mydb.commit()
        if data !=[]:
            msg ='valid'
            session['empforgotemail'] = empemail
            return render_template('forgot.html',msg=msg)
        else:
            msg="notvalid"
            flash("Provide Valid Email","warning")
            return render_template('signin1.html',msg=msg)
    return render_template('forgot.html',msg='check')

@app.route("/updatepassword",methods=['POST','GET'])
def updatepassword():
    if request.method=="POST":
        form = request.form
        empemail = session['empforgotemail']
        password = form['password']
        confirmpassword =  form['confirmpassword']
        if password == confirmpassword:
            sql = "select * from employee where empemail='%s'"%(empemail)
            cursor.execute(sql)
            data = cursor.fetchall()
            mydb.commit()
            if data:
                sql= "update employee set password='%s' where empemail='%s'"%(password,session['empforgotemail'])
                cursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully","success")
                return redirect(url_for("signin1"))
        else:
             return render_template("signin1.html")

@app.route('/forgot1')
def forgot1():
    return render_template('forgot.html')


@app.route('/forgetback1', methods=['POST', 'GET'])
def forgetback1():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from job_seeker where email='%s'" % (email)
        x = pd.read_sql_query(sql, mydb)
        count = x.values[0][0]
        pwd = x.values[0][2]
        name = x.values[0][1]
        if count == 0:
            flash("Email not valid try again", "info")
            return render_template('forgot.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'Job Mapper Services.'
            mail_content = 'Dear ' + name + ',' + '\n' + msg + pwd + '\n' + '\n' + t + '\n' + t1
            sender_address = ''
            sender_pass = ''
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Job Mapper Services'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("signin1.html")

    return render_template('forgot.html')


@app.route('/adminhome')
def adminhome():
    return render_template('admin/adminhome.html')


@app.route('/view_job_seekers')
def view_job_seekers():
    sql = "select * from job_seeker "
    # x = pd.read_sql_query(sql, mydb)
    cursor.execute(sql, mydb)
    data = cursor.fetchall()
    # x = x.drop(['pwd'], axis=1)
    # x = x.drop(['resume'], axis=1)
    return render_template("admin/view_job_seekers.html", data=data)


@app.route('/view_emlpyers')
def view_emlpyers():
    sql = "select * from employee "
    cursor.execute(sql, mydb)
    data = cursor.fetchall()
    return render_template("view_emlpyers.html", data=data)


@app.route('/emphome')
def emphome():
    return render_template('employee/emphome.html')


@app.route('/add_job')
def add_job():
    return render_template('employee/add_job.html')


@app.route('/add_job_back', methods=['POST', 'GET'])
def add_job_back():
    if request.method == 'POST':
        qual = request.form['qual']
        skill = request.form['skill']
        cname = session.get('cname')
        email = session.get('email')
        exp = request.form['exp']
        salary = request.form['salary']
        notf = request.form['notf']
        loc = request.form['loc']
        desc = request.form['disc']
        roll = request.form['role']
        pno = request.form['pno']
        cemail = request.form['cemail']

        sql = 'INSERT INTO jobs_info (email,cname,role,disc,salary,exp,skill,qual,notf,loc,pno,cemail) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur = mydb.cursor()
        cur.execute(sql, (email, cname, roll, desc, salary, exp, skill, qual, notf, loc, pno, cemail))
        mydb.commit()
        cur.close()
        message = "Added Successfully!"
        return render_template("employee/add_job.html", message = message)
    return render_template('employee/add_job.html')


@app.route('/remove_data')
def remove_data():
    # employee_email = session['employee_email']
    # sql = "select * from jobs_info where email='" + session['email'] + "' "
    sql = "select * from jobs_info"
    x = pd.read_sql_query(sql, mydb)
    # x = x.drop(['email'], axis=1)
    # x = x.drop(['photo'], axis=1)1
    return render_template("employee/remove_data.html", cal_name=x.columns.values, row_val=x.values.tolist())



@app.route('/viewjobnotifivation')
def viewjobnotifivation():
    sql = "select * from jobs_info  "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['id'], axis=1)
    # x = x.drop(['photo'], axis=1)
    return render_template("admin/viewjobnotifivation.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route('/cancel/<s>')
def cancel(s=0):
    sql = "delete from jobs_info where id='%s'" % (s)
    cursor.execute(sql, mydb)
    mydb.commit()
    flash("Data deleted", "info")
    return redirect(url_for('remove_data'))


@app.route('/search')
def search():
    return render_template("job_seeker/search.html")


def get_recommendations(name, cosine_sim, indices, data, m):
    idx = indices[name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    food_indices = [i[0] for i in sim_scores]
    c = data['role'].iloc[food_indices].tolist()
    c += [m]
    return c

@app.route("/searchback",methods=["POST","GET"])
def searchback():
    if request.method == 'POST':
        tfidf = TfidfVectorizer()
        skill = request.form['role']
        sql = "select * from jobs_info where role='%s'" % (skill)
        data = pd.read_sql_query(sql, mydb)
        if data.empty:
            return redirect(url_for("search"))
        else:
            data['skill'] = data['skill'].fillna('')
            tfidf_matrix = tfidf.fit_transform(data['skill'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(data.index, index=data['role']).drop_duplicates()
            c = get_recommendations(skill, cosine_sim, indices, data, skill)
            data = []
            for i in c:
                query = "select * from jobs_info where role='%s'" % (i)
                cursor.execute(query)
                temp = cursor.fetchall()[0]
                data.append(temp)
                mydb.commit()
            return render_template("job_seeker/jobrecomendation.html",data=data)

@app.route("/topredictpage")
def topredictpage():
    return render_template("job_seeker/prediction.html")

@app.route("/j_account")
def j_account():
    query = "SELECT * FROM job_seeker WHERE email = %s"
    val = (session['job_seeker_email'], )
    cursor.execute(query, val)
    data = cursor.fetchall()
    return render_template("job_seeker/j_account.html", data = data)

@app.route("/e_account")
def e_account():
    query = "SELECT * FROM employee WHERE email = %s"
    val = (session['employee_email'], )
    cursor.execute(query, val)
    data = cursor.fetchall()
    return render_template("employee/e_account.html", data = data)

import pickle
@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method == 'POST':																					
        education = int(request.form['education'])
        industry = request.form['experience']
        skills = int(request.form['industry'])
        jobtitle = int(request.form['skills'])
        experience = int(request.form['jobtitle'])
        location = request.form['location']
        salary_range = int(request.form['salary_range'])
        work_hours = int(request.form['work_hours'])
        company_size = int(request.form['company_size'])
        job_level = int(request.form['job_level'])
        remote_option = int(request.form['remote_option'])
        salary_midpoint = int(request.form['salary_midpoint'])

        lee=[[education	,experience,	industry,	skills	,jobtitle,	location,	salary_range,company_size,	work_hours,job_level,remote_option,salary_midpoint]]
        filename = 'random_forest.sav'
        # with open('randomforest.sav', 'rb') as f:
        #     model_data = pickle.load(f)
        model = pickle.load(open(filename, 'rb'))
        # print(model_data)
        result = model.predict(lee)
        result = result[0]

        # print(lee)
        # filename = (r'Decision_job.sav')
        # model = pickle.load(open(filename, 'rb'))
        # result =model.predict(lee)
        # result=result[0]
        if result==0:
            msg = "The Job_type : Accountant"
        elif result==1:
            msg=" The Job_type :  Business Analyst "
        elif result==2:
            msg=" The Job_type :  Customer Support Representative"
        elif result==3:
            msg=" The Job_type :  Data Analyst"
        elif result==4:
            msg=" The Job_type :  Education Professional"
        elif result==5:
            msg=" The Job_type :  Engineer (Non-Software)"
        elif result==6:
            msg=" The Job_type :  Business Analyst "
        elif result==7:
            msg=" The Job_type :  Healthcare Professional"
        elif result==8:
            msg=" The Job_type :  Marketing Specialist "
        elif result==9:
            msg=" The Job_type :  Network Administrator"
        elif result==10:
            msg=" The Job_type :  Product Manager"
        elif result==8:
            msg=" The Job_type :  Project Manager"
        elif result==9:
            msg=" The Job_type :  Network Administrator"
        elif result==10:
            msg=" The Job_type :  Sales Associate"
        else:
            msg= " The Job_type : software Engineer"
        return render_template("job_seeker/prediction.html",result=msg)
    return render_template("job_seeker/prediction.html") 

# @app.route('/load',methods=["POST","GET"])
# def load():
#     if request.method=="POST":
#         files1 = request.files['resume']
#         files2 = request.files['job_description']

#         files1.save(os.path.join('upload', files1.filename))
#         resume = docx2txt.process(files1)
#         print(resume)

#         # Store the job description into a variable
#         files2.save(os.path.join('upload', files2.filename))
#         jd = docx2txt.process(files2)
#         print(jd)

#         # Print the job description
#         print(jd)

#         text = [resume, jd]
#         cv = CountVectorizer()
#         count_matrix = cv.fit_transform(text)

#         print("\nSimilarity Scores:")
#         print(cosine_similarity(count_matrix))

#         matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
#         matchPercentage1 = round(matchPercentage, 2) # round to two decimal
#         # msg = print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")

#         if matchPercentage1>=70:                      
#              m1="Your resume matches about "+ str(matchPercentage)+ "% of the job description. You have a nice resume"
#         else:
#             m1="Your resume matches about "+ str(matchPercentage)+ "% of the job description.You need to work on your resume to improve."
#         from pyresparser import ResumeParser
#         data = ResumeParser(os.path.join('upload', files1.filename)).get_extracted_data()
#         list = data['skills']
#         print(list)
#         data1 = ResumeParser(os.path.join('upload', files2.filename)).get_extracted_data()
#         list1 = data1['skills']

#         matches=[]
#         for item_a in list1:
#             for item_b in list:
#                 if item_a == item_b:
#                      matches.append(item_a)
#         print( matches)
#         # extract email and name
#         email = data['email']
#         name = data['name']

#         msg2="The matching skills are as "+ " ,".join(matches)
#         # get the unmatched skills from the list and list1 
#         unmatched_skills = [item for item in list1 if item not in list]
#         msg3 = "The unmatched skills are as "+ ",".join(unmatched_skills)

#         dir_path = os.getcwd()  # get current working directory
#         all_files = os.listdir(os.path.join(dir_path,'static','resumes'))  # get all files in directory

#         # select 5 random files
#         random_files = random.sample(all_files,5)

#         file_names = [os.path.basename(f) for f in random_files]

#         return render_template('job_seeker/load.html',m1=m1,msg2=msg2, msg3 = msg3,msg4=name,msg5= email , file_names = random_files)

#     return render_template('job_seeker/load.html')
import os
import random
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from docx import Document
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nlp = spacy.load("en_core_web_sm")

# Define the path for upload
app.config['UPLOAD_FOLDER'] = 'upload'

def docx_to_text(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_information(doc):
    name, email = None, None
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        if ent.label_ == "EMAIL" and not email:
            email = ent.text
    return name, email

def get_skills(doc, predefined_skills):
    matcher = spacy.matcher.PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(text) for text in predefined_skills]
    matcher.add("Skills", None, *patterns)
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills.add(span.text)
    return skills

@app.route('/load', methods=["POST", "GET"])
def load():
    if request.method == "POST":
        resume_file = request.files['resume']
        jd_file = request.files['job_description']

        resume_filename = secure_filename(resume_file.filename)
        jd_filename = secure_filename(jd_file.filename)

        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)

        resume_file.save(resume_path)
        jd_file.save(jd_path)

        resume_text = docx_to_text(resume_path)
        jd_text = docx_to_text(jd_path)

        text = [resume_text, jd_text]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)
        
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage_rounded = round(match_percentage, 2)

        if match_percentage_rounded >= 70:
            m1 = f"Your resume matches about {match_percentage_rounded}% of the job description. You have a nice resume."
        else:
            m1 = f"Your resume matches about {match_percentage_rounded}% of the job description. You need to work on your resume to improve."

        # Parsing for skills, email, and name
        resume_doc = nlp(resume_text)
        jd_doc = nlp(jd_text)

        resume_skills = get_skills(resume_doc, predefined_skills={'Python', 'Java', 'SQL'})  # Example skill set
        jd_skills = get_skills(jd_doc, predefined_skills={'Python', 'Java', 'SQL'})

        name, email = extract_information(resume_doc)

        matched_skills = resume_skills.intersection(jd_skills)
        unmatched_skills = jd_skills.difference(resume_skills)

        msg2 = "The matching skills are as " + ", ".join(matched_skills)
        msg3 = "The unmatched skills are as " + ", ".join(unmatched_skills)

        return render_template('job_seeker/load.html', m1=m1, msg2=msg2, msg3=msg3, msg4=name, msg5=email)

    return render_template('job_seeker/load.html')


@app.route("/appliedjobs")
def appliedjobs():
    job_seeker_email = session['job_seeker_email']
    sql = "select * from job_applications where email=%s"
    val = (job_seeker_email,)
    cursor.execute(sql,val)
    data = cursor.fetchall()
    return render_template("job_seeker/applied.html",data=data)

@app.route("/delete_applied_job", methods=["POST"])
def delete_applied_job():
    id = request.form['id']
    sql = "DELETE from job_applications where id = %s"
    val = (id, )
    cursor.execute(sql,val)
    mydb.commit()

    job_seeker_email = session['job_seeker_email']
    sql = "select * from job_applications where email=%s"
    val = (job_seeker_email,)
    cursor.execute(sql,val)
    data = cursor.fetchall()
    return render_template("job_seeker/applied.html",data=data)


@app.route("/applyforjob",methods=['POST','GET'])
def applyforjob():
    if request.method == 'POST':
        id = request.form['id']

        job_seeker_email = session['job_seeker_email']
        query = "SELECT name FROM job_seeker WHERE email = %s"
        val = (job_seeker_email, )
        cursor.execute(query, val)
        job_seeker_name = cursor.fetchall()
        session['job_seeker_name'] = job_seeker_name

        query = "SELECT * FROM jobs_info WHERE id = %s"
        val = (id, )
        cursor.execute(query, val)
        data = cursor.fetchall()

        sql = 'insert into job_applications(name,email,role,disc,salary,exp,skill,cname,loc,status,emp_email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (job_seeker_name[0][0],session['job_seeker_email'],data[0][3],data[0][4],data[0][5],data[0][6],data[0][7],data[0][2],data[0][10],'applied',data[0][12])
        cursor.execute(sql,values)
        mydb.commit()

        sql = "select * from job_applications where email='%s'"%(session['job_seeker_email'])
        cursor.execute(sql,mydb)
        data = cursor.fetchall()
        return render_template("job_seeker/applied.html", data=data, message = "Successfully Applied!")

@app.route("/view_applied_jobs")
def view_applied_jobs():
    employee_email = session['employee_email']
    sql = "select * from job_applications where emp_email=%s"
    val = (employee_email, )
    cursor.execute(sql, val)
    data = cursor.fetchall()
    return render_template("employee/view_applied_jobs.html",data=data)

@app.route("/download/<s>")
def download(s=''):
    sql = "select resume from job_seeker where email=%s"
    val = (s,)
    cursor.execute(sql,val)
    resume = cursor.fetchall()[0][0]
    directory = "/Downloads"
    # return send_file(filename_or_fp=resume,as_attachment=True)
    return send_file(resume, as_attachment=True)

@app.route("/send_mail", methods = ["POST"])
def send_mail():
    id = request.form["id"]
    employee_email = session['employee_email']
    sql = "select * from job_applications where id=%s"
    val = (id, )
    cursor.execute(sql, val)
    data = cursor.fetchall()

    sql = "UPDATE job_applications SET status = %s WHERE id = %s"
    val = ("accepted", id)
    cursor.execute(sql, val)
    mydb.commit()

    sql = "select * from employee where email=%s"
    val = (employee_email, )
    cursor.execute(sql, val)
    data2 = cursor.fetchall()


    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sender = data[0][11]
    receiver = data[0][2]
    password = "xbis dzsd uokj ulja"  

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'Selected for Interview!'
    message_body = 'Dear {}; You are selected for Interview in our {}.'.format(data[0][1], data[0][8])
    message.attach(MIMEText(message_body, 'plain'))

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(sender, password)
        smtpObj.send_message(message)
        smtpObj.quit()
        message = "Successfully sent email!"
    except smtplib.SMTPException as e:
        message = f"Unable to send email!: {e}"

    sql = "select * from job_applications where emp_email=%s"
    val = (employee_email, )
    cursor.execute(sql, val)
    data = cursor.fetchall()
    return render_template("employee/view_applied_jobs.html",data=data, message = message)

@app.route("/decline", methods = ["POST"])
def decline():
    id = request.form["id"]
    sql = "DELETE FROM job_applications where id=%s"
    val = (id,)
    cursor.execute(sql,val)
    mydb.commit()
    employee_email = session['employee_email']
    sql = "select * from job_applications where emp_email=%s"
    val = (employee_email, )
    cursor.execute(sql, val)
    data = cursor.fetchall()
    return render_template("employee/view_applied_jobs.html",data=data, message = "Candidate Request Removed!")

    


if __name__ == '__main__':
    app.run(debug=True)
