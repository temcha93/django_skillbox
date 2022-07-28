from django import forms
from .models import News, Comment


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ('activity', )


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('news_comment', )
