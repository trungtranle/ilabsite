from django.contrib import admin
from main.models import Test, TestCategory, Contact_requirement
# Register your models here.

class TestAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'referance_range', 'price', 'publish','sample_type', 'slug', 'description', 'related_post')
    list_filter = ['category', 'publish']
    list_display = ('name', 'category', 'referance_range', 'price', 'publish')
    search_fields = ['name']

class ContactAdmin(admin.ModelAdmin):
    list_filter = ['responded']
    list_display = ['name', 'added', 'email', 'phone_number', 'responded','edited']


admin.site.register(Test, TestAdmin)
admin.site.register(TestCategory)
admin.site.register(Contact_requirement, ContactAdmin)
