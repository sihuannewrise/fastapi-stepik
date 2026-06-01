import socket


my_socket = socket.socket()

print(my_socket.fileno())

with open("text.txt", "w") as file:  # создаем объект файла
    print(file.fileno())         # и печатаем его дескриптор
