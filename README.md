#### Health Dashboard meant for patients to keep record of their Healthcare. Built using Cryptographically secure Server Client Model using RSA. Created with a team for Queens Summer Computing Challenge; Won 3rd place.

___

## Project Screen Shots

![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/1.png?raw=true)
![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/2.png?raw=true)
![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/3.png?raw=true)
![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/4.png?raw=true)
![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/5.png?raw=true)
![ALT](https://github.com/RamyPoe/QueensGroupProject/blob/master/images/6.png?raw=true)


## Installation and Setup Instructions

Clone down this repository. Tested on `Windows 10`. Setup instructions will be for `Windows 10`. Created using `Python 3.10.x`.

#### Server

See `Server/config.py` before running. Can be run using `Server/server.py`. Using non-blocking io sockets via selector to handle multiple clients. Threading should be implemented in the future for further simultaneousness.

#### Client

See `Client/Main.py` before running to configure server IP. Can be run via `Client/Main.py`. Uses Tkinter GUI for user interaction.


## Reflection

This was a 2 week long project built for Queens Summer Computing Challenge. Project goals included:  
 - Applying good code practices
 - Familiarization with Tkinter GUI toolkit
 - Learning Server/Client models
 - Hashing and cryptography
 - Encryption and Key handshakes for all network traffic
 - Custom database for well structured user data
