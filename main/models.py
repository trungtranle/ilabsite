from django.db import models
from django.utils.text import slugify
import re
from django.contrib.auth.models import AbstractUser

#No Vietnamese accent
def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s

# Create your models here.
class TestCategory(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, null = True, blank = True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        name_no_accent = no_accent_vietnamese(self.name)
        unique_slug = slugify(name_no_accent)
        num = 1
        while Test.objects.filter(slug = unique_slug).exists():
            unique_slug = '{}-{}'.format(unique_slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(TestCategory, self).save(*args, *kwargs)

    class Meta:
        verbose_name = 'Nhóm xét nghiệm'
        verbose_name_plural = 'Nhóm xét nghiệm'

class Test(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.PROTECT, verbose_name = 'Nhóm xét nghiệm')
    name = models.CharField(max_length = 100, verbose_name = 'Tên xét nghiệm')
    sample_type = models.CharField(max_length = 100, null=True, blank=True, verbose_name = 'Loại mẫu')
    description = models.TextField(null = True, blank= True)
    referance_range = models.TextField(verbose_name = 'Reference range', blank=True, null=True)
    price = models.PositiveIntegerField(null=True, blank = True)
    publish = models.BooleanField(default = True)
    slug = models.SlugField(max_length = 100, null = True, blank = True)
    related_post = models.URLField(verbose_name='Bài viết liên quan', null = True, blank = True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        name_no_accent = no_accent_vietnamese(self.name)
        unique_slug = slugify(name_no_accent)
        num = 1
        while Test.objects.filter(slug = unique_slug).exists():
            unique_slug = '{}-{}'.format(unique_slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Test, self).save(*args, *kwargs)

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


# Only for LAST_ACTIVITY = True
