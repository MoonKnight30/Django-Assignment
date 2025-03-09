from rest_framework import serializers
from api.models import Placement, Student, Application

class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    studentid = serializers.SlugRelatedField(
        queryset=Student.objects.all(), slug_field='rollno'
    )
    placementid = PlacementSerializer(read_only=True) 

    class Meta:
        model = Application
        fields = '__all__'

