from django import forms
from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image', 'message']
        widgets = {
            'image': forms.FileInput(attrs={
                'type': 'file',
                'id': 'image',
                'onchange': 'setThumbnail(event)',
                'style': 'margin-left: 200px'
            }),
        }