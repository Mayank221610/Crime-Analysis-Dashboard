import sqlite3

def create_conn():
    conn=sqlite3.connect("feedback.db",check_same_thread=False)
    return conn

conn=create_conn()
cursor=conn.cursor()

def fed(data):
    try:
        cursor.execute("INSERT INTO Details(feedback) VALUES(?)",data)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    

# Function to register a new user
# Function to login a user

def reg(data):  # data = (Name, Phone, Email, Password, Why)

    try:
        cursor.execute(
            "INSERT INTO Info (Name, Phone, Email, Password, Why) VALUES (?, ?, ?, ?, ?)",
            data
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error in reg:", e)
        return False


def login(data):
    try:
        cursor.execute("SELECT * FROM Info WHERE Email=? AND Password=?",data)
        if cursor.fetchone():
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
# Function to reset a user's password
def reset_password(email, new_password):
    try:
        cursor.execute("UPDATE Info SET Password=? WHERE Email=?", (new_password, email))
        conn.commit()
        if cursor.rowcount == 0:
            return False  # No user found with the given email
        return True
    except Exception as e:
        print("Error in reset_password:", e)
        return False





