from rest_framework import generics, permissions
from bugs.models import Bug
from bugs.serializers import BugSerializer

class BugListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = [permissions.DjangoModelPermissions]

class BugRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = [permissions.DjangoModelPermissions]
