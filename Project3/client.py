from socket import *
import pickle
import threading
import sys
import time

#smp library for emails

#Note: 0.00001 lat/long = 1.11 m. People move about 1.42 m/sec

longitude = -6.252668
latitude = 53.342973

key_code = 1                    #Key for this device
key_list = [2]                  #Known devices
client_port = 33600             #This is used to connect to this client
server_port = 33500
server_IP = '10.35.70.33'
device_IP = '10.35.70.14'
SOS = False
SOS_message = "Nothing"

#Data for other peers
detail1 = [latitude, longitude]

#Data for server
server_package = [key_code, key_list, latitude, longitude, client_port]

#Data for Peers
peer_package = [latitude, longitude, SOS, SOS_message]

class Device:
    def __init__(self, key, IP, key_list, latitude, longitude, port):
        self.key = key
        self.IP = IP
        self.key_list = key_list
        self.latitude = latitude
        self.longitude = longitude
        self,port = port

def handle_connection(port, peer_package):

    latitude = peer_package[0]
    longitude = peer_package[1]
    SOS = peer_package[2]
    SOS_message = peer_package[3]
    

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    
    print("Waiting for connections...")

    connection, address = server_socket.accept()
    print("Connected to peer! Data received:")

    timecounter2 = 0

    while True:
        
        if timecounter2 == 40:
            SOS = True
            SOS_message = "Panic Attack!"

        peer_package = [latitude, longitude, SOS, SOS_message]

        rec = connection.recv(1024)
        if len(rec) > 0:
            data = pickle.loads(rec)

            if data[2] == True:
                print("SOS!!! Message:")
                print(data[3])
                print("Location:")
                print (data[0], data[1])
        try:
            connection.send(pickle.dumps(peer_package))
        except:
            print("Connection closed unexpectedly!")
            break
        
        #print(data[0], data[1], data[2], timecounter2)
        time.sleep(1)
        timecounter2 = timecounter2 + 1

print("Starting Device. \n")

val = 0

while val == 0:
    inp = input("Please enter a new key, or else input -1: ")

    try:
        val = int(inp)
        if val % 1 != 0:
            val = 0
            raise TypeError("Not an integer")
            
        elif val < -1:
            val = 0
            raise TypeError("Not a valid number, below -1")
            
    except ValueError:
        print("Invalid input, not an int")
    except TypeError as ve:
        print(ve)

    if val == -1:
        break

    elif val != 0:
        if val in key_list:
            print("Repeated Value")
        else:
            key_list.append(val)
        val = 0

print("List of known keys:")
print(key_list)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_IP, server_port))

client_socket.send(pickle.dumps(server_package))

msg = client_socket.recv(1024)

devices = pickle.loads(msg)
n_devices = len(devices)

if n_devices > 0:
    print('Devices received from server')
    print('Key \t latitude \t longitude \t port \t IP')
#Devices found?
for i in range(n_devices):
    print(devices[i].key, "\t", devices[i].latitude, "\t", devices[i].longitude, "\t", devices[i].port, "\t", devices[i].IP)

client_socket.close()

#Wait for connections:
thread1 = threading.Thread(target=handle_connection, args=[client_port, peer_package])
thread1.daemon = True #So that it ends instead of having to manually kill the thread
thread1.start()

#Here, go into async for each connected device?

#If device found, connect to it
if n_devices > 0:
    if (devices[0].IP != device_IP) and (devices[0].port != client_port):
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((devices[0].IP, devices[0].port))
        except:
            print("Failed to connect, details:")
            print(devices[0].IP)
        timecounter = 0

        print("Connected to peer! Data received: ")
        while True:
            
            if timecounter == 30:
                SOS = True
                SOS_message = "Being Harassed!"
            
            peer_package = [latitude, longitude, SOS, SOS_message]
            try:
                client_socket.send(pickle.dumps(peer_package))
            except:
                print("Connection closed by other end")
                break

            rec = client_socket.recv(1024)
            if len(rec) > 0:
                data = pickle.loads(rec)
            if data[2] == True:
                print("SOS!!! Message:")
                print(data[3])
                print("Location:")
                print (data[0], data[1])
        
            #print(data[0], data[1], data[2], timecounter)
            time.sleep(1)
            timecounter = timecounter + 1

time.sleep(60)

#s.connect(('127.0.0.1', receiving_port))

#key = s.recv(1024)

#print(key.decode())

#s.close