README
Programing Assignment 2
Rayhan Nazir, Ethan Van Deusen, Shruti Asolkar


Steps to run:

1. Open one command terminal that will host the server
2. cd to the location of the server.py file
3. Run the command "python server.py". Now the server should be running on that terminal
4. Open separate terminals based on the number of clients you want to test
5. On each of those terminals cd to the location of the client.py file
6. Run the command "python client.py". Now the clients will be running on each of the terminals.


List of commands to run:

%connect [server address] [port number]: For our server the address is 127.0.0.1 and our port number is 12345
%post [Subject] [Message]: This posts a message to the discussion board. The format of the post is [ID][username][date][time][Subject]
%users: provides a list of users in the discussion board
%message [Message ID]: Displays the message content of the provided Message ID
%exit: Leaves the server

%groups: Provides a list of groups in the server
%groupjoin [groupname]: Allows the user to join a specific group
%grouppost [groupname] [Subject] [Message]: Allows the user to post a message in a specific group
%groupusers [groupname]: Provides a list of users in a specific group
%groupleave [groupname]: Allows the user to leave a specific group
%groupmessage [groupname] [Message ID]: Allows the user to see a specific post in a specific group

Major Issues:

The only major issue we ran into was incorporating the groups with out existing commands in part 1. We had some problems with the commands 
such as post and message not working within the groups. To fix that we rewrote our code in part 1 to adapt to the new changes in part 2. 



Demo List of commands (Steps are numbered in what order to type them in): 
Terminal 1 (server):
	python server.py

Terminal 2 (client1):
	1 python client.py
	2 %connect 127.0.0.1 12345
	7 %post message content
	8 %exit
	11 %python client.py
	12 %connect 127.0.0.1 12345
	17 %groupjoin group1
	20 %grouppost group1 message content
	27 %groupleave group1
	28 %exit

Terminal 3 (client2):
	3 python client.py
	4 %connect 127.0.0.1 12345
	9 %exit
	13 %python client.py
	14 %connect 127.0.0.1 12345
	18 %groupjoin group2
	21 %grouppost group2 message2 content2
	22 %groupjoin group3
	23 %grouppost group2 message3 content3
	24 %grouppost group3 message4 content4
	25 %groupleave group2
	26 %exit

Terminal 4 (client3):
	5 python client.py
	6 %connect 127.0.0.1 12345
	10 %exit
	15 %python client.py
	16 %connect 127.0.0.1 12345
	19 %groupjoin group2
	29 %groupleave group2
	30 %exit
