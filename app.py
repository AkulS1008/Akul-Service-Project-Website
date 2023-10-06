from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
import random
from datetime import date

app = Flask(__name__)
app.secret_key = 'Sample'
Bootstrap(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'serviceproject108@gmail.com'
app.config['MAIL_PASSWORD'] = 'learningpythonfornow123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

eng = create_engine("mysql+mysqldb://AkulServiceS:ilikemssql123@AkulServiceS.mysql.pythonanywhere-services.com/AkulServiceS$ServiceProjectDemo", pool_recycle = 280)
conn = eng.connect()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/activation", methods = ["POST", "GET"])
def activate():
    if request.method == "GET":
      return render_template('activation.html')

    if request.method == "POST":
      form_data = request.form
      result = eng.execute("SELECT * FROM Membership WHERE EmailID =  '" + form_data.get('inputEmail') + "';")
      res = result.fetchone()
      try:
        if (sha256_crypt.verify(form_data.get('activation_code'), res[7])):
          eng.execute("UPDATE Membership SET activation = 'y' WHERE EmailID =  '" + form_data.get('inputEmail') + "';")
          session['email'] = form_data.get('inputEmail')
          session['name'] = res[3]
          return render_template('home.html')
        else:
          return render_template('activation.html', error_message = "Invalid Username or Activation code. Please try again. Otherwise create new account")
      except:
        return render_template('Membership.html', message = str(sha256_crypt.verify(res[7], form_data.get('activation_code'))))

@app.route("/home")
def home1():
    return render_template('home.html')

@app.route("/membership", methods = ["POST", "GET"])
def connect_membership():
    if request.method == "GET":
      return render_template('Membership.html')

    if request.method == "POST":
      form_data = request.form
      try:
        msg1 = ""
        try:
          aresult = eng.execute("SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail') + "';")
          res1 = aresult.fetchone()
          if res1[0] == form_data.get('inputEmail'):
            return render_template('Membership.html', message = "Member already exists")
        except:
          encrypt = sha256_crypt.encrypt(form_data.get('inputPassword'))
          activ = pwd_generator()
          encrypt_temp = sha256_crypt.encrypt(activ)
          cmd = "INSERT INTO Membership Values('" + form_data.get('inputEmail') + "', '" + encrypt + "', '" + form_data.get('DOB') + "', '" + form_data.get('Username') + "', '" + form_data.get('gender') + "', 0, 'y', '" + encrypt_temp + "');"
          eng.execute(cmd)
          #msg = Message('Hello', sender = 'serviceproject108@gmail.com', recipients = [form_data.get('inputEmail')])
          #msg.body = "Hello " + form_data.get('Username') + ",\n Thank you for becoming a member!\n Please activate your account by clicking n the link below:\n" + "http://akulservices.pythonanywhere.com/activation" + "\nYor activation code is " + activ
          #mail.send(msg)
          return render_template('Membership.html', good_message = "You're In!")
      except:
        return render_template('Membership.html', message = "Unable to create member.")

@app.route("/about")
def connect_about():
    return render_template('AboutUs.html')

@app.route("/logout")
def connect_logout():
    if 'email' in session:
        session.pop('email', None)
    if 'name' in session:
        session.pop('name', None)
    return render_template('logout.html')

@app.route("/detail")
def connect_detail():
    return render_template('detail.html')

@app.route("/testCaptcha")
def connect_captcha():
    return render_template('testCaptcha.html')

@app.route("/forgot_password", methods = ["POST", "GET"])
def connect_forgot_password():
    if request.method == "GET":
      return render_template('forgot_password.html')

    if request.method == "POST":
      form_data = request.form
      result = eng.execute("SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail') + "';")
      res = result.fetchone()
      try:
        if res[6] == "y":
          temp_pwd = pwd_generator()
          eng.execute("UPDATE Membership SET Password = '" + temp_pwd + "' , tempPWD = 'y', login_try = 0 WHERE EmailID = '" + form_data.get('inputEmail') + "';")
          msg = Message('Hello', sender = 'serviceproject108@gmail.com', recipients = [form_data.get('inputEmail')])
          msg.body = "Based on the information you have provided, you have recieved a temporary password \n" + temp_pwd + " \nYou can later change your password by logging in using your temporary password."
          mail.send(msg)
          return render_template('forgot_password.html', ok_message = "You will recieve an email shortly to the email address you have provided. You can later change your temporary password if you log in again.")
        else:
          return render_template('activation.html', error_message = "Please activate your account")
      except:
        return render_template('forgot_password.html', error_message = "An error occured in processing your request. Please try again.")

def pwd_generator():
    small_char = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    large_char = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    num_char = ["0","1","2","3","4","5","6","7","8","9"]
    special_char = ["/","@","$","#","%","&","*","|"]
    pwd = ""
    for i in range(3):
        pwd += random.choice(small_char)
    for j in range(3):
        pwd += random.choice(large_char)
    for j in range(1):
        pwd += random.choice(special_char)
    for j in range(3):
        pwd += random.choice(num_char)
    return pwd

@app.route("/mail")
def connect_mail():
   msg = Message('Hello', sender = 'serviceproject108@gmail.com', recipients = ['akulsingh0708@gmail.com'])
   msg.body = "This is to verify that you have recieved an email."
   mail.send(msg)
   return "Sent"

@app.route("/contact")
def connect_contact():
    return render_template('contactus.html')

@app.route("/help")
def connect_help():
    return render_template('help.html')

@app.route("/settings")
def connect_settings():
    return render_template('settings.html')

@app.route("/test")
def connect_test1():
    return render_template('test.html')

@app.route("/login", methods = ["POST", "GET"])
def connect_log_in():
    if request.method == "GET":
      return render_template('login.html')

    if request.method == "POST":
      form_data = request.form
      msg1 = ""
      try:
        msg1 = "MIKA"
        result = eng.execute("SELECT * FROM Membership WHERE EmailID =  '" + form_data.get('inputEmail') + "';")
        res = result.fetchone()
        if res[6] == "y":
          if res[5] >= 5:
            return render_template('login.html', message = "Your account is locked. Please reset your password.")
          if (sha256_crypt.verify(form_data.get('inputPassword'), res[1])):
            msg1 = "UPDATE Membership SET login_try = 0 WHERE EmailID =  '" + form_data.get('inputEmail') + "';"
            eng.execute(msg1)
            session['email'] = form_data.get('inputEmail')
            session['name'] = res[3]
            return render_template('home.html')
          else:
            msg1 = "UPDATE Membership SET login_try = login_try + 1 WHERE EmailID =  '" + form_data.get('inputEmail') + "';"
            eng.execute(msg1)
            return render_template('login.html', message = "Invalid Username or Password. Please try again.")
        else:
          return render_template('activation.html', error_message = "Please activate your account")
      except:
        return render_template('login.html', message = "This user does not exist. Become a member." + msg1)

@app.route("/reset_pwd", methods = ["POST", "GET"])
def connect_reset_pwd():
    if request.method == "GET":
      return render_template('reset_pwd.html')

    if request.method == "POST":
      form_data = request.form
      result = eng.execute("SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail') + "';")
      res = result.fetchone()
      if res[1] == form_data.get('inputPasswordTemp'):
        try:
          encrypt = sha256_crypt.encrypt(form_data.get('inputPasswordNew'))
          eng.execute("UPDATE Membership SET Password = '" + encrypt + "' , tempPWD = 'n', login_try = 0 WHERE EmailID = '" + form_data.get('inputEmail') + "';")
          session['email'] = form_data.get('inputEmail')
          session['name'] = res[3]
          return render_template('home.html')
        except:
          return render_template('reset_pwd.html', error_message = "An error occured in processing your request. Please try again.")
      else:
          return render_template('reset_pwd.html', error_message = "Invalid Username or Password. Please try again.")

@app.route("/participants")
def connect_participate():
    email = ""
    if 'name' in session and 'email' in session:
      name = session['name']
      email = session['email']
      try:
        result = eng.execute("select * from Meeting_Schedule where EmailID = '" + email + "';")
        return render_template('participate.html', res = result.fetchall(), name = name)
      except:
         return render_template('participate.html', message = "Error")
    else:
        return render_template('login.html')

@app.route("/foodservice", methods = ["POST", "GET"])
def connect_food():
    try:
     if request.method == "GET":
        return render_template('foodservice.html')

     if request.method == "POST":
        form_data = request.form
        cmd = "SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail1') + "';"
        result = eng.execute(cmd)
        res = result.fetchone()
        if res and (sha256_crypt.verify(form_data.get('inputPassword1'), res[1])):
            mydate = str(date.today())
            cmd2 = ""
            try:
                cmd2 = "Insert into Meeting_Schedule values('" + mydate + "', '3:00 - 4:00 PM P.S.T', 'Food Distribution', 'https://meet.google.com/nwm-igvp-ncd', '" + form_data.get('inputEmail1') + "');"
                eng.execute(cmd2)
                return redirect('/membermeetings')
            except Exception as e:
                return render_template('foodservice.html', message = "Your meeting schedule is updated")
        else:
            return render_template('foodservice.html', message = "User not a member. Please sign up.")
    except:
        return render_template('foodservice.html', message = "User not a member. Please sign up.")

@app.route("/medicalservice", methods = ["POST", "GET"])
def connect_medical():
    try:
     if request.method == "GET":
        return render_template('medicalservice.html')

     if request.method == "POST":
        form_data = request.form
        cmd = "SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail1') + "';"
        result = eng.execute(cmd)
        res = result.fetchone()
        if res and (sha256_crypt.verify(form_data.get('inputPassword1'), res[1])):
            mydate = str(date.today())
            cmd2 = ""
            try:
                cmd2 = "Insert into Meeting_Schedule values('" + mydate + "', '4:00 - 5:00 PM P.S.T', 'Medical Services', 'https://meet.google.com/nwm-igvp-ncd', '" + form_data.get('inputEmail1') + "');"
                eng.execute(cmd2)
                return redirect('/membermeetings')
            except Exception as e:
                return render_template('medicalservice.html', message = "Your meeting schedule is updated")
        else:
            return render_template('medicalservice.html', message = "User not a member. Please sign up.")
    except:
        return render_template('medicalservice.html', message = "User not a member. Please sign up.")

@app.route("/cleanservice", methods = ["POST", "GET"])
def connect_clean():
    try:
     if request.method == "GET":
        return render_template('cleanservice.html')

     if request.method == "POST":
        form_data = request.form
        cmd = "SELECT * FROM Membership WHERE EmailID = '" + form_data.get('inputEmail1') + "';"
        result = eng.execute(cmd)
        res = result.fetchone()
        if res and (sha256_crypt.verify(form_data.get('inputPassword1'), res[1])):
            mydate = str(date.today())
            cmd2 = ""
            try:
                cmd2 = "Insert into Meeting_Schedule values('" + mydate + "', '5:00 - 6:00 PM P.S.T', 'Sanitory and Clean Services', 'https://meet.google.com/nwm-igvp-ncd', '" + form_data.get('inputEmail1') + "');"
                eng.execute(cmd2)
                return redirect('/membermeetings')
            except Exception as e:
                return render_template('cleanservice.html', message = "Your meeting schedule is updated")
        else:
            return render_template('cleanservice.html', message = "User not a member. Please sign up.")
    except:
        return render_template('cleanservice.html', message = "User not a member. Please sign up.")

@app.route("/membermeetings")
def connect_membermeeting():
    email = ""
    if 'name' in session and 'email' in session:
      name = session['name']
      email = session['email']
      try:
        result = eng.execute("select * from Meeting_Schedule where EmailID = '" + email + "';")
        return render_template('member_meeting.html', res = result.fetchall(), name = name)
      except:
         return render_template('member_meeting.html', message = "Error")
    else:
        return render_template('login.html')

@app.route("/onsite")
def connect_onsite():
    return render_template('onsite.html')

@app.route("/response")
def connect_response():
    return render_template('response.html')

@app.route("/event")
def connect_event():
    emailID = ""
    if 'name' in session and 'email' in session:
      name = session['name']
      emailID = session['email']
      result = eng.execute("select meetingDate, meetingtime, agenda, details from Meeting_Schedule order by meetingDate;")
      return render_template('event.html', res = result.fetchall(), name = name)
    else:
        return render_template('login.html')
