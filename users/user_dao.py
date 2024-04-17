import database
from users.user import User

#from user import User



class UserDao:
    connexion = database.connect_db()
    cursor = connexion.cursor()


    @classmethod
    def create(cls,user: User):
        sql = "INSERT INTO user (nom_complet,username,password, is_admin) VALUES (%s,%s,%s,%s)"
        params = (user.nom_complet,user.username,user.password, user.is_admin)
        try:
            UserDao.cursor.execute(sql, params)
            UserDao.connexion.commit()
            message = 'success'        
        except Exception as error:
            message = 'failure'
        return message

    @classmethod
    def list_all(cls):
        sql = "SELECT * FROM user"
        try:
            UserDao.cursor.execute(sql)
            users = UserDao.cursor.fetchall()
            message = 'success'
        except Exception as error:
            users = []
            message = 'error'
        return (message, users)
    
    @classmethod
    def get_one(cls,username):
        sql = "SELECT * FROM user WHERE username = %s"
        try:
            UserDao.cursor.execute(sql,(username,))
            user = UserDao.cursor.fetchone()
            message = 'success'
        except Exception as error:
            message = 'failure'
            user =()
            message= user
        return (message, user)
    
    @classmethod
    def get_user_role(cls,username):
        sql = "SELECT is_admin FROM user WHERE username = %s"
        try:
            UserDao.cursor.execute(sql, (username,))
            user = UserDao.cursor.fetchone()
            message= 'success'
            if user:
                is_admin = user[0]
                if is_admin==1:
                    message = ("The user is an administrator")             
            else:
                message =("The user is not an administrator")        
        except Exception as error:
            message =("Error retrieving user role")
        return (message, user)
       

        
    