from django.db import models

class Virus(models.Model):
    name=models.CharField(max_length=100)
    common_name=models.CharField(max_length=100)
    period=models.IntegerField()
    def __str__(self):
        return self.common_name

class Patient(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    idn=models.CharField(max_length=50)
    dob=models.DateField()
    def __str__(self):
        return self.firstname+' '+self.lastname

class Case(models.Model):
    case_id=models.CharField(max_length=20)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    virus=models.ForeignKey(Virus, on_delete=models.CASCADE)
    date=models.DateField()
    TYPE=(
        ('l', 'local'),
        ('i', 'imported')
    )
    category=models.CharField(max_length=1, choices=TYPE)
    def __str__(self):
        return self.case_id

class Location(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200, blank=True)
    x=models.FloatField()
    y=models.FloatField()
    def __str__(self):
        return self.name
    
class Visit(models.Model):
    case=models.ForeignKey(Case, on_delete=models.CASCADE)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)
    date_from=models.DateField()
    date_to=models.DateField()
    TYPE=(
        ('r', 'residence'),
        ('w', 'workplace'),
        ('v', 'visit')
    )
    category=models.CharField(max_length=1, choices=TYPE)
    def __str__(self):
        return self.case.case_id+', '+self.location.name+', '+self.dateStr(self.date_from)+', '+self.dateStr(self.date_to)

    def dateStr(self,o):
	    return o.strftime("%Y-%m-%d")

    
