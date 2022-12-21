from django import forms
from .models import Post, PostImage

goods_type = [
    ('griptok', '그립톡'), 
    ('mugcub', '머그컵'),
    ('keyring', '키링'),
    ('tshirt', '티셔츠'),   
    ('phonecase', '핸드폰 케이스'),
]
class PostForm(forms.ModelForm):
    Board_gtype = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=goods_type,
        error_messages={'required':'굿즈 종류를 선택해주세요.'},
        required=True
    )
    
    class Meta:
        model = Post
        fields = ['Board_share', 'Board_gtype', 'Board_title', 'Board_content']
        widgets = {
            'Board_share' : forms.RadioSelect(),
            'Board_title' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':"제목을 입력해주세요.",
                'style':'border: none;'
            }),
            'Board_content' : forms.Textarea(attrs={
                'class':'form-control',
                'rows':'10',
                'placeholder':"내용을 입력해주세요.",
                'style':'height: 300px; border: none;resize: none;'
            }),
        }
        
class Post_ImageForm(forms.ModelForm):
    Board_image = forms.ImageField(
            label='image',
            widget=forms.ClearableFileInput(
                attrs={
                    'onchange':"addFile(this)",
                    'multiple': True,
                }
            )
        )
    
    class Meta:
        model = PostImage
        fields = ['Board_image',]
        