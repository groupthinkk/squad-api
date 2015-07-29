from django import forms

from .models import User
from .collect import find_user


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        super(UserAdminForm, self).clean()

        username = self.cleaned_data['username']

        user = find_user(username)

        if not user:
            raise forms.ValidationError(
                'No user found with username "{0}".'.format(username)
            )

        self.cleaned_data['user_id'] = user['id']

    def save(self, **kwargs):
        user = super(UserAdminForm, self).save(commit=False)
        user.user_id = self.cleaned_data['user_id']

        if kwargs.get('commit'):
            user.save()

        return user
