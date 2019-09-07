from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter

from .models import Injury


class InjuryAdmin(MPTTModelAdmin, TranslationAdmin):

    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )


admin.site.register(Injury, InjuryAdmin)
