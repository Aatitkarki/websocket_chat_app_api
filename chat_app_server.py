from simple_websocket_server import WebSocketServer, WebSocket

# Change to your IP
hostname="10.0.0.78"
# hostname="192.168.1.64"
# Data Structure
# { address: (uniqueId,name)}
clients = {}

class ChatServer(WebSocket):
    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

    def handle(self):
        userId = None
        try:
            message = self.data
            print("There is something")
            if message is None:
                return
            elif message.startswith("register:"):
                userId, userName = message.split(":")[1].split(",")
                for key,value in clients.items():
                    if(key != self.address[0]):
                        value[2].send_message(f"active_user:{userId},{userName}")
                clients[self.address[0]+userId] = (userId, userName,self)
            elif message.startswith("unregister:"):
                userId = message.split(":")[1]
                clients.pop(self.address, None)
                for key,value in clients.items():
                    self.send_message(f"inactive_user:{value[0]},{value[1]}")
            elif message.startswith("message:"):
                recipientId,senderId,message = message.split(":")[1].split(",")
                # recipient = clients.get(recipientId)
                for key,value in clients.items():
                    # if(value[0] == recipientId):
                    print("Sending message")
                    value[2].send_message(f"senderId:{senderId},message:{message}")

            elif message.startswith("list users"):
                print("listing users")
                userId = message.split(":")[1]
                print(f"Listing users {userId} {message}")
                for key,value in clients.items():
                    if(key != self.address[0+userId]):
                        print("Seding User fom list")
                        self.send_message(f"active_user:{value[0]},{value[1]}")
        except Exception as e:
            print(f"Error is: {e}")
print("hlello world")
server = WebSocketServer(hostname,8000, ChatServer)
server.serve_forever()
