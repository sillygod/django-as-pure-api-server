from modeltranslation.translator import (
    register,
    TranslationOptions
)

from .models import Injury


@register(Injury)
class InjuryTranslationOptions(TranslationOptions):

    fields = ('name', )
    empty_values = {'name': None}
    # because our name is not nullable, default will give value ''
    # but None will be accessable


