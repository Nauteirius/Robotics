import os
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.20.10.1",9999))
print("polaczono")

file = open("image.png", "rb")
file_size = os.path.getsize("image.png")

client.send("received_image.png".encode())
client.send(str(file_size).encode())
data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()



# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("localhost",9999))
# server.listen()
#
# client,addr = server.accept()
#
# file_name = client.recv(1024).decode()
# print(file_name)
# file_size=client.recv(1024).decode()
# print(file_size)
# file.open(file_name,"wb")
# file_bytes=b""
# done=False
# while not done:
#     data = client.recv(1024)
#     if file_bytes[-5:] == b"<END>":
#         done = True
#     else:
#         file_bytes+= data

# file.write(file_bytes)
# file.close()
# client.close()
# server.close()


