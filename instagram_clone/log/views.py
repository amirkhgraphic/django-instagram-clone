from rest_framework.generics import CreateAPIView

from .models import Log
from .serializers import LogSerializer


class LogCreateAPIView(CreateAPIView):
    model = Log
    serializer_class = LogSerializer
