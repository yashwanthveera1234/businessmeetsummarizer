def recognizeAudio(audioObj):
    import speech_recognition as sr
    import io

    HOUNDIFY_CLIENT_ID = "wmSLC3HqKCVq_SvznelYMA=="  # Houndify client IDs are Base64-encoded strings
    HOUNDIFY_CLIENT_KEY= "0jmIzgvPIKG_zJTrFZp0ITAxSsvWDY12pTr-zNqCniAVbhR02uFiubqY3CqgkKETPbrI6Wg8T5MzRKFAYOa0SA=="  # Houndify

    r = sr.Recognizer()

    b = io.BytesIO()
    audioObj.export(b, bitrate='192k', format='wav')
    b.seek(0)
    with sr.AudioFile(b) as source:
        audio = r.listen(source)

    try:
        return r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
    except sr.UnknownValueError:
        return "<<Could not understand audio>>"
    except sr.RequestError as e:
        return "<<Error Occured : {0}>>".format(e)


def toText(filePath):
    import os
    
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    
    # # constants (or) settings
    MAX_LEN = 60000
    FILE_PATH = filePath
    
    # # # # Logic Starts Here
    audio = AudioSegment.from_wav(FILE_PATH)
    
    # creating chunks by splitting at silence
    audio_chunks = split_on_silence(audio, min_silence_len = 500, silence_thresh = audio.dBFS - 16)
    
    # modifying each chunk. Adding 10 milli sec silence at both ends of chunk
    rawChunks = []
    for chunk in audio_chunks:
        silent_chunk = AudioSegment.silent(duration=10)
        tempChunk = silent_chunk+chunk+silent_chunk
        rawChunks.append(tempChunk)
    
    # making 1min audio chunks and saving as text...
    recognizedText = ''
    
    audioObj = None
    for chunk in rawChunks:
        if audioObj != None:
            if len(audioObj) + len(chunk) < MAX_LEN:
                audioObj += chunk
            else:
                recognizedText += recognizeAudio(audioObj)
                audioObj = chunk
        else:
            audioObj = chunk
    if audioObj != None:
        recognizedText += recognizeAudio(audioObj)
    
    return recognizedText