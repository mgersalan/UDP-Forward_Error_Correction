# Muzaffer Gur Ersalan, 014841873
import socket 
import sys
import numpy as np
import time
import matplotlib.pyplot as plt
import math

err_rates = list(np.arange(0.0, 1.0, 0.05))
#err_rates = [0.0]
s_rates = []
s_rates_sf = []


unique_id = 1

host = socket.gethostname() 
text = input("enter port")
port = int(text)
BUFFER_SIZE = 1638400
#MESSAGE = input("message to be sent from Client") 


udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 


MESSAGE = 'Hello from client'

def reconstruct_xor(p1,p2,n):
    
    rec_package = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(p1,p2))
    #print ('recovered pack',type(l),'--> ', l )

    return rec_package

def decode_original_message(packs_recieved,s_num):
    
    print ('\033[91m' + 'SEQ NUM', str(s_num) + '\033[0m')
    print ('\n')
    #print (packs_recieved)
    ##
    last_pack_id = 0
    for p in packs_recieved:
        if 'r' not in p[0:4]:
            last_pack_id = int(p[p.find('|') + 1 : p.find('|') + 3])
            
    
    if last_pack_id == 0:
        print ('For sequence number',s_num,' all recieved packages are redundancy packages')
        return ('fail', 0.0) 
    
    pack_ids_recieved = {}
    redundants_recieved = {} 
    for p in packs_recieved:
        if 'r' not in p[0:4]:
            #pack_ids_recieved.append(int(p[p.find('|') + 4 : p.find('|') + 6]))
            pack_ids_recieved[p[p.find('|') + 4 : p.find('|') + 6]] = p[p.find('|') + 7 : ]
            
        else:
            #pack_ids_recieved.append((p[p.find('|') + 1 : p.find('|') + 4]))
            redundants_recieved[p[p.find('|') + 2 : p.find('|') + 4]] = p[p.find('|') + 5 : ]
    

    missing_list = list(range(1,int(last_pack_id)+1))
    
    for key, value in pack_ids_recieved.items():
        if int(key) in missing_list:
            missing_list.remove(int(key))
    
   
    if len(missing_list) == 0:
        
        print ('Succesfully reconstructed data')
        print ('\n')

    for key in range(1,last_pack_id + 1):
        
        if int(key) in missing_list:
            
            if int(key) % 2 == 0:
                red_keys = [int(i) for i in redundants_recieved.keys()]
                if int(key) - 1 not in missing_list and int(key) / 2 in red_keys:
                    if key < 11:
                        if math.ceil(int(key) / 2) < 10:
                            rc_pack = reconstruct_xor(pack_ids_recieved[('0' + str(int(key) - 1))] , redundants_recieved['0' + str(math.ceil(int(key) / 2))], int(last_pack_id))
                        else:
                            rc_pack = reconstruct_xor(pack_ids_recieved[('0' + str(int(key) - 1))] , redundants_recieved[str(math.ceil(int(key) / 2))], int(last_pack_id))
                    else:
                        if math.ceil(int(key) / 2) < 10:
                            rc_pack = reconstruct_xor(pack_ids_recieved[str(int(key) - 1)] , redundants_recieved['0' + str(math.ceil(int(key) / 2))], int(last_pack_id))
                        else:
                            rc_pack = reconstruct_xor(pack_ids_recieved[str(int(key) - 1)] , redundants_recieved[str(math.ceil(int(key) / 2))], int(last_pack_id))
                    if rc_pack:
                        print ('-------------------------------------------------------------------')
                        #print ('\033[91m' + 'SEQ NUM ' , str(s_num) + '\033[0m')
                        print ('Succesful reconstruction of missing package number', int(key))
                        print ('Reconstructed package -- >  ', rc_pack)
                        print ('\n')
                        print ('-------------------------------------------------------------------')
                        missing_list.remove(int(key))
                        pack_ids_recieved[str(key)] = rc_pack
                else:
                    print ('Package with Id ', key , 'can not be reconstructed')
            
            else:
                red_keys = [int(i) for i in redundants_recieved.keys()]
                if int(key) + 1 not in missing_list and math.ceil(int(key) / 2) in red_keys:
                    if key < 9:
                        if math.ceil(int(key) / 2) < 10:
                            rc_pack = reconstruct_xor(pack_ids_recieved[('0' + str(int(key) + 1))] , redundants_recieved['0' +str(math.ceil(int(key) / 2))],int(last_pack_id))
                        else:
                            rc_pack = reconstruct_xor(pack_ids_recieved[('0' + str(int(key) + 1))] , redundants_recieved[str(math.ceil(int(key) / 2))],int(last_pack_id))
                    
                    else:
                        if math.ceil(int(key) / 2) < 10:
                            rc_pack = reconstruct_xor(pack_ids_recieved[str(int(key) + 1)] , redundants_recieved['0' + str(math.ceil(int(key) / 2))],int(last_pack_id))
                        else:
                            rc_pack = reconstruct_xor(pack_ids_recieved[(str(int(key) + 1))] , redundants_recieved[str(math.ceil(int(key) / 2))],int(last_pack_id))
                    
                    if rc_pack:
                        
                        print ('-------------------------------------------------------------------')
                        #print ('\033[91m' + 'SEQ NUM', str(s_num) + '\033[0m')
                        print ('Succesful reconstruction of missing package number', int(key))
                        print ('Reconstructed package -- >', rc_pack)
                        print ('\n')
                        print ('-------------------------------------------------------------------')
                        missing_list.remove(int(key))
                        pack_ids_recieved[str(key)] = rc_pack
                else:
                    
                    print ('Package with Id ', key , 'can not be reconstructed')
                    

        else:
            print ('Succesful reconstruction of delievered package number', int(key))
            continue
     
    last_pack_id = int(last_pack_id)
    missed = len(missing_list)
    if missed != 0:
        print ('\x1b[6;30;42m' + '******* For Sequence number ', s_num , 'DATA CAN BE RECONSTRUCTED with a success rate of -->', (last_pack_id - missed) / last_pack_id,' *******' + '\x1b[0m')
        print ('\n')
        return ('fail', (last_pack_id - missed) / last_pack_id)
    else:
        if missed == 0:
            print ('\x1b[6;30;42m' + '******* For Sequence number ', s_num , 'DATA CAN BE RECONSTRUCTED with a success rate of -->', '1.0' ,' *******' + '\x1b[0m')
            print ('\n')
            
            # Print the whole reconstructed data if there is no missing package

            #print ('Reconsctruted whole data is below')
            #bigstr = []
            #for k in range(1,last_pack_id + 1):
            #    if k < 10:
            #        bigstr.append(pack_ids_recieved['0' + str(k)])
            #    else:
            #        bigstr.append(pack_ids_recieved[str(k)])
            #bigstr_ = ''.join(bigstr)
            #print (bigstr_)
            #print ('\n')
            ################################################

            return ('success', (last_pack_id - missed) / last_pack_id)
        else:    
            print ('\x1b[6;30;42m' + '******* For Sequence number ', s_num , 'DATA CAN BE RECONSTRUCTED with a success rate of -->', (last_pack_id - missed) / last_pack_id,' *******' + '\x1b[0m')
            print ('\n')
            return ('success', (last_pack_id - missed) / last_pack_id)


def Divide_Packs_Into_Sequences(all_Packets,seq_num):
    #get packages with seq num and return them
    pack_to_ret = []
    if seq_num < 10:
        for pack in all_Packets:
            #print ('altinda')
            #print (pack)
            pack = pack.decode()
            if int(pack[1]) == int(seq_num):
                pack_to_ret.append(pack)
    else:
        for pack in all_Packets:
            pack = pack.decode()
            if int(pack[0:2]) == int(seq_num):
                pack_to_ret.append(pack)

    return pack_to_ret




packs_recieved = []
total_num_of_seqs = len(err_rates)

while True:
    
    #udpClient.send(MESSAGE.encode())
    udpClient.sendto(MESSAGE.encode(),(host, port))   
    try:  
        data = udpClient.recv(BUFFER_SIZE)
        #package = data.decode()
        package = data
        packs_recieved.append(package)

        print (package)

        print ('-----------------')
        #print (data)
        print ('Recieveing Data')
        #print ('--->Recieved packages with sequence number ', package[0:package.find('|') -1])
        #print ('--->Recieved package with id ', package[package.find('|') + 3])
        #print ('--->Recieved and decoded ', package[7:])
        #print ('---->Last num of the sequence ', total_num_of_seqs)
        #print ('---->Last num of packages in this sequence ', package[package.find('|') + 1])
        #print ('--------------------')
    except socket.timeout:
        
        print ('\n')
        print ('\n')
        print ('!------!')
        print ('no more data coming --- timed out')

        for s_num in range(1,total_num_of_seqs + 1):
            divided_packs = Divide_Packs_Into_Sequences(packs_recieved,s_num)
            if divided_packs:
                ret = decode_original_message(divided_packs,s_num)
                s_f = ret[0]
                s_rate = ret[1]
                s_rates.append(round(s_rate, 3)) 
                if s_f == 'fail':
                    s_rates_sf.append(0)
                else:
                    s_rates_sf.append(1)

            else:
                s_rates.append(0)
                s_rates_sf.append(0)
        break
        

    udpClient.settimeout(5)
    
rounded_er = [round(e,3) for e in err_rates]

print ('onezero_srates ', s_rates_sf)
print ('s_rates ',s_rates)
print ('e_rates ',rounded_er)
udpClient.close() 

## Remove here if user inputs the loss rate

plt.plot(err_rates, s_rates, 'bo')
plt.show()