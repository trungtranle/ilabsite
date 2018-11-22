from django.db import models

# Create your models here.
class TestCategory(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nhóm xét nghiệm'
        verbose_name_plural = 'Nhóm xét nghiệm'

class Test(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.PROTECT, verbose_name = 'Nhóm xét nghiệm')
    name = models.CharField(max_length = 100, verbose_name = 'Tên xét nghiệm')
    sample_type = models.CharField(max_length = 100, null=True, blank=True, verbose_name = 'Loại mẫu')
    description = models.TextField(null = True, blank= True)
    referance_range = models.CharField(max_length = 100, verbose_name = 'Reference range')
    price = models.PositiveIntegerField(null=True, blank = True)
    publish = models.BooleanField()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Xét nghiệm'
        verbose_name_plural = 'Xét nghiệm'

class Contact_requirement(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length = 100)
    email = models.EmailField(blank = True, null = True)
    phone_number = models.CharField(max_length = 12, blank = True)
    message = models.TextField()
    responded = models.BooleanField(default = False)

    def __str__(self):
        return self.name + self.added.strftime('%Y-%m-%d %H:%M')

    class Meta:
        verbose_name = 'Yêu cầu liên hệ'
        verbose_name_plural = 'Yêu cầu liên hệ'
		

