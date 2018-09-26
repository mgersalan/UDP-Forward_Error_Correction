# UDP-Forward_Error_Correction


## 1) Triple Redundancy
I used a multi-threaded server to send the data to the client. I had 2 separate scripts as server.py and client.py. I used different articles to test my system but examples below are from a UTF-8 text test file. ​https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt

Server.py and client.py scripts are used in this scheme.

Server Side
I defined a class called server which has its own methods as ​init where socket connection and binding is defined, ​listen_clients ​where we have socket_recieve to start data transmission after a client connects, it sends data in sequences. Data sent is the same but with different losses in each sequence. Before sending the data we call ​Create_UDP_Packages which prepares each package to be sent in a sequence(with a specific error rate). Create_UDP_Packages takes the data, #number of bytes in the payloads(100) and sequence number as inputs and returns all packages to be sent by dividing the data into packages which have 100 bytes of payloads plus overhead for each package. Create_UDP_Packages returns these packages and stored in our packs_to_send variable. Then, there is a while loop which sends all packages 3 times. In that while loo loss transmission is injected by using numpy's random.binomial function which returns success with a probability of (1 - loss rate). So if the loss rate is 0.40, for each package to be sent, np.random.binomial returns 1 or 0 with a probability of 0.60 returning 1. If 1 is returned package would be sent in a thread by passing the package and client as the arguments in the talkToClient​ function which sends the package to the client in a thread.

 When client connects, data stream start. Until time out data is read, id's and sequences are printed to the terminal for each package decoded and appended to the packs_recieved array without processing. Packs_Recieved array would be processed after the time out.

Next, when the socket timeout occurs, actual processing and reconstruction starts.
There is a main for loop which iterates through the sequence numbers, as we defined in the server side each sequence corresponds to sending the same data but with different error rates.


● All packages received are sent to the ​Divide_Packs_Into_Sequences function for each sequence number. So we call the Divide_Packs_Into_Sequences for each sequence number and it returns the packages only with specified sequence number. Let's say we set the parameter of sequence numbers as 1 and called our function, in return we will have only the packages which belongs to the sequence number 1 filtered and returned and stored in ​divided_packs​ array.
● After getting and storing the packages belongs to a specific sequence number in divided_packs then we call our second function, ​decode_original_message which takes input as ​divided_packs​ and ​sequence number​.
● decode_original_message function is where the most of the job is done. The mechanism works like extracting the package ids first by checking the id part of the overhead of each package. For each package, their id's are extracted from the overhead part and stored in ​pack_ids_recieved array. Then from those id's unique id's are extracted. We also extract the total number of packages (last_id) of the package from the overhead. Now, we have all the unique id's received and total number of packages from the last_id of the sequence. Now it is easy to do a list comparison and see how many of the packages are missing.
● There is another function called ​reconstruct,​ which would display the whole recovered data if all the packages of the sequence can be reconstructed properly. If all the required ids are subset of all the unique ids, this means there is no missing package, in that case whole message can be reconstructed with a success rate of 100%, in this case to display the recovered data we call the reconstruct function and print the recovered data to the terminal.
● If there are missing packages, we store the number of missing packages in the ​missed variable and return the success rate.
● There is also a binary success or fail rate defined, which returns success only if whole data can be reconstructed otherwise fail but we will use the partial success rates in our graphs.
● I added different print statements to decode_original_message function to observe the reconstructions and success rates before the graph.

For each sequence, steps are displayed in the terminal before sketching the graphs. 

How does increasing loss rate affect the success rate of decoding? Provide your answer as a graph where you plot the success rate as a function of the loss rate.
As we can see since we are using triple redundancy, even in the very high loss rates there is still relatively high success rates. For each triplet of same package we can lose 2 of it and still will be able to reconstruct the package. So for 2⁄3 loss is tolerable and even only 1⁄3 of the packages delivered are enough per triplet.


What was the overhead, i.e., how many additional bytes you needed to send to get a certain number of bytes successfully decoded?

b'17|29|01|This test file can help you examine, how your UTF-8 decoder handles\nvarious types of correct, malfor'

● 17 is the sequence number
● 29 is the last id (biggest id) of the sequence
● 01 is the id of the package
● Each of them separated with '|' character, and after that 100 bytes of payload starts
● In total, 9 bytes are used for the overhead, sequence number is not necessary if data
would be send with user defined one loss rate.
Note: Input for loss transmission parameter by user is implemented but commented it out, since I created a for loop for different error rates and send each sequence of data with different error rates. To use it, for loop in the listen_clients should be should be modified that it would take the loss rate imputed from the user.

