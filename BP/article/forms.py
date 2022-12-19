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
        error_messages={'required':'굿즈 종류를 선택해주세요.'}
    )
    
    class Meta:
        model = Post
        fields = ['Board_share', 'Board_gtype', 'Board_title', 'Board_content']
        
class Post_ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['Board_image',]