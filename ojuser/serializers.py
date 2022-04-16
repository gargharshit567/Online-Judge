from rest_framework import serializers
from .models import Ojuser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ojuser
        fields= ['name', 'email', 'password', 'username']
        extra_kwargs= {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password= validated_data.pop('password')

        ojuser= self.Meta.model(**validated_data)
        if password is not None:
            ojuser.set_password(password)
        ojuser.save()
        return ojuser

class LoginSerializer(serializers.Serializer):
    email= serializers.CharField(max_length= 255, required= True)
    password= serializers.CharField(max_length= 255, required= True)
    extra_kwargs= {
            'password': {'write_only': True}
        }