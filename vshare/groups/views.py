from rest_framework import generics
from .models import Group , Membership
from users.models import Account
from .serializers import GroupRegistrationSerializer
from .serializers import GroupSerializer , MembershipSerializer
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from rest_framework.permissions import (
		AllowAny,
		IsAuthenticated,
		IsAdminUser,
		IsAuthenticatedOrReadOnly,
	)


class GroupList(generics.ListCreateAPIView):
    search_fields = ['groupid']
    filter_backends = (filters.SearchFilter,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user)

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'groupid'
    permission_classes = [AllowAny]

class MembershipList(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(the_member=req.user)



'''
class GroupsOfUser(generics.ListCreateAPIView):
	queryset = Group.objects.all()
	queryset.account_set.all()
	serializer_class = GroupSerializer
	lookup_field = 'Account.username'
	permission_classes = [AllowAny]
'''
@api_view(['POST',])
@permission_classes([AllowAny])
@csrf_protect
def GroupRegistration(request):
    #context = RequestContext(request)
    if request.method =='POST':
        serializer_class = GroupRegistrationSerializer(data=request.data)
        data = {}
        if serializer_class.is_valid():
            account = serializer_class.save()
            data['response'] = 'Successfully created'
            data['groupid'] = account.groupid
            data['title'] = account.title
            data['describtion'] = account.describtion
            data['invite_only'] = account.invite_only
            data['created_by'] = account.created_by
            data['members'] = account.members
        else:
            data = serializer_class.errors
        return Response(data)