# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import channels
from .models import Ant, Field
from .draw import Draw
import json

class AntConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        self.field = Field(id = 0)
        self.field.initField()
        self.field.createAnts()

    def disconnect(self, close_code):
         pass

    def receive(self, text_data):
        draw = Draw()
        self.field.moveAnts()
        matrix = draw.getDrawingMatrix(self.field)
        self.field.globalEvaporate()
        self.send(text_data=json.dumps({'matrix': matrix}))