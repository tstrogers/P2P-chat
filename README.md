# P2P-Chat

This repository contains a peer to peer chat where friends can communicate with one another by using the chat3.py script. When a person signs on (runs the script) the rendezvous server (server3.py) prompts the user to enter the details of the person they would like to chat with. If the person is available to chat, the rendezvous server sends a message to this person with the details of the chat initiator (IP address and delivery port), letting them know that they would like to chat. If this person is not available to chat, the server makes the chat initiator aware and any sent messages are stored in an sql database on the client side. These messages are sent once the two people are online again and connect. The server keeps listening continuously for new connections in order to connect new people to chat.

Database: SQL lite

