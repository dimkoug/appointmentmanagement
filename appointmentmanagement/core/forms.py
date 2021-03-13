from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from adminsortable2.admin import CustomInlineFormSet
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from sorl.thumbnail import get_thumbnail


def unique_field_formset(field_name):
    from django.forms.models import BaseInlineFormSet
    from adminsortable2.admin import CustomInlineFormSet
    class UniqueFieldFormSet(CustomInlineFormSet, BaseInlineFormSet):
        def clean(self):
            if any(self.errors):
                # Don't bother validating the formset unless each form is valid on its own
                return
            values = set()
            for form in self.forms:
                if form.cleaned_data:
                    value = form.cleaned_data[field_name]
                    if value in values:
                        raise forms.ValidationError('Duplicate values for "%s" are not allowed.' % field_name)
                    values.add(value)
    return UniqueFieldFormSet


class ShortableFormSet(CustomInlineFormSet, BaseInlineFormSet):
    pass


class SlugValidator:
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        existing_objects = self.Meta.model.objects.filter(slug=slug)
        if self.instance:
            existing_objects = existing_objects.exclude(
                pk=self.instance.pk)
        if existing_objects:
            raise ValidationError('The slug already exists')
        return slug



class AdminImageWidget(AdminFileWidget):
  def render(self, name, value, attrs=None, renderer=None):
    output = []
    if value and getattr(value, "url", None):
      t = get_thumbnail(value,'80x80')
      output.append('<img src="{}">'.format(t.url))
    output.append(super(AdminImageWidget, self).render(name, value, attrs))
    return format_html(u''.join(output))


class BootstrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
