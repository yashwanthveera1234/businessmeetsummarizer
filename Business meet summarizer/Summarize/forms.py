from django import forms

class StrAudioDataForm(forms.Form): # Using django's forms. Not modelforms
    audioName = forms.CharField(label='Audio Name', max_length = 255)
    audioDescription = forms.CharField(label='Audio Description', max_length = 1024)
    audioData = forms.CharField(label = '', widget=forms.Textarea(attrs={'id':'base_64_str','hidden':True})) # id='base_64_str' is used in 'base.js' file.

class UploadAudioFileForm(forms.Form):
    audioName = forms.CharField(label='Audio Name', max_length = 255)
    audioDescription = forms.CharField(label='Audio Description', max_length = 1024)
    uploadFile = forms.FileField(label='Upload Audio File')
