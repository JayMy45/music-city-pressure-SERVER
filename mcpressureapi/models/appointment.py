from django.db import models

class Appointments(models.Model):
    employee = models.ManyToManyField("Employee", blank=True, related_name="employee_id", through='EmployeeAppointment')
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True, related_name='confirm')
    service_type = models.ForeignKey("ServiceType", null=True, blank=True, on_delete=models.CASCADE)
    progress = models.ForeignKey("Progress", null=True, blank=True, on_delete=models.CASCADE)
    request_details = models.CharField(max_length=200)
    image = models.CharField(max_length=1000)
    request_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    date_completed = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    scheduled = models.BooleanField(default=False)
    consultation = models.BooleanField(default=False)
    completed = models.BooleanField(default=False) 
    confirm = models.BooleanField(default=False)

    @property
    def confirmed(self):
     return self.__confirmed

    @confirmed.setter
    def unconfirmed(self, value):
        self.__confirmed = value
    
