from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        self.accept()
        self.send(text_data="Hello world!")

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="Hello world!")

    def disconnect(self, close_code):
        pass