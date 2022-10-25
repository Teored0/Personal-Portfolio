class User:
    def __init__(self):  # , name, surname, pssw, city, usn, sex
        self.users = []
        self.last_user = None

    def save(self, name, surname, sex, city, usn, pssw):
        self.users.append(
            {"name": name, "surname": surname, "sex": sex, "city": city, "username": usn,
             "password": pssw})
        self.last_user = {"name": name, "surname": surname, "sex": sex, "city": city, "username": usn, "password": pssw}

    def return_dict(self):
        return self.users

    def return_last_user(self):
        return self.last_user

    def signup_control(self, all_user, user, password):
        count_n = 0
        for i in range(len(all_user)):
            if all_user[i]["username"] == user or all_user[i]["password"] == password:
                count_n += 1
        return count_n

    def login_control(self, all_users, user, password):
        check, id_user = False, 0
        for i in range(len(all_users)):
            if all_users[i]["username"] == user and all_users[i]["password"] == password:
                check = True
                id_user = all_users[i]["id"]
        return check, id_user
