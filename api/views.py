from django.db.models import Max, Min, Avg, Count, F
from django.db.models.functions import Round
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
import numpy as np
from api.models import Application, Placement, Student
from .serializers import PlacementSerializer, StudentSerializer, ApplicationSerializer


#basic apis for CRUD
class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


#statistics API

@api_view(['GET'])
def statistics_view(request):
    # Get all branches
    branches = Student.objects.values_list("branch", flat=True).distinct()
    
    stats = {
        "highest_ctc": {},
        "median_ctc": {},
        "lowest_ctc": {},
        "average_ctc": {},
        "percentage_placed": {},
        "students": []
    }
    
    for branch in branches:
        students_in_branch = Student.objects.filter(branch=branch)
        total_students = students_in_branch.count()

        #applications in which students got placed
        placed_students = students_in_branch.filter(application__selected=True).distinct()
        placed_count = placed_students.count()

        #ctcs for placed
        ctc_values = list(Placement.objects.filter(application__studentid__branch=branch, application__selected=True)
                          .values_list('ctc', flat=True))
        
        if ctc_values:
            stats["highest_ctc"][branch] = max(ctc_values)
            stats["lowest_ctc"][branch] = min(ctc_values)
            stats["median_ctc"][branch] = round(float(np.median(ctc_values)), 2)
            stats["average_ctc"][branch] = round(sum(ctc_values) / len(ctc_values), 2)
        else:
            stats["highest_ctc"][branch] = None
            stats["lowest_ctc"][branch] = None
            stats["median_ctc"][branch] = None
            stats["average_ctc"][branch] = None

        #placement percentage
        stats["percentage_placed"][branch] = round((placed_count / total_students) * 100, 2) if total_students else 0

    #student wise placement data
    students = Student.objects.prefetch_related('application_set__placementid').all()

    for student in students:
        applications = student.application_set.filter(selected=True)
        companies = applications.values_list('placementid__name', flat=True)
        ctc_offers = applications.values_list('placementid__ctc', flat=True)

        stats["students"].append({
            "rollno": student.rollno,
            "branch": student.branch,
            "batch": student.batch,
            "companies_selected": list(companies),
            "ctc": max(ctc_offers) if ctc_offers else None
        })

    return Response(stats)
