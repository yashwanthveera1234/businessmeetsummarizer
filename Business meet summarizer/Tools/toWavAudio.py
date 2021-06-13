from os import path
from pydub import AudioSegment

# files                                                                         
src = path.abspath("testAudio.mp3")
dst = path.abspath("test4.wav")

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

# def toWav(filePath):
#     from pydub import AudioSegment
#     if filePath.split('.')[-1] == 'mp3':
#         sound = AudioSegment.from_mp3(filePath)
#         filePath = sound.export(filePath.split('.')[0], format = 'wav')
#     return filePath