from gtts import gTTS
def convert_text_to_audio(text,name):
    audio = gTTS(text)
    audio.save(name)

convert_text_to_audio("Mask",'mask.mp3')
convert_text_to_audio("No Mask",'no_mask.mp3')

