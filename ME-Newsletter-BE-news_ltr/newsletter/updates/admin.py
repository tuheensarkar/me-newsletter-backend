from django.contrib import admin
from newsletter.updates.models import Update

class UpdateAdmin(admin.ModelAdmin):
    fields = ['newsletter','title','content','region', 'country','publish','is_active', 'is_deleted', 'meta_title', 'meta_description', 'meta_keywords']


admin.site.register(Update, UpdateAdmin)
