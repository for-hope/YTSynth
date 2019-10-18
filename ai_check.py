import speech_recognition as sr
from pydub import AudioSegment


r = sr.Recognizer()
src = 'mp3_results/challenge.mp3'
dst = 'mp3_results/challenge.wav'
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

with sr.AudioFile(dst) as source:
    audio = r.listen(source)

try:  
    print("Sphinx thinks you said '" + r.recognize_sphinx(audio) + "'")  
except sr.UnknownValueError:  
   print("Sphinx could not understand audio")  
except sr.RequestError as e:  
   print("Sphinx error; {0}".format(e)) 