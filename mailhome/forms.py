from django import forms
from froala_editor.widgets import FroalaEditor
from .models import MailSend

class PageForm(forms.ModelForm):
  content = forms.CharField(widget=FroalaEditor)

  class Meta:
    model = MailSend
    fields = ('content', )