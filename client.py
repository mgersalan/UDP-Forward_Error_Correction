
import socket 
import sys
import numpy as np
import time
import matplotlib.pyplot as plt

err_rates = list(np.arange(0.0, 1.0, 0.05))
#err_rates = [0.0]
s_rates = []
s_rates_sf = []


unique_id = 1

host = socket.gethostname() 
text = input("enter port")
port = int(text)
BUFFER_SIZE = 1024
#MESSAGE = input("message to be sent from Client") 
#MESSAGE = '' + str(p_number)

udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

#udpClient.connect((host, port))

MESSAGE = 'Hello from client'

def reconstruct(packages,n):
    
    rec_message = []

    for i in range(0,n+1):
        for p in packages:
            if int(p[p.find('|') + 4 : p.find('|') + 6 ]) == i:
                rec_message.append(p[(p.find('|') + 7) : ])
                break
    res = ''.join(rec_message)
    #print ('len of decoded',len(res))
    return res

def decode_original_message(packs_recieved,s_num):
    #print (packs_recieved)
    package = packs_recieved[0]
    print ('\n')
    print ('\n')
    print ('--> for Sequence number ', package[0:2])
    print (len(packs_recieved),' packages recieved, supposed to be ', 3 * int((package[package.find('|') + 1 : package.find('|') + 3 ])))
    print ('All recieved packages :')
    # start deconstruction
    #print ('Recieved Packages')
    #print (packs_recieved)
    pack_ids_recieved = []                  # not uniqiue, all pack ideas 
    last_pack_id = int(package[package.find('|') + 1 : package.find('|') + 3])
    for p in packs_recieved:
        pack_ids_recieved.append(int(p[p.find('|') + 4 : p.find('|') + 6]))
        print (p)
        #print ('-------')
    
    #print ('pack ids recieved')
    #print (pack_ids_recieved)
    unique_ids = list(set(pack_ids_recieved))
    print ('\n')
    print ('--->recieved unique ids',unique_ids)
    print ('---->required ids',list(range(1,int(last_pack_id)+1)))

    #print ('recieved packages contains all required packages to decode the original message', set(unique_ids).issubset(list(range(1,int(last_pack_id)+1)))) 
    print ('----->recieved packages contains all required packages to decode the original message', set(list(range(1,int(last_pack_id)+1))).issubset(unique_ids)) 

    s = set(list(range(1,int(last_pack_id)+1))).issubset(unique_ids)

    if s:
        print ('-----> Data can be reconstructed properly')
        print ('Reconstrcuted Data')
        print ('\n')
        
        rec_message = reconstruct(packs_recieved,int(last_pack_id))
        print (rec_message)
        print ('\n')
        print ('Reconstrcuted Data')
        print ('\x1b[6;30;42m' + '******* For Sequence number ', s_num , 'DATA CAN BE FULLY RECONSTRUCTED *******' + '\x1b[0m' )
        return ('success',1)
        
    else:
        missed = (int(last_pack_id)) - len(unique_ids)
        print ('\x1b[6;30;42m' + '******* For Sequence number ', s_num , 'DATA CAN BE RECONSTRUCTED with a success rate of -->', (int(last_pack_id) - missed)/(int(last_pack_id)),' *******' + '\x1b[0m')
        return ('fail',(int(last_pack_id) - missed)/(int(last_pack_id)))


def Divide_Packs_Into_Sequences(all_Packets,seq_num):
    #get packages with seq num and return them
    pack_to_ret = []
    if seq_num < 10:
        for pack in all_Packets:
            if int(pack[1]) == int(seq_num):
                pack_to_ret.append(pack)
    else:
        for pack in all_Packets:
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
        package = data.decode()
        packs_recieved.append(package)
        print ('-----------------')
        #print (data)
        print ('--->Recieved package with sequence number ', package[0:package.find('|') -1])
        print ('--->Recieved package with id ', package[package.find('|') + 4:6])
        #print ('--->Recieved and decoded ', package[7:])
        print ('---->Last num of the sequence ', total_num_of_seqs)
        print ('---->Last num of packages in this sequence ', package[package.find('|') + 1 : package.find('|') + 3])
        print ('--------------------')
    except socket.timeout:
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

plt.plot(err_rates, s_rates, 'bo')
plt.show()