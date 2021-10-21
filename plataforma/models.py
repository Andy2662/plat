from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class data_table(models.Model):
    latitud = models.CharField(_("latitud"),max_length=200)
    longitud = models.CharField(_("longitud"),max_length=200)
    imsi = models.CharField(_("imsi"),max_length=200)
    date = models.DateTimeField(_("date"), auto_now=True)
    test_name = models.CharField(_("test_name"),max_length=200)
    pot_db = models.CharField(_("pot_db"),max_length=200)
    operador = models.CharField(_("operador"),max_length=200)
    user = models.CharField(_("user"),max_length=200)
    observacion = models.CharField(_("observacion"),max_length=200)


    def __str__(self):
        return f"Datos recolectados en {self.date}"

    def datepublished(self):
        return self.fecha.strftime("%m/%d/%Y, %H:%M:%S")

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    def __str__(self):
        return f"Nombre del archivo: {self.file_name}"