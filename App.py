from flask import Flask, render_template, json, request, flash, redirect, url_for
import flask_login
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'some_secret'

mysql = MySQL()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# MySQL configurations
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/form")
def showFormx():
    return render_template('formsample.html')

@app.route('/showSettings')
def showSettings():
    return render_template('settings.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showHome')
def showHome():
    return render_template('index.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/signIn',methods=['POST'])
def signIn():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputName']
        _password = request.form['inputPassword']

        cursor.execute("SELECT * FROM tbl_user")
        all_users = [list(i) for i in cursor.fetchall()]
        # print(all_users)
        # user = all_users
        user = []
        for lst in all_users:
            if _name == lst[2]:
                user = lst

        if (user == []):
            print("User not found!")
            return json.dumps({'message':'User not found!'})
        if (user[3]!= _password):
            print("Incorrect Password!")
            return json.dumps({'message':'Incorrect Password!'})

        print("Welcome",user[1])

        return json.dumps({'message':'Data retrieved!'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/signUp',methods=['POST'])
def signUp():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        print(_name,_email,_password)
        # validate the received values
        if _name and _email and _password:
            # All Good, let's call MySQL
            # _hashed_password = generate_password_hash(_password)
            # cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                print('User created successfully!')
                # flash('User created')
                # return render_template('signup.html')
                # return redirect(url_for('index'))
                return showHome()
                # return json.dumps({'message':'User created successfully!'})
            else:
                print('Username Exists!')
                # flash('User exists')
                # return render_template('signup.html')
                return json.dumps({'error':str(data[0])})
        else:
            print('Enter the required fields')
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/sendForm',methods=['POST'])
def sendForm():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name     = request.form['inputName']
        _email    = request.form['inputEmail']
        _password = request.form['inputPassword']
        _setting1 = request.form['inputSetting1']
        _setting2 = request.form['inputSetting2']
        _setting3 = request.form['inputSetting3']
        _setting4 = request.form['inputSetting4']
        _setting5 = request.form['inputSetting5']
        settingsValid = _setting1 and _setting2 and _setting3 and _setting4 and _setting5

        print(_name,_email,_password,_setting1,_setting2,_setting3,_setting4,_setting5)
        # validate the received values
        if _name and _email and _password and settingsValid:
            # All Good, let's call MySQL
            # _hashed_password = generate_password_hash(_password)
            # cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            # cursor.execute("SELECT * FROM tbl_user")
            # all_users = [list(i) for i in cursor.fetchall()]
            # user = []
            # for lst in all_users:
            #     if _name == lst[2]:
            #         user = lst
            # if (user == []):
            #     print("User not found!")
            #     return json.dumps({'message':'User not found!'})
            # if (user[3]!= _password):
            #     print("Incorrect Password!")
            #     return json.dumps({'message':'Incorrect Password!'})

            cursor.callproc('sp_editUser',(_name,_email,_password,
                _setting1,_setting2,_setting3,_setting4,_setting5))

            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                print('User Profile updated successfully!')
                return showHome()
            else:
                print('User does not exist!')
                return json.dumps({'error':str(data[0])})
        else:
            print('Enter the required fields')
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

# # all_users =
# class User(flask_login.UserMixin):
#     pass
#
# @login_manager.user_loader
# def user_loader(username):
#     if username not in all_users:
#         return
#     user = User()
#     user.id = username
#     return user
#
# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get('username')
#     if username not in all_users:
#         return
#
#     user = User()
#     user.id = username
#     user.is_authenticated = request.form['pw'] == all_users[username]['pw']
#
#     return user
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if flask.request.method == 'GET':
#         return '''
#                <form action='login' method='POST'>
#                 <input type='text' name='email' id='email' placeholder='email'></input>
#                 <input type='password' name='pw' id='pw' placeholder='password'></input>
#                 <input type='submit' name='submit'></input>
#                </form>
#                '''
#
#     email = flask.request.form['email']
#     if flask.request.form['pw'] == all_users[email]['pw']:
#         user = User()
#         user.id = email
#         flask_login.login_user(user)
#         return flask.redirect(flask.url_for('protected'))
#
#     return 'Bad login'
#
# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return 'Logged out'
#
# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     return 'Logged in as: ' + flask_login.current_user.id
#
# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

if __name__ == "__main__":
    app.run()
