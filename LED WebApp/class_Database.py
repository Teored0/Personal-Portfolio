import pymysql

class Database:
    db_con = None

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect_db(self, host, username="", password="", db_name=""):
        try:
            db = pymysql.connect(host=host, user=username, password=password, db=db_name)
            self.cursor = db.cursor(pymysql.cursors.DictCursor)
            print("DB Connected")
            self.conn = db
        except:
            print("CONNECTION ERROR")

    def insert_user(self, user):
        query = "INSERT INTO `users` (`name`, `surname`, `sex`, `city`, `username`, `password`) " \
                "VALUES ( %s, %s, %s, %s, %s, %s)"

        try:
            self.cursor.execute(query, (
                user["name"], user["surname"], user["sex"], user["city"], user["username"], user["password"]))
            self.conn.commit()
        except:
            self.conn.rollback()
            print("Query not Executed")

    def all_users(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def last_activity(self):
        query = "SELECT * FROM activities ORDER BY id DESC"
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return res

    def get_activity_from_user(self, id_user):
        query = "SELECT activities.* FROM user_activity,users,activities WHERE users.id=user_activity.id_user " \
                "AND user_activity.id_activity=activities.id AND user_activity.id_user=%s ORDER BY activities.id DESC"
        self.cursor.execute(query, id_user)
        res = self.cursor.fetchall()
        return res

    def activity(self, type):
        query = "INSERT INTO `activities` (`type`) VALUES (%s)"

        try:
            self.cursor.execute(query, type)
            self.conn.commit()
        except:
            self.conn.rollback()
            print("Query non eseguita")

    def type_activity(self, type, action_type):
        query = "INSERT INTO `activities` (`type`,`type_action`) VALUES (%s,%s)"

        try:
            self.cursor.execute(query, (type, action_type))
            self.conn.commit()
        except:
            self.conn.rollback()
            print("Query not Executed")

    def user_activity(self, id_user):
        query = "INSERT INTO `user_activity`(`id_activity`,`id_user`) VALUES (%s,%s)"
        id_activity = self.last_activity()["id"]
        try:
            self.cursor.execute(query, (id_activity, id_user))
            self.conn.commit()
        except:
            self.conn.rollback()
            print("Query not Executed")

    def all_activities_per_user(self, user, pssw):
        query = "SELECT activities.date_time, activities.type FROM activities,user_activity,users " \
                "WHERE activities.id=user_activity.id_activity AND users.id = user_activity.id_user  " \
                "AND users.username= %s AND users.password= %s AND activities.type != 'Log' " \
                "AND activities.type_action='on';"
        self.cursor.execute(query, (user, pssw))
        res = self.cursor.fetchall()

        return res
