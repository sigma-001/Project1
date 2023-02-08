from rest_framework import serializers, status
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data['username'],
                                        password = validated_data['password'])
        return user
        
        
        
class WorkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Work
        fields = "__all__"
        