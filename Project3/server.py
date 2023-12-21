#import socket

from socket import *
from random import randint
import math
import pickle

#s = socket.socket()
#print("Socket created")

class Device:
    def __init__(self, key, IP, key_list, latitude, longitude, port):
        self.key = key
        self.IP = IP
        self.key_list = key_list
        self.latitude = latitude
        self.longitude = longitude
        self.port = port

#From 3D5:
def swap(arr, x, y):
    z = arr[x]
    arr[x] = arr[y]
    arr[y] = z

#Fisher-Yates shuffle
def fisher_yates (arr):

    for i in reversed(range(1, len(arr))):
        #Get random value
        x = randint(0,i)
        #Swap (Could also use swap function, but found this apparently works in Python)
        swap(arr, i, x)
    #print(arr)
    return arr

#Checks if a new key is in the list of current keys
def key_check_current (current_keys, new_key):
    #print(len(current_keys))
    for i in range(len(current_keys)):
        print(current_keys[i], new_key)
        if new_key == int(current_keys[i]):
            #print("Got here!")
            return i #return position

    return -1

def check_match (current_keys, key_list):
    matching_keys = []

    #Nested for loop to compare two arrays
    for i in range(len(current_keys)):
        for j in range(len(key_list)):
            if(current_keys[i] == key_list[j]):
                matching_keys.append(i)

    #Returns LOCATION of matching keys
    return matching_keys

def coord_to_distance (coord1, coord2):
    #Get distance
    coord_total = coord2 - coord1

    #convert from coord distance to km
    coord_total = coord_total * 111

    #convert from coord distance to m
    coord_total = coord_total * 1000

    return abs(coord_total)

#8 available keys - easily scalable
start_arr = [1, 2, 3, 4, 5, 6, 7, 8]
#Generate key array by fisher-yates shuffle
key_arr = fisher_yates(start_arr)

#Start at 0
arr_index = 0

#List of keys currently connected to server
#This is redundant and can be covered by the Device class
#Will be phased out
current_keys = []

#Devices that are currently connected
known_devices = []

sent_devices = []

#Create dummy values for testing:
# current_keys.append(2)
# sample_key_list = [1]
# known_devices.append(Device(2, '127.0.0.1', sample_key_list,  53.342892, -6.252682))


server_port = 33500
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('Socket created. Receiving information')
msg = "Data received:"
print(msg)
while True:

    connection_socket, address = server_socket.accept()
    rec2 = connection_socket.recv(1024)
    
    #Take in data as object
    data_package = pickle.loads(rec2)

    #Distribute data
    key_code = data_package[0]
    key_list = data_package[1]
    lat1 = data_package[2]
    long1 = data_package[3]
    port_rec = data_package[4]
    #Remember! IP is in "address"

    #Print, for inspection
    print(key_code, key_list, lat1, long1, port_rec)

        

    #If it doen't have a key code, assign it one
    #This isn't working properly and needs to work on client side
    #However, this should be an easy addition
    if key_code == 0:
        #Send a key code
        connection_socket.send(key_arr[arr_index])
        #Key code is now the key sent
        key_code = key_arr[arr_index]
        #Array index up one, so next key will be the one used
        arr_index = arr_index + 1

    #Check if key is in current keys list
    key_location = key_check_current(current_keys, key_code)

    if key_code in current_keys:
        key_location = key_check_current(current_keys, key_code)
    else:
        key_location = -1

    if key_location == -1:          #If no key found in current devices
        current_keys.append(key_code)               #Add key
        key_location = len(current_keys) - 1        #Location is at end
        known_devices.append(Device(key_code, address[0], key_list, lat1, long1, port_rec))

    #Any matching keys?
    matching_keys = check_match(current_keys, key_list)


    #Checking distance
    for i in range(len(matching_keys)):

        val = matching_keys[i]
        current_lat = float(known_devices[val].latitude)
        current_long = float(known_devices[val].longitude)

        #print(current_lat, lat1, current_long, long1)

        #Get lat and long distance
        lat_distance = coord_to_distance(lat1, current_lat)
        long_distance = coord_to_distance(long1, current_long)

        #Distance formula
        total_distance = math.sqrt(pow(lat_distance, 2) + pow(long_distance, 2))

        print("Distance between 2 devices: ")
        print(total_distance)

        #If equal to or closer than 150m
        if(total_distance < 150):
            sent_devices.append(known_devices[val])

    #Convert to bytes so it can be sent
    mesg = pickle.dumps(sent_devices)
    connection_socket.send(mesg)

    #After sending devices, finish.
    connection_socket.close


#In case it's needed for future use (redundant due to source control, though)


# s.bind(('', port))
# print("socket bound to %s" %(port))

# s.listen(5)
# print("socket is listening")


# while True:

#     c, addr = s.accept()
#     print ('Connection established from', addr)

#     c.send('Hello!'.encode())

#     c.close()

#     break


#connection_socket.send(key_check_code)

        #Get the key_code of the device (0 if it has no code)
        #And the list of keys it can connect to 
        #And location, plus other data (socket)


        # buffer = ''
        # while "\n" not in buffer:
        #     buffer += connection_socket.recv(1)

        # key_code = int(buffer)
        # rec1 = connection_socket.recv(1024)
        
        # key_code = int(rec1.decode('utf-8'))

        
        # buffer = ''
        # while '\n' not in buffer:
        #     buffer += connection_socket.recv(1)
        #     #print(buffer)
            
        # lat1 = float(buffer)
        # buffer = ''
        # while '\n' not in buffer:
        #     buffer += connection_socket.recv(1)
            
        # long1 = float(buffer)
        # buffer = ''
        # while '\n' not in buffer:
        #     buffer += connection_socket.recv(1)
            
        # port_rec = int(buffer)


        # rec3 = connection_socket.recv(9)
        # lat1 = float(rec3.decode('utf-8'))

        # rec4 = connection_socket.recv(9)
        # long1 = float(rec4.decode('utf-8'))

        # rec5 = connection_socket.recv(16)
        # port_rec = int(rec5.decode('utf-8'))

    

    # lat1  = connection_socket.recv(1024).decode()
    # long1 = connection_socket.recv(1024).decode()