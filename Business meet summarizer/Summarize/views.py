from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse

from .decorators import authenticatedUser

from .forms import StrAudioDataForm, UploadAudioFileForm

from .models import AudioSummarizeModel

from Tools.sendMails import sendEmails
from Tools.summarizeText import toSummarize
from Tools.recognizeText import toText
from Tools.punctuate import punctuateFunc




@authenticatedUser
def recordView(HttpRequest):
    if HttpRequest.method == 'POST':
        form = StrAudioDataForm(HttpRequest.POST, None)
        if form.is_valid():

            import base64 # to decode base64 encoded string
            from django.core.files.base import ContentFile # to save the decoded string as a file

            base64EncStr = form.cleaned_data.get("audioData") # returns data. Here base64 encoded string.
            decodedData = base64.b64decode(base64EncStr) # decodes the base64 encoded string.
            r = AudioSummarizeModel(audioName = form.cleaned_data.get('audioName'),audioDescription = form.cleaned_data.get('audioDescription') ,audioFile = ContentFile(decodedData, 'record.wav'), user=User.objects.get(pk=HttpRequest.user.id))
            # ContentFile() takes the decoded base64 string and a default file name. It returns a file object which is saved in the database.
            r.save() # saves record in database.
            return redirect('Summarize:summarizeHomeView')
    else:
        form = StrAudioDataForm()
    context = {
        'form' : form,
    }
    return render(HttpRequest, 'record.html', context)




@authenticatedUser
def uploadView(HttpRequest):
    if HttpRequest.method == 'POST':
        form = UploadAudioFileForm(HttpRequest.POST, HttpRequest.FILES or None)
        if form.is_valid():
            if not HttpRequest.FILES['uploadFile'].name.split('.')[-1] in ['wav']:
                messages.warning(HttpRequest, 'Unsupported File Uploaded. We Only Support WAV format.')
            else:
                r = AudioSummarizeModel(audioName = form.cleaned_data.get('audioName'),audioDescription = form.cleaned_data.get('audioDescription') ,audioFile = form.cleaned_data.get('uploadFile'), user=User.objects.get(pk=HttpRequest.user.id))
                r.save()
                return redirect('Summarize:summarizeHomeView')
    else:
        form = UploadAudioFileForm()
    context = {
        'form' : form,
    }
    return render(HttpRequest, 'upload.html', context)




@authenticatedUser
def summarizeHomeView(HttpRequest):
    user = User.objects.get(pk = HttpRequest.user.id)
    audioSummarizeObjs = AudioSummarizeModel.objects.filter(user = user).last()
    if audioSummarizeObjs == None:
        messages.warning(HttpRequest, "You haven't had any data.  Please Upload (or) Record Audio.")
        return redirect('Summarize:uploadView')
    else:
        context = {
            'audioObj' : audioSummarizeObjs,
        }
    return render(HttpRequest, 'summarizeHome.html', context)




def delAudioView(request, id):
    audioObj = AudioSummarizeModel.objects.get(id = id)
    audioObj.delete()
    messages.info(request, 'Audio is Deleted!')
    return redirect('Summarize:summarizeHomeView')




@authenticatedUser
def detailsView(HttpRequest, id):
    audioObj = AudioSummarizeModel.objects.get(id = id)
    context = {
        'audioObj' : audioObj,
    }
    return render(HttpRequest, 'details.html', context)




@authenticatedUser
def recognizeTextView(HttpRequest, id):
    audioObj = AudioSummarizeModel.objects.get(id = id)
    if audioObj.isRecognized :
        messages.info(HttpRequest, 'Already Converted to Text.')
    else:
        audioObj.recognizedText = punctuateFunc(toText(audioObj.audioFile))
        audioObj.isRecognized = True
        audioObj.save(update_fields = ['recognizedText', 'isRecognized'])
    context = {
        'audioObj' : audioObj,
    }
    return render(HttpRequest, 'recognize.html', context)




@authenticatedUser
def summarizeTextView(HttpRequest, id):
    audioObj = AudioSummarizeModel.objects.get(id = id)
    if audioObj.isRecognized:
        if audioObj.isSummarized :
            messages.info(HttpRequest, 'Already Summarized.')
        else:
            audioObj.summarizedText = toSummarize(audioObj.recognizedText)
            audioObj.isSummarized = True
            audioObj.save(update_fields = ['summarizedText', 'isSummarized'])
    else:
        messages.info(HttpRequest, 'Unable to summarize audio. Did you converted audio to text ?')
    context = {
        'audioObj':audioObj,
    }
    return render(HttpRequest, 'summarize.html', context)




@authenticatedUser
def sendMailsView(HttpRequest, id):
    audioObj = AudioSummarizeModel.objects.get(id = id)
    if audioObj.isSummarized:
        if audioObj.isMailSent:
            messages.info(HttpRequest, 'E-Mails are already sent.')
        else:
            from Users.models import MailReceiverModel
            mailReceiverObj = list(MailReceiverModel.objects.filter(user = User.objects.get(pk = HttpRequest.user.id)).values_list('email'))
            emailsList = [str(item[0]) for item in mailReceiverObj]
            header = f'{audioObj.audioName} - Summary'
            htmlContent = f'''\
<html>
    <body>
        <table>
            <tr>
                <td><strong>Meeting Host : </strong></td>
                <td>{HttpRequest.user}</td>
            </tr>
            <tr>
                <td><strong>Meeting Name : </strong></td>
                <td>{audioObj.audioName}</td>
            </tr>
            <tr>
                <td><strong>Meeting Description : </strong></td>
                <td>{audioObj.audioDescription}</td>
            </tr>
        </table>
        <h4>Meeting Summary</h4>
        <p>{audioObj.summarizedText}</p>
    </body>
</html>
            '''
            sendEmails(header, htmlContent, emailsList)
            audioObj.isMailSent = True
            audioObj.save(update_fields = ['isMailSent'])
    else:
        messages.info(HttpRequest, 'Unable to Send E-Mails. Did you summarized ?')
    return render(HttpRequest, 'emails.html', {})


