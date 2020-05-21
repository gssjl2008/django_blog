from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(verbose_name='问题', max_length=200)
    pub_date = models.DateTimeField(verbose_name='时间')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name='选项', max_length=200)
    votes = models.IntegerField(verbose_name='票数', default=0)

    def __str__(self):
        return self.choice_text