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
        print('connected')
        # alreadyRegistered= clients.has_key(self.address[0])
        # if alreadyRegistered:
        #     data=clients[self.address[0]]
        #     userId= data[0]
        #     userName = data[1]
        #     for key,value in clients.items():
        #         if(key != self.address[0]):
        #             messageData = {
        #                 'type':'activeUser',
        #                 'data':{
        #                     'uid':userId,
        #                     'name':userName,
        #                     'isOnline':True
        #                 },
        #             }
        #             json_object = json.dumps(messageData, indent = 4) 
        #             value[2].send_message(json_object)

    def handle_close(self):
        print("Disconnected")
        ipadd = self.address[0]
        uid = clients[ipadd][0]
        name = clients[ipadd][1]
        del clients[ipadd]
        for key,value in clients.items():
            messageData = {
                'type':'activeUser',
                'data':{
                    'uid':uid,
                    'name':name,
                    'isOnline':False
                },
            }
            json_object = json.dumps(messageData, indent = 4) 
            value[2].send_message(json_object)
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
            elif requestType == "videoCallStarted":
                print("Video call started")
                recipientId = data['receiverId']
                for key,value in clients.items():
                    if(value[0] == recipientId):
                        value[2].send_message(self.data)

            elif requestType == "videoCallAccepted":
                print("Video call accepted")
                callerId = data['callerId']
                for key,value in clients.items():
                    if(value[0] == callerId):
                        value[2].send_message(self.data)

            elif requestType == "videoCallRejected":
                print("Video call rejected")
                callerId = data['callerId']
                for key,value in clients.items():
                    if(value[0] == callerId):
                        value[2].send_message(self.data)
                
            elif requestType == "videoCallEnded":
                print("Video call ended")
                callerId = data['callerId']
                for key,value in clients.items():
                    if(value[0] == callerId):
                        value[2].send_message(self.data)
                print("Video call ended")

            # TODO: ADD UNREGISTER FEATURE 
            # elif requestType == "unregister":
            #     print("UnRegistering User")
            #     userId= data['uid']
            #     userName = data['name']
            #     for key,value in clients.items():
            #         if(key != self.address[0]):
            #             messageData = {
            #                 'type':'activeUser',
            #                 'data':{
            #                     'uid':userId,
            #                     'name':userName,
            #                     'isOnline':True
            #                 },
            #             }
            #             json_object = json.dumps(messageData, indent = 4) 
            #             value[2].send_message(json_object)
            #     clients[self.address[0]] = (userId, userName,self)
        except Exception as e:
            print(f"Error is: {e}")

print("hello boos")
server = WebSocketServer(hostname,8000, ChatServer)
server.serve_forever()
