from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ListCreateMessageAPIView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
