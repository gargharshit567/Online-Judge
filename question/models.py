from django.db import models
from ojuser.models import Ojuser
# Create your models here.

class Question(models.Model):
    name = models.TextField(max_length = 50)
    statement = models.TextField(max_length=9000)
    sample_input = models.TextField(max_length=9000)
    explanation = models.TextField(max_length = 9000,null = True)
    creator = models.ForeignKey(Ojuser,null = True, on_delete=models.SET_NULL)
    submissions = models.IntegerField(default=0)
    editorial = models.TextField(max_length = 9000, default = '')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


