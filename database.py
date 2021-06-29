import mysql.connector as mysql
config = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote'
}
config1 = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote1'
}
config2 = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote2'
}
config3 = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote3'
}
config4 = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote4'
}
config5 = {
    'user': 'root',
    'host': 'localhost',
    'passwd': '********',
    'database': 'evote5'
}


db = mysql.connect(**config)
cursor = db.cursor(dictionary=True, buffered=True)

db1 = mysql.connect(**config1)
cursor1 = db1.cursor(dictionary=True, buffered=True)

db2 = mysql.connect(**config2)
cursor2 = db2.cursor(dictionary=True, buffered=True)

db3 = mysql.connect(**config3)
cursor3 = db3.cursor(dictionary=True, buffered=True)

db4 = mysql.connect(**config4)
cursor4 = db4.cursor(dictionary=True, buffered=True)

db5 = mysql.connect(**config5)
cursor5 = db5.cursor(dictionary=True, buffered=True)
