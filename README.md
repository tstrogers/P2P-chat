# P2P-Chat

This repository contains a peer to peer chat where friends can communicate with one another by using the client.py script. When a person signs on (runs the script) the rendezvous server (server.py) prompts the user to enter their username and password.

<img width="696" alt="Screenshot 2023-05-07 at 12 45 25 AM" src="https://user-images.githubusercontent.com/93225913/236659524-6f64d5af-ca2f-4c4d-996c-48f34e6c1e6e.png">

If the username and password are authenticated, the next screen prompts the user to enter the name of the person they would like to chat with. 

<img width="695" alt="Screenshot 2023-05-07 at 12 51 58 AM" src="https://user-images.githubusercontent.com/93225913/236659566-a91706bf-19d2-46fe-a9e9-f4cc3200b6e0.png">

If this person is not available to chat, the server makes this known via a message screen.

<img width="291" alt="Screenshot 2023-05-07 at 1 20 46 AM" src="https://user-images.githubusercontent.com/93225913/236659620-3f4a45a4-6902-4df4-b680-d028c87f3b1c.png">


Any sent messages are stored in an sql database on the client side. These messages are sent once the two people are online again and connect. 

If the person is available to chat, the rendezvous server exchanges information between the pairs and allows them to connect.

<img width="678" alt="Screenshot 2023-05-07 at 1 50 15 AM" src="https://user-images.githubusercontent.com/93225913/236660153-8bcc0b4b-e6d4-477e-8d1a-861c6427a800.png">

<img width="681" alt="Screenshot 2023-05-07 at 1 50 08 AM" src="https://user-images.githubusercontent.com/93225913/236660157-ab0e3e7f-12f1-4e5e-ac4f-8ea43b5c71eb.png">


The server keeps listening continuously for new connections in order to connect new people to chat.

Database: SQL lite

