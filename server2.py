# Muzaffer Gur Ersalan, 014841873
import threading
import socket
import logging
import numpy as np


err_rates = list(np.arange(0.0, 1.0, 0.05))
#err_rates = [0.0]

my_ip = socket.gethostname()

#big_String = 'Second point. Due to the way chunks are sliced up we know that all slices except the last one must be SliceSize (1024 bytes). We take advantage of this to save a small bit of bandwidth sending the slice size only in the last slice, but there is a trade-off: the receiver doesnt know the exact size of a chunk until it receives the last slice. I would like to add more lines to this data set I am trying to acoomplish'
#big_String = 'Second point. Due to the way chunks are sliced up we know that all slices except the last one must be SliceSize (1024 bytes). We take advantage of this to save a small bit of bandwidth sending the slice size only in the last slice, but there is a trade-off: the receiver doesnt know the exact size of a chunk until it receives the last slice. I would like to add more lines to this data set I am trying to acoomplish now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package '

with open('article2.txt') as f:
    big_String = f.read()



#loss_rate = float(input('Enter loos rate as float number'))

def Create_UDP_Packages(data,chunk_size,seq_num):
    ##divide payload and add id to it
    
    packages = []
    
    encoded = data.encode('utf-8')
    loop_len = int(len(encoded) / chunk_size)
    loop_len += 1
    last_id = loop_len

    payload_dict = {}
    for i in range(0,loop_len):
        payload_dict[ "p" + str( i+1 ) ] = encoded[100*i:100*(i+1)]

    # create packages
    for key, value in payload_dict.items():
        if seq_num < 10:
            if int(key[1:]) < 10:
                if last_id < 10:
                    packages.append(('0' + str(seq_num)+ '|' + '0' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
                else:
                    packages.append(('0' + str(seq_num)+ '|' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
            else:
                if last_id < 10:
                    packages.append(('0' + str(seq_num)+'|' + '0' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
                else:
                    packages.append(('0' + str(seq_num)+'|' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
        else:   
            if int(key[1:]) < 10:
                if last_id < 10:
                    packages.append((str(seq_num)+'|' + '0' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
                else:
                    packages.append((str(seq_num)+'|' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
            else:
                if last_id < 10:
                    packages.append((str(seq_num)+'|' + '0' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))
                else:
                    packages.append((str(seq_num)+'|' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode('utf-8'))

    ## add reduncany packages 
    red_packages = []
    cnt = 1
    
    for i in range (0,len(packages),2):
    
        if i == len(packages) - 1:
            break
        #print (i)
        payload1 = packages[i][9:]
        payload2 = packages[i+1][9:]
        #print (len(payload1))
        #print (len(payload2))
        #print (payload1, type(payload1))
        red_package =  bytes(p1 ^ p2 for p1, p2 in zip(payload1, payload2))
        
        if seq_num < 10:
            if cnt < 10:
                red_packages.append(('0' + str(seq_num)+ '|' + 'r' + '0' + str(cnt) + '|').encode('utf-8') + red_package)
            else:
                red_packages.append(('0' + str(seq_num)+ '|' + 'r' +  str(cnt) + '|').encode('utf-8') + red_package )
        else:
            if cnt < 10:
                red_packages.append((str(seq_num)+ '|' + 'r' + '0' + str(cnt) + '|' ).encode('utf-8') + red_package)
            else:
                red_packages.append((str(seq_num)+ '|' + 'r' +  str(cnt) + '|').encode('utf-8') + red_package)

        cnt += 1

    index = 2
    for rp in red_packages:

        packages.insert(index , rp)
        index += 3 

    return packages


class Server():

    def __init__(self):
        logging.info('Initializing Server')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((my_ip, 0))
        
        print ('port_num',self.sock.getsockname())
        self.clients_list = []
       

    def talkToClient(self, ip ,arg2):
        pack = arg2
        #print (type(packs_to_send))
        print (pack)
        self.sock.sendto(pack, ip)



    def listen_clients(self):
            
            while True:
                #socket.setdefaulttimeout(80)
                seq_num = 1
                msg, client = self.sock.recvfrom(1024)
                for loss_rate in err_rates:
                    if client not in self.clients_list:
                        print ('----------------------',seq_num)
                        print ('loss rate',loss_rate)
                        print ('All sent packages')
                        
                        packs_to_send = Create_UDP_Packages(big_String,100,seq_num)
                        for package in packs_to_send:
                            k = 0
                            while k < 1:
                                s = np.random.binomial(1, 1 - loss_rate)

                                if s == 1:

                                    k += 1
                                    t = threading.Thread(target=self.talkToClient, args=(client,),kwargs={'arg2':package})
                                    t.start()
                                
                                else:
                                    k += 1

                        seq_num += 1

                self.clients_list.append(client)

            
                
            

if __name__ == '__main__':
    # Make sure all log messages show up
    while True:
        logging.getLogger().setLevel(logging.DEBUG)
        b = Server()
        b.listen_clients()
   