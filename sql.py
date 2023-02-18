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
    cursor.execute('select PhoneNumber from dbo.AspNetUsers')
    users = []
    for row in cursor.fetchall():
        users.append(row[0])
    if user_id in users:
        return True
    else:
        return False


def favorite(user_id):
    cursor = cnxn.cursor()
    cursor.execute('select Id, PhoneNumber from dbo.AspNetUsers')
    for row in cursor.fetchall():
        if row[1] == str(user_id):
            user_id = row[0]
    cursor = cnxn.cursor()
    cursor.execute('select * from dbo.Favorites')
    states_id = []
    for row in cursor.fetchall():
        if row[0].lower() == user_id:
            states_id.append(row[1].lower())
    cursor = cnxn.cursor()
    cursor.execute('select * from dbo.RealEstates')
    info = dict(dict())
    for row in cursor.fetchall():
        if row[0].lower() in states_id:
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
                'price': float(row[4]) * float(row[5]),
                'is_repaired': row[14]
            }
            info[row[0].lower()] = l
    cursor.execute('select _Image, StateId from dbo.Images')
    a = []
    for row in cursor.fetchall():
        if row[1] not in a:
            a.append(row[1])
            if row[1].lower() in info.keys():
                l = info[row[1].lower()]
                l['image'] = img(row[0])
                info[row[1].lower()] = l
    return info


def check():
    cursor = cnxn.cursor()
    cursor.execute('select UserId, StateId, IsChanged from dbo.Favorites')
    lib = dict([])
    for row in cursor.fetchall():
        if row[2]:
            if row[0] in lib.keys():
                l = lib[row[0]]
                l.append(row[1])
                lib[row[0]] = l
            else:
                l = []
                l.append(row[1])
                lib[row[0]] = l
    cursor.execute(f'update dbo.Favorites set IsChange = 0')
    cnxn.commit()
    return lib
