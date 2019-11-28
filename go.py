import csv
import random
import textstat
import pyttsx3

from google.cloud import texttospeech
from pydub import AudioSegment

engine = pyttsx3.init()

def load_verbs():
    verbs = []

    with open('data/verbs.csv', 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            verb = row[0]
            num_syllables = textstat.syllable_count(verb, lang='en_US')

            if num_syllables == 1:
                if '-' not in verb:
                    if '_' not in verb:
                        verbs.append(verb)

    return verbs

def gen_tuples(num_tuples):
    verbs = load_verbs()
    tuples = []

    for i in range(num_tuples):
        verb_1 = random.choice(verbs)
        verb_2 = random.choice(verbs)

        tuples.append([verb_1, verb_2])

    return tuples

subjects = ['I', 'You']
verb_tuples = gen_tuples(50)

song = ''

for i, verb_tuple in enumerate(verb_tuples):
    subject_1 = random.choice(subjects)
    subject_2 = random.choice(subjects)

    if subject_2 != 'I':
        subject_2 = str.lower(subject_2)

    verb_1, verb_2 = verb_tuple
    phrase = '{} {} it, {} {} it.'.format(subject_1, verb_1, subject_2, verb_2)

    song += phrase + '\n'

song_lyrics = song[:-1] # get rid of last \n

def gen_audio(song_id, song_lyrics):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=song_lyrics)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3
    )

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    filename = 'phrases/song-{}.mp3'.format(song_id)

    with open(filename, 'wb') as out:
        out.write(response.audio_content)

    print('Audio content written to file "{}"'.format(filename))
    return filename

song_id = random.randrange(1, 9999999999)
# lyrics_audio = 'phrases/song-3655327275.mp3'
lyrics_audio = gen_audio(song_id, song_lyrics)

def concat_audio(song_id, lyrics_audio, background_audio):
    fade_dur = 2000

    lyrics = AudioSegment.from_file(lyrics_audio)
    background = AudioSegment.from_mp3(background_audio)[46000:len(lyrics) + 46000 + fade_dur * 2].fade_in(fade_dur)
    background = background.fade_out(fade_dur)
    lyrics = AudioSegment.silent(duration=fade_dur) + lyrics
    song = background.overlay(lyrics)

    # background = background[:len(lyrics) + fade_dur * 3]

    output_song_path = 'songs/song-{}.mp3'.format(song_id)
    song.export(output_song_path, format="mp3")
    print(output_song_path)

song_path = concat_audio(song_id, lyrics_audio, 'media/7-rings.mp3')
