from django import forms

from contact.models import MailToAdmin


class MailToAdminForm(forms.ModelForm):

    class Meta:
        model = MailToAdmin
        fields = ('username', 'from_mail', 'text')
