import pyodbc
import PIL.Image as Image
import io

server = 'SQL8004.site4now.net'
database = 'db_a93836_invest'
username = 'db_a93836_invest_admin'
password = 'elmelm327327'
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';ENCRYPT=yes;UID=' + username + ';PWD=' + password)


def img(path):
    io_bytes = io.BytesIO(path)
    i = Image.open(io_bytes)
    return i


def check_usr(user_id):
    user_id = str(user_id)
    cursor = cnxn.cursor()
    cursor.execute('select UserName, PhoneNumber from dbo.AspNetUsers')
    for row in cursor.fetchall():
        if row[1] == user_id:
            return row[0]
    return None


def favorite(user_name, push):
    cursor = cnxn.cursor()
    cursor.execute('select StateId, UserName, IsChanged from dbo.Favorites')
    states_id = []
    for row in cursor.fetchall():
        if (user_name == row[1]) and (not push or row[2]):
            states_id.append(row[0])
    print(states_id)
    cursor = cnxn.cursor()
    cursor.execute('select * from dbo.RealEstates')
    info = dict(dict())
    for row in cursor.fetchall():
        print(row)
        if row[0] in states_id:
            l = {
                'address': row[1],
                'area': row[5],
                'stage': row[3],
                'perspective': row[12],
                'risk': '',
                'usage': row[6],
                'are_ready': row[8],
                'number': row[2],
                'type': row[7],
                'price': float(row[4]) * float(row[5]),
                'is_repaired': row[14]
            }
            info[row[0]] = l

    cursor.execute('select _Image, StateId from dbo.Images')
    a = []
    for row in cursor.fetchall():
        if row[1] not in a:
            a.append(row[1])
            if row[1] in info:
                info[row[1]]['image'] = img(row[0])

    return list(info.values())


def check():
    cursor = cnxn.cursor()
    cursor.execute('select UserName, PhoneNumber from dbo.AspNetUsers')
    users = dict()
    for row in cursor.fetchall():
        users[row[0]] = row[1]
    lib = dict()
    for k, v in users.items():
        lib[v] = favorite(k, True)
    cursor.execute(f'update dbo.Favorites set IsChanged = 0')
    cnxn.commit()
    return lib
