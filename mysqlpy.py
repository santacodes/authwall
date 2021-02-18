import mysql
from mysql.connector import Error


def check():
    """Authenticate Password"""
    username = str(input("Enter Username: "))
    password = str(input("Enter PASSWORD: "))
    cursor.execute(f"select Password from info where Username='{username}'")

    record = cursor.fetchone()
    print(record[0])
    if password == record[0]:
        print('Successfully Logged In!!')
        return
    else:
        print('Please try again..')


if __name__ == '__main__':
    db_pass = input("For Administrators! (press enter to use defauly) enter DB password: ")
    db_pass = db_pass if db_pass is not None else "password"
    connection = mysql.connector.connect(
        host='localhost', database='login', user='root', password=db_pass)
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            print("You are connected to database")
            check()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
