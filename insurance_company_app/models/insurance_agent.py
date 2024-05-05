import re

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .company_branch import CompanyBranch
from .base_model import BaseModel


class InsuranceAgent(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    address = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=20)
    branch_name = models.ForeignKey(CompanyBranch, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/agents_photos')

    class Meta:
        verbose_name = 'Страховой агент'
        verbose_name_plural = 'Страховые агенты'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        if 18 > self.age > 120:
            raise ValidationError({'age': "You should be at least 18 years old!"})

        if not re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', self.phone_number):
            raise ValidationError('Phone number must be in the format +375 (29) XXX-XX-XX')


@receiver(post_save, sender=InsuranceAgent)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Employee')
        instance.user.groups.add(group)
