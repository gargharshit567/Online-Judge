from rest_framework import serializers
from .models import Question, TestCase

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Question
        fields= '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=  TestCase
        exclude= ('question')
