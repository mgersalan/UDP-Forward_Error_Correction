import threading
import socket
import logging
import numpy as np

err_rates = list(np.arange(0.0, 1.0, 0.06))
#err_rates = [0.0]

my_ip = socket.gethostname()

#big_String = 'Second point. Due to the way chunks are sliced up we know that all slices except the last one must be SliceSize (1024 bytes). We take advantage of this to save a small bit of bandwidth sending the slice size only in the last slice, but there is a trade-off: the receiver doesnt know the exact size of a chunk until it receives the last slice. I would like to add more lines to this data set I am trying to acoomplish'
#big_String = 'Second point. Due to the way chunks are sliced up we know that all slices except the last one must be SliceSize (1024 bytes). We take advantage of this to save a small bit of bandwidth sending the slice size only in the last slice, but there is a trade-off: the receiver doesnt know the exact size of a chunk until it receives the last slice. I would like to add more lines to this data set I am trying to acoomplish now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package '
big_String = 'Second point. Due to the way chunks are sliced up we know that all slices except the last one must be SliceSize (1024 bytes). We take advantage of this to save a small bit of bandwidth sending the slice size only in the last slice, but there is a trade-off: the receiver doesnt know the exact size of a chunk until it receives the last slice. I would like to add more lines to this data set I am trying to acoomplish now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package I would like to add more lines to this data set I am trying to acoomplish now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package now I am going to extend the package'

#err_rates = list(np.arange(0.0, 1.0, 0.05))
#loss_rate = float(input('Enter loos rate as float number'))

def Create_UDP_Packages(data,chunk_size,seq_num):
    ##divide payload and add id to it
    
    packages = []
    
    encoded = data.encode()
    loop_len = int(len(encoded) / chunk_size)
    loop_len += 1
    last_id = loop_len

    payload_dict = {}
    for i in range(0,loop_len):
        payload_dict[ "p" + str( i+1 ) ] = encoded[100*i:100*(i+1)]

    for key, value in payload_dict.items():
        if seq_num < 10:
            if int(key[1:]) < 10:
                packages.append(('0' + str(seq_num)+'|' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode())
            else:
                packages.append(('0' + str(seq_num)+'|' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode())

        else:
            if int(key[1:]) < 10:
                packages.append((str(seq_num)+'|' + str(last_id) + '|' + '0' + key[1:] + '|' + payload_dict[key].decode()).encode())
            else:
                packages.append((str(seq_num)+'|' + str(last_id) + '|' + key[1:] + '|' + payload_dict[key].decode()).encode())

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
        
        self.sock.sendto(pack, ip)



    def listen_clients(self):
            
            while True:
                #socket.setdefaulttimeout(80)
                seq_num = 1
                msg, client = self.sock.recvfrom(1024)
                for loss_rate in err_rates:
                    if client not in self.clients_list:
                        print ('loss rate',loss_rate)
                        
                        packs_to_send = Create_UDP_Packages(big_String,100,seq_num)
                        for package in packs_to_send:
                            k = 0
                            while k < 3:
                                s = np.random.binomial(1, 1 - loss_rate)
                                if s == 1:
                            
                                    t = threading.Thread(target=self.talkToClient, args=(client,),kwargs={'arg2':package})
                                    t.start()
                                k +=1
                    seq_num += 1
                self.clients_list.append(client)

            
                
            

if __name__ == '__main__':
    # Make sure all log messages show up
    while True:
        logging.getLogger().setLevel(logging.DEBUG)
        b = Server()
        b.listen_clients()
   
