from rest_framework import serializers
from .models import Question, TestCase

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields= '__all__'

class FileSerializer(serializers.Serializer):
    extension = serializers.CharField(max_length= 255, required= True),
    code = serializers.CharField(max_length= 255, required= True)
