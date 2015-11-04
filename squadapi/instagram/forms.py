from django import forms

from .models import User
from .collect import find_user, get_user


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

        user = get_user(user['id'])

        self.cleaned_data['name'] = user['full_name']
        self.cleaned_data['user_id'] = user['id']
        self.cleaned_data['username'] = user['username']
        self.cleaned_data['followers'] = user['counts']['followed_by']
        self.cleaned_data['image_url'] = user['profile_picture']

    def save(self, **kwargs):
        user = super(UserAdminForm, self).save(commit=False)
        user.name = self.cleaned_data['name']
        user.user_id = self.cleaned_data['user_id']
        user.followers = self.cleaned_data['followers']
        user.image_url = self.cleaned_data['image_url']

        if kwargs.get('commit'):
            user.save()

        return user
