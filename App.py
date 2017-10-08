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

@app.route("/showForm")
def showForm():
    return render_template('form.html')

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
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        print(_name,_username,_password)
        # validate the received values
        if _name and _username and _password:
            # All Good, let's call MySQL
            # _hashed_password = generate_password_hash(_password)
            # cursor.callproc('sp_createUser',(_name,_username,_hashed_password))
            cursor.callproc('sp_createUser',(_name,_username,_password))
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
        _username    = request.form['inputUsername']
        _password = request.form['inputPassword']
        _email = request.form['inputEmail']
        _phone = request.form['inputPhone']
        _city = request.form['inputCity']
        _country = request.form['inputCountry']
        _disaster = request.form['inputDisaster']
        _need_relief = request.form['inputNeed_relief']
        _emergency = request.form['inputEmergency']
        _options = request.form['inputOptions']
        _health = request.form['inputHealth']
        _safety = request.form['inputSafety']
        _description = request.form['inputDescription']
        _donate = request.form['inputDonate']

        settingsValid = _email and _phone and _city and _country and _disaster and _need_relief and _emergency

        print(_name,_username,_password,_email,_phone,_city,
            _country,_disaster,_need_relief,_emergency,_health,_safety,
            _description,_donate,_options)
        # validate the received values

        if _name and _username and _password and settingsValid:

            cursor.callproc('sp_editUser',(_name,_username,_password,_email,
                _phone,_city,_country,_disaster,_need_relief,_emergency,
                _health,_safety,_description,_donate,_options))

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

@app.route('/sendRelief',methods=['POST'])
def sendRelief():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _name     = request.form['inputName']
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']
        _email = request.form['inputEmail']
        _phone = request.form['inputPhone']
        _city = request.form['inputCity']
        _country = request.form['inputCountry']
        _disaster    = request.form['inputDisaster']
        _need_relief = request.form['inputNeed_relief']
        _emergency   = request.form['inputEmergency']

        _health      = request.form['inputHealth']
        _safety      = request.form['inputSafety']
        _description = request.form['inputDescription']
        _options     = request.form['inputOptions']

        _donate      = False #request.form['inputDonate']

        settingsValid = _email and _phone and _city and _country

        print(_name,_username,_password,_email,_phone,_city,
            _country,_disaster,_need_relief,_emergency,_health,_safety,
            _description,_donate,_options)

        # validate the received values

        if _name and _username and _password and settingsValid:

            cursor.callproc('sp_editUser',(_name,_username,_password,_email,
                _phone,_city,_country,_disaster,_need_relief,_emergency,
                _options,_health,_safety,_description,_donate))

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

@app.route('/sendNoRelief',methods=['POST'])
def sendNoRelief():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        print('hi')
        _name     = request.form['inputName']
        _username    = request.form['inputUsername']
        _password = request.form['inputPassword']
        _email = request.form['inputEmail']
        _phone = request.form['inputPhone']
        _city = request.form['inputCity']
        _country = request.form['inputCountry']
        _disaster    = request.form['inputDisaster']
        _need_relief = request.form['inputNeed_relief']
        _emergency   = request.form['inputEmergency']

        _health      = False #request.form['inputHealth']
        _safety      = False #request.form['inputSafety']
        _description = False #request.form['inputDescription']
        _options     = False #request.form['inputOptions']

        _donate      = request.form['inputDonate']

        settingsValid = _email and _phone and _city and _country

        print(_name,_username,_password,_email,_phone,_city,
            _country,_disaster,_need_relief,_emergency,_health,_safety,
            _description,_donate,_options)

        # validate the received values

        if _name and _username and _password and settingsValid:

            cursor.callproc('sp_editUser',(_name,_username,_password,_email,
                _phone,_city,_country,_disaster,_need_relief,_emergency,
                _options,_health,_safety,_description,_donate))

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
#                 <input type='text' name='username' id='username' placeholder='username'></input>
#                 <input type='password' name='pw' id='pw' placeholder='password'></input>
#                 <input type='submit' name='submit'></input>
#                </form>
#                '''
#
#     username = flask.request.form['username']
#     if flask.request.form['pw'] == all_users[username]['pw']:
#         user = User()
#         user.id = username
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
