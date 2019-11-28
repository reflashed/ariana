import os
import csv
import random

import textstat
from google.cloud import texttospeech
from pydub import AudioSegment

def make_output_dirs():
    if not os.path.isdir('out'):
        os.mkdir('out')

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

def gen_lyrics_text():
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
    return song_lyrics

def gen_lyrics_audio(song_id, song_lyrics):
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    except:
        print('Error ==> You must set the env variable GOOGLE_APPLICATION_CREDENTIALS')
        exit()

    print('Generating audio from Google TTS... ', end='', flush=True)
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
    print('done')

    lyrics_audio = 'out/lyrics-{}.mp3'.format(song_id)
    lyrics_text = 'out/lyrics-{}.txt'.format(song_id)

    with open(lyrics_audio, 'wb') as out:
        print('Saving lyrics audio to {}... '.format(lyrics_audio), end='', flush=True)
        out.write(response.audio_content)
        print('done')

    with open(lyrics_text, 'w') as f:
        print('Saving lyrics text to {}... '.format(lyrics_text), end='', flush=True)
        f.write(song_lyrics)
        print('done')

    return lyrics_audio

def concat_audio(song_id, lyrics_audio, background_audio):
    fade_dur = 2000

    lyrics = AudioSegment.from_file(lyrics_audio)
    background = AudioSegment.from_mp3(background_audio)[46000:len(lyrics) + 46000 + fade_dur * 2].fade_in(fade_dur)
    background = background.fade_out(fade_dur)
    lyrics = AudioSegment.silent(duration=fade_dur) + lyrics
    song = background.overlay(lyrics)

    output_song_path = 'out/song-{}.mp3'.format(song_id)

    print('Saving song to ' + output_song_path + '... ', end='', flush=True)
    song.export(output_song_path, format="mp3")
    print('done')

make_output_dirs()
song_id = random.randrange(1, 9999999999)
song_lyrics = gen_lyrics_text()
lyrics_audio = gen_lyrics_audio(song_id, song_lyrics)
song_path = concat_audio(song_id, lyrics_audio, 'media/7-rings.mp3')
