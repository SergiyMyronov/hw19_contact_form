from contact.models import MailToAdmin

from django import forms


class MailToAdminForm(forms.ModelForm):

    class Meta:
        model = MailToAdmin
        fields = ('username', 'from_mail', 'text')
