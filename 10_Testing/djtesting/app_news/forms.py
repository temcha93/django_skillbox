from django import forms
from .models import News, Comment
from .fields import ListTextWidget
from django.utils.translation import gettext_lazy as _


class NewsForm(forms.ModelForm):
    tag = forms.CharField(required=False, label=_('Tag'))
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 required=False, label=_('Pictures'))

    def __init__(self, *args, **kwargs):
        data_list = kwargs.pop('data_list', None)
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['tag'].widget = ListTextWidget(data_list=data_list, name='tag')

    class Meta:
        model = News
        fields = ['title', 'description', 'published_at', 'fl_ready_to_publish']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'comment']


class UploadCSVFileForm(forms.Form):
    file = forms.FileField()
