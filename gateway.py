from hash_pass import hash_password, check_hash
from mysql.connector import Error
from mysql.connector import connect


def authenticate():
    global cursor
    username = str(input("Enter Username: "))
    cursor.execute(f"select hashcode from info where username='{username}'")
    return check_hash(cursor.fetchone()[0], str(input("Enter PASSWORD: ")))


def recover_password():
    global cursor
    username = str(input("Enter Username: "))
    cursor.execute(f"select sqone, sqtwo, sqthree, hashcode from info where username='{username}'")
    sq = check_hash(cursor.fetchone()[0], str(input("Name of father: ")))
    if sq:
        hashcode = str(hash_password(str(input("Enter New Password: "))))
        password = check_hash(cursor.fetchone()[0], hashcode)
        if password:
            cursor.execute(f"UPDATE info SET hashcode='{hashcode}' WHERE username='{username}'")
            connection.commit()
        else:
            print('Your new password cannot be the same as your old one.')
    else:
        print("You got one or more security questions wrong!")


def delete_user():
    username = str(input("Enter Username: "))
    cursor.execute(f"select hashcode from info where username='{username}'")
    password = check_hash(cursor.fetchone()[0], str(input("Enter PASSWORD: ")))
    if password:
        cursor.execute(f"delete from info where username='{username}'")
        connection.commit()
    else:
        print("You do not have authorization")


def login():
    password = authenticate()
    if password:
        print("Succesfully logged in")
    else:
        print("Not Unsuccessful logged in")


def register():
    global cursor
    username = str(input("Enter Username: "))
    hashcode = str(hash_password(str(input("Enter Password: "))))
    print("Security Questions")
    sq = str(hash_password(str(input("What's your father's name: "))))
    cursor.execute(f"insert into info values ('{username}', '{hashcode}', '{sq}')")
    connection.commit()


if __name__ == '__main__':
    global cursor
    # db_pass = input("For Administrators! (press enter to use default) enter DB password: ")
    connection = connect(
        host='localhost', database='login', user='SuperUser', password="Rocky123")

    try:
        if connection.is_connected():
            cursor = connection.cursor()
        cursor = connection.cursor()
        print("\033[A                                               \033[A")
        print("Connected Succesfully")
        print("""Operations:
                1) Register New User
                2) Login
                3) Delete User
                4) Reset Password
                5) Exit""")
        while True:
            operation = int(input("Enter Operation: "))
            if operation == 1:
                register()
            if operation == 2:
                login()
            if operation == 3:
                delete_user()
            if operation == 4:
                recover_password()
            if operation == 5:
                exit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
