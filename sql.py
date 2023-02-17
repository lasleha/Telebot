import pyodbc
import threading

server = 'SQL8004.site4now.net'
database = 'db_a93836_invest'
username = 'db_a93836_invest_admin'
password = 'elmelm327327'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)


def CheckUsr(user_id):
    cursor = cnxn.cursor()
    cursor.execute('select PhoneNumber from dbo.AspNetUsers')
    users = []
    for row in cursor.fetchall():
        users.append(row)
    if user_id in users:
        return True
    else:
        return False


def Favorit(user_id):
    cursor = cnxn.cursor()
    cursor.execute('select * from dbo.Favorites')
    states_id = []
    for row in cursor.fetchall():
        if row[0] == str(user_id) and row[2] == 1:
            states_id.append(row[1])
    cursor = cnxn.cursor()
    cursor.execute('select * from dbo.RealEstates')
    info = [
        {
        }
    ]
    for row in cursor.fetchall():
        if row[0] in states_id:
            l = {
                'address': row[1],
                'pr2m': row[4],
                'area': row[5],
                'stage': row[3],
                'perspective': row[12],
                'risk': '',
                'usage': row[6],
                'are_ready': row[8],
                'number': row[2],
                'type': row[7],
                'price': float(row[4])*float(row[5])
            }
            info.append(l)
    cursor.execute('select * from dbo.Favorites')
    return info


def Check():
    #threading.Timer(1800.0, Check)
    cursor = cnxn.cursor()
    cursor.execute('select StateId, IsChanged from dbo.Favorites')
    lib = []
    for row in cursor.fetchall():
        if row[1]:
            lib.append(row[0])
    return lib










#5708104256
#6131879353:AAGKP8nmK-6kksTxJWtymxCBgIWCIihOchs