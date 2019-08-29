import mysql.connector as db


def getuser(userid :int):
    records = "ERROR"
    try:
        connection = db.connect(host='localhost',
                                database='REDACTED',
                                user='REDACTED', # change me
                                password='REDACTED') # change me
        cursor = connection.cursor(prepared=True) #this will return MySQLCursorPrepared object
        cursor.execute("""select balance from a_coinbot WHERE discordid = %s""", (str(userid),))
        data = cursor.fetchone()
        if data is not None:
            records = data[0]
    except db.Error as error:
        print("parameterized query failed {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return records

def changebal(userid :int, coin :int):
    balance = getuser(userid)
    if balance == "ERROR":
        balance = 0
    if updateuser(userid, balance + coin):
        return True
    else:
        return False
def updateuser(userid :int, coin :int):
    try:
        connection = db.connect(host='localhost',
                                database='REDACTED', # to be changed
                                user='REDACTED', # change me
                                password='REDACTED') # change me
        cursor = connection.cursor(prepared=True) #this will return MySQLCursorPrepared object
        existing = getuser(userid)
        print(existing)
        print(userid , coin)
        #check if we need to make new user
        if existing == "ERROR":
            cursor.execute("""
            INSERT INTO a_coinbot (discordid, balance) VALUES (%s, %s)
            """, (str(userid), coin))
            connection.commit()
        else:
            val = (coin, userid)
            cursor.execute("UPDATE a_coinbot SET `balance` = %s WHERE `discordid` = %s", val)
#            print(cursor._last_executed)
            connection.commit()

    except db.Error as error:
        print("parameterized query failed {}".format(error))
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return True
