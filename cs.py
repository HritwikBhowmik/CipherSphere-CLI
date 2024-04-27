import os
import colorama
import sys
import sqlite3
import clipboard

colorama.init()
red = '\033[91m'
orange = '\33[38;5;208m'
green = '\033[92m'
# green = '<ESC>[42m'
cyan = '\033[36m'
bold = '\033[1m'
end = '\033[0m'


def check_database(conn, c):
    if 'data.db' not in os.listdir(os.getcwd()):
        print("{0}[-] Database doesn't exist {1}".format(red, end))
        print("{0}[*] Creating new empty database {1}".format(orange, end))
        table = c.execute("""CREATE TABLE IF NOT EXISTS manager
                (id INTEGER PRIMARY KEY,
                Names TEXT,
                Credentials TEXT,
                Passwords TEXT);""")
        with open('data.db', 'w') as dbfile:
            dbfile.write(str(table))
            dbfile.close()
        print("{0}[+] Database created successfully {1}".format(green, end))
    else:
        print("{0}[+] Database already exist {1}".format(green, end))
    __end()


def __encrypt():
    key = str(input("[*] KEY: "))
    os.chdir(os.getcwd())
    if (len(key) == 8):
        os.system("java -jar secure_CiperSphere-CLI.jar encrypt "+key)
    else:
        print("{0}[-] Key size must be 8 character long {1}".format(red, end))


def __decrypt():
    key = str(input("[*] KEY: "))
    os.chdir(os.getcwd())
    if (len(key) == 8):
        os.system("java -jar secure_CiperSphere-CLI.jar decrypt "+key)
    else:
        print("{0}[-] Key size must be 8 character long {1}".format(red, end))


def insert_data(conn, c):
    if '-n' == sys.argv[2] or '--name' == sys.argv[2] \
            and '-c' == sys.argv[4] or '--credential' == sys.argv[4]\
            and '-p' == sys.argv[6] or '--password' == sys.argv[6]:
        name = sys.argv[3]
        cred = sys.argv[5]
        password = sys.argv[7]
        c.execute('''INSERT INTO manager 
                  (Names, Credentials, Passwords) 
                  VALUES (?, ? ,?)'''
                  , (name, cred, password))
        conn.commit()
    print("{0}[+] Data insertion is successful{1}".format(green, end))
    __end()


def search_data(conn, c):
    if '-n' == sys.argv[2] or '--name' == sys.argv[2]:
        name = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Names=?", [name])
        _lsname = c.fetchall()
        print("id   Name        Credential            Password")
        print("--   ----        ----------            --------")
        for _name in _lsname:
            print("{3}  {0} {2} {1}  {4}   {5}".format(cyan, end, _name[1], _name[0], _name[2], _name[3]))
    elif '-c' == sys.argv[2] or '--credential' == sys.argv[2]:
        cred = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Credentials=?", [cred])
        _lscred = c.fetchall()
        print("id   Name        Credential            Password")
        print("--   ----        ----------            --------")
        for _cred in _lscred:
            print("{3}  {2}  {0} {4} {1}   {5}".format(cyan, end, _cred[1], _cred[0], _cred[2], _cred[3]))
            # id[0] name[1] cred[2] pass[3]
    elif '-p' == sys.argv[2] or '--password' == sys.argv[2]:
        key = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Passwords=?", [key])
        _lskey = c.fetchall()
        print("id   Name        Credential            Password")
        print("--   ----        ----------            --------")
        for _key in _lskey:
            print("{3}  {2}  {4}   {0} {5} {1}".format(cyan, end, _key[1], _key[0], _key[2], _key[3]))
    __end()


def show_database(conn, c):
    if sys.argv[2] == '-n' or sys.argv[2] == '--name':
        name = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Names=?", [name])
        _lsname = c.fetchall()
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        print("| Name     | credentials          || Passwords                                        |")
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        for _name in _lsname:
            print("| {0} | {1}    || {2}                     >>".format(_name[1], _name[2], _name[3]))
            print("+-------------------+-------+-----------+-----------+---------------------------------+")
            # print(_name[:])
    if sys.argv[2] == '-c' or sys.argv[2] == '--credential':
        cred = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Credentials=?", [cred])
        _lscred = c.fetchall()
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        print("| Name     | credentials          || Passwords                                        |")
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        for _cred in _lscred:
            print("| {0} | {1}    || {2}                     >>".format(_cred[1], _cred[2], _cred[3]))
            print("+-------------------+-------+-----------+-----------+---------------------------------+")
            # print(_cred[:])
    if sys.argv[2] == '-p' or sys.argv[2] == '--password':
        key = sys.argv[3]
        c.execute("SELECT * FROM manager WHERE Passwords=?", [key])
        _lskey = c.fetchall()
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        print("| Name     | credentials          || Passwords                                        |")
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        for _key in -_lskey:
            print("| {0} | {1}    || {2}                     >>".format(_key[1], _key[2], _key[3]))
            print("+-------------------+-------+-----------+-----------+---------------------------------+")
    if 'n' in sys.argv[2] and \
            'c' in sys.argv[2] and \
            'p' in sys.argv[2] or \
            'all' in sys.argv[2]:
        c.execute("SELECT * FROM manager")
        _lsall = c.fetchall()
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        print("| Name     | credentials          || Passwords                                        |")
        print("+-------------------+-------+-----------+-----------+---------------------------------+")
        for _all in _lsall:
            print("| {0} | {1}    || {2}                     >>".format(_all[1], _all[2], _all[3]))
            print("+-------------------+-------+-----------+-----------+---------------------------------+")
    __end()


# python3 manager.py update -i 1 -n "u_name" -c "u_cred" -p "u_pass"
#                      1     2 3  4     5     6     7     8     9
def update_data(conn, c):
    if sys.argv[2] == '-i' or sys.argv[2] == '--id':
        id = sys.argv[3]
        u_name = sys.argv[5]
        u_cred = sys.argv[7]
        u_pass = sys.argv[9]
        if '-n' in sys.argv[4] or '--name' in sys.argv[4]:
            c.execute("UPDATE manager SET Names=? WHERE id=?", [u_name, id])
            conn.commit()
        if '-c' in sys.argv[6] or '--credential' in sys.argv[6]:
            c.execute("UPDATE manager SET Credentials=? WHERE id=?", [u_cred, id])
            conn.commit()
        if '-p' in sys.argv[8] or '--password' in sys.argv[8]:
            c.execute("UPDATE manager SET Passwords=? WHERE id=?", [u_pass, id])
            conn.commit()
    print("{0}[+] Data update successfully {1}".format(green, end))
    __end()


def delete_data(conn, c):
    id = sys.argv[3]
    if '-i' in sys.argv[2] or '--id' in sys.argv[2]:
        c.execute("DELETE FROM manager WHERE id=?", [id])
        conn.commit()
    print("{0}[-] Data delete successfully {1}".format(red, end))
    __end()


def start():
    en_filename = '[E]data.db'
    filename = "data.db"
    if filename in os.listdir(os.getcwd()):
        main()
    elif en_filename in os.listdir(os.getcwd()):
        __decrypt()
    else:
        print("{0}[-] No database found{1}".format(red, end))
    

def __end():
    __encrypt()
    sys.exit()
    #en_filename = "[E]data.db"
    #filename = "data.db"
    #if filename in os.listdir(os.getcwd()):
        #__encrypt()
    #elif en_filename in os.listdir(os.getcwd()):
        #sys.exit()


def main():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS manager
                    (id INTEGER PRIMARY KEY,
                    Names TEXT,
                    Credentials TEXT,
                    Passwords TEXT);""")

    if 'check' == sys.argv[1]:
        check_database(conn, c)
    if 'insert' == sys.argv[1]:
        insert_data(conn, c)
    if 'search' == sys.argv[1]:
        search_data(conn, c)
    if 'show' == sys.argv[1]:
        show_database(conn, c)
    if 'update' == sys.argv[1]:
        update_data(conn, c)
    if 'delete' == sys.argv[1]:
        delete_data(conn, c)


if __name__ == '__main__':
    start()
    main()
