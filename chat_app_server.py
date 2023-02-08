from simple_websocket_server import WebSocketServer, WebSocket
import json

# Change to your IP
# hostname="10.0.0.78"
hostname="192.168.1.64"
# Data Structure
# { ipadd: (uniqueId,name,wsaddress)}
clients = {}

class ChatServer(WebSocket):
    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

    def handle(self):
        userId = None
        try:
            rawMessage = self.data
            wsRequestData=json.loads(rawMessage)
            requestType = wsRequestData['type']
            data = wsRequestData['data']
            print(f"The message is as: {rawMessage}")
            if wsRequestData is None:
                return
            elif requestType == "register":
                print("Registering User")
                userId= data['uid']
                userName = data['name']
                for key,value in clients.items():
                    if(key != self.address[0]):
                        messageData = {
                            'type':'activeUser',
                            'data':{
                                'uid':userId,
                                'name':userName,
                                'isOnline':True
                            },
                        }
                        json_object = json.dumps(messageData, indent = 4) 
                        value[2].send_message(json_object)
                clients[self.address[0]] = (userId, userName,self)

            elif requestType == "listUsers":
                print("Listing Users")
                userId = data['uid']
                for key,value in clients.items():
                    print(f"The saved id {value[0]} and current userID {userId}")
                    if(value[0] != userId):
                        messageData = {
                            'type':'activeUser',
                            'data':{
                                'uid':value[0],
                                'name':value[1],
                                'isOnline':True
                            },
                        }
                        json_object = json.dumps(messageData, indent = 4)
                        self.send_message(json_object)
            elif requestType == "textMessage":
                recipientId = data['receiverId']
                for key,value in clients.items():
                    if(value[0] == recipientId):
                        value[2].send_message(self.data)
            elif wsRequestData.startswith("unregister:"):
                userId = wsRequestData.split(":")[1]
                clients.pop(self.address, None)
                for key,value in clients.items():
                    self.send_message(f"inactive_user:{value[0]},{value[1]}")
            elif wsRequestData.startswith("message:"):
                recipientId,senderId,wsRequestData = wsRequestData.split(":")[1].split(",")
                # recipient = clients.get(recipientId)
                for key,value in clients.items():
                    # if(value[0] == recipientId):
                    print("Sending message")
                    value[2].send_message(f"senderId:{senderId},message:{wsRequestData}")
        except Exception as e:
            print(f"Error is: {e}")
server = WebSocketServer(hostname,8000, ChatServer)
server.serve_forever()
