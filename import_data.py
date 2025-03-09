import csv
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_placement_statistics.settings")
django.setup()

from api.models import Student, Placement, Application

# Function to import students
def import_students():
    with open("students.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Student.objects.update_or_create(
                rollno=row["id"],  
                defaults={
                    "batch": row["batch"],
                    "branch": row["branch"],
                },
            )
    print("Students imported successfully!")

# Function to import placements
def import_placements():
    with open("placements.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Placement.objects.update_or_create(
                id=row["id"],
                defaults={
                    "name": row["name"],
                    "role": row["role"],
                    "ctc": row["ctc"],
                },
            )
    print("Placements imported successfully!")

# Function to import applications
def import_applications():
    with open("placement_applications.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = Student.objects.get(rollno=row["studentid"])
            placement = Placement.objects.get(id=row["placementid"])
            Application.objects.update_or_create(
                id=row["id"],
                defaults={
                    "studentid": student,
                    "placementid": placement,
                    "selected": row["selected"].lower() == "true",
                },
            )
    print("Applications imported successfully!")

if __name__ == "__main__":
    import_students()
    import_placements()
    import_applications()
    print("All data imported successfully!")
