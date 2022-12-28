from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model
from accounts.models import Account
from django.contrib.auth.hashers import check_password

# 회원 가입 폼
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')
    
    class Meta:
        model = Account
        fields = ('username', 'name', 'nickname', 'email', 'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={
                'readonly': True,
                'style': 'display: none;'})
        }
 
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"이미 사용중인 이름입니다.")
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"이미 사용중인 이메일입니다.")
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].lower()
        try:
            account = Account.objects.get(nickname=nickname)
        except Exception as e:
            return nickname
        raise forms.ValidationError(f"이미 사용중인 별명입니다.")
  
 
 
 
# 로그인 인증 폼
class AccountAuthForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
    class Meta:
        model = Account
        fields = ('username', 'password')
 
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("로그인이 실패했습니다.")


# 회원정보 수정 폼
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'name', 'nickname', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'disabled',
                'readonly': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'disabled',
                'readonly': True
            }),
        }
        
# 비빌번호 변경 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
        
        
# 회원탈퇴 비밀번호 확인 폼
class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
    )
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
