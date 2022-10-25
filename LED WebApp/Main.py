from flask import Flask, request, render_template, session
from class_User import User
from class_Database import Database
from KNN import KNN

app = Flask(__name__)
app.secret_key = "super secret key"

# Main page (Signup / Login)
@app.route("/")
def index():
    return render_template("index.html")

# Registration page
@app.route("/registration")
def registration():
    return render_template("Registration page.html")

# Signup page to retrieve all the information
@app.route("/signup", methods=["post"])
def signup():
    name = request.form.get('name')
    surname = request.form.get('surname')
    password = request.form.get("pssw")
    city = request.form.get('city')
    user = request.form.get('user')
    sex = request.form.get('sex')

    # return all the users in the Database
    r = db.all_users()
    n = user_obj.signup_control(r, user, password)

    if len(r) > 0:
        if n < 1:
            user_obj.save(name=name, surname=surname, sex=sex, city=city, usn=user, pssw=password)
            u = user_obj.return_last_user()
            db.insert_user(u)
            return render_template("succ_reg.html")
        else:
            return render_template("signup failed.html")
    else:
        user_obj.save(name, surname, sex, city, user, password)
        u = user_obj.return_last_user()
        db.insert_user(u)
        return render_template("succ_reg.html")

# Login page
@app.route("/login")
def login():
    return render_template("login.html")

# get the information from Login page
@app.route("/getlogin", methods=["post"])
def getlogin():
    user = request.form.get('user')
    password = request.form.get("pwd")

    buttons = {"red": 0, "yellow": 1, "blue": 2}
    k = 41
    r = db.all_users()
    check, session["id"] = user_obj.login_control(all_users=r, user=user, password=password)
    all_act_u = db.all_activities_per_user(user, password)
    if check:
        db.type_activity("Log", "in")
        db.user_activity(session["id"])
        knn_res = "KNN is not working"

        if len(all_act_u) > k:
            knn = KNN(k)
            x, y = knn.clean(all_act_u)
            knn.fit(x, y)
            y_pred = knn.predict()
            for val in buttons.values():
                if val == y_pred:
                    knn_res = list(buttons.keys())[list(buttons.values()).index(y_pred)]

        return render_template("LED.html", knn=knn_res.upper())

    else:
        return render_template("login failed.html")


# --------------------------- LED ---------------------------

gpio = {'blue': 2, 'yellow': 3, 'red': 4}
actions = []


# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# for n in gpio.values():
#     GPIO.setup(n, GPIO.OUT)


def shutdown_leds(color=0):
    # if color == 0:
    #     for n in gpio.values():
    #         GPIO.output(n, GPIO.LOW)

    # else:
    #     GPIO.output(gpio[color], GPIO.LOW)
    db.type_activity(color, "off")
    db.user_activity(session["id"])


def turnon_leds(color=0):
    # GPIO.output(gpio[color], GPIO.HIGH)
    db.type_activity(color, "on")
    db.user_activity(session["id"])


@app.route("/led_b")
def blue():
    color = "blue"
    if len(actions) == 0:
        turnon_leds(color)
        actions.append(color)


    elif len(actions) >= 1 and actions[len(actions) - 1] == color:
        print(actions)
        shutdown_leds(color)
        actions.pop(-1)
    else:
        shutdown_leds(actions[len(actions) - 1])
        turnon_leds(color)
        actions.append(color)

    return render_template("LED.html")


@app.route("/led_y")
def yellow():
    color = "yellow"
    if len(actions) == 0:
        turnon_leds(color)
        actions.append(color)


    elif len(actions) >= 1 and actions[len(actions) - 1] == color:
        print(actions)

        shutdown_leds(color)
        actions.pop(-1)
    else:
        shutdown_leds(actions[len(actions) - 1])
        turnon_leds(color)
        actions.append(color)

    return render_template("LED.html")


@app.route("/led_r")
def red():
    color = "red"
    if len(actions) == 0:
        turnon_leds(color)
        actions.append(color)

    elif len(actions) >= 1 and actions[len(actions) - 1] == color:
        print(actions)

        shutdown_leds(color)
        actions.pop(-1)
    else:
        shutdown_leds(actions[len(actions) - 1])
        turnon_leds(color)
        actions.append(color)

    return render_template("LED.html")


# --------------------------- FINE ---------------------------

@app.route("/table")
def table():
    return render_template("succ_login.html", result=db.get_activity_from_user(session["id"]))


@app.route('/logout')
def logout():
    db.type_activity("Log", "out")
    db.user_activity(session["id"])
    session.pop("id", None)
    return render_template("index.html")


if __name__ == '__main__':
    user_obj = User()
    db = Database()

    db.connect_db(host="localhost", username="root", password="", db_name="led_activity")
    app.run(debug=True)
