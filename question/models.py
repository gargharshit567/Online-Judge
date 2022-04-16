from django.db import models
from ojuser.models import Ojuser
# Create your models here.

class Question(models.Model):
    name = models.TextField(max_length = 50)
    code= models.CharField(max_length=6,unique= True)
    statement = models.TextField(max_length=9000)
    sample_input = models.TextField(max_length=9000)
    explanation = models.TextField(max_length = 9000,null = True)
    creator = models.ForeignKey(Ojuser,null = True, on_delete=models.SET_NULL)
    submissions = models.IntegerField(default=0)
    editorial = models.TextField(max_length = 9000, default = '')
    test_case_cnt = models.IntegerField(default=0)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class TestCase(models.Model):
    testcase_input = models.TextField(max_length = 1000)
    testcase_output = models.TextField(max_length = 1000)
    questionId= models.ForeignKey(Question,null= True, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    


