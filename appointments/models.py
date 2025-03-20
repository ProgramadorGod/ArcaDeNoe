
# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Cliente que agenda la cita
    pet_name = models.CharField(max_length=100)  # Nombre de la mascota
    date = models.DateTimeField()  # Fecha y hora de la cita
    reason = models.TextField()  # Motivo de la cita
    status = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='pendiente'
    )

    def __str__(self):
        return f"{self.pet_name} - {self.date.strftime('%Y-%m-%d %H:%M')}"
