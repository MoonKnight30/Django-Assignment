from django.db import models



class Placement(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) 
    role = models.CharField(max_length=100)
    ctc = models.FloatField() 

    def __str__(self):
        return f"{self.name} - {self.role} ({self.ctc} LPA)"
    


class Student(models.Model):
    rollno = models.CharField(max_length=9, primary_key=True)
    batch = models.IntegerField(default=2021)  
    branch = models.CharField(max_length=20, choices=(
        ('CSE', 'Computer Science & Engineering'),
        ('EP', 'Engineering Physics'),
        ('EE', 'Electrical Engineering'),
        ('MNC', 'Mathematics & Computing'),
        ('MMAE', 'Mechanical & Manufacturing Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('CHEMICAL', 'Chemical Engineering'),
    ))

    def __str__(self):
        return self.rollno + '--'+self.branch

class Application(models.Model):
    id = models.AutoField(primary_key=True)  
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE, to_field='rollno')  
    placementid = models.ForeignKey(Placement, on_delete=models.CASCADE)  
    selected = models.BooleanField(default=False)  

    class Meta:
        constraints = []
    def __str__(self):
        status = "Selected" if self.selected else "Not Selected"
        return f"{self.studentid.rollno} → {self.placementid.name} ({status})"

