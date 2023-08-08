from pydub import AudioSegment
import random
import os

# set the path for read and output (audio and alignment respectively)
folder_path_audio = 'D:/miniconda3/localwhisperx/VCTK_Corpus/wave/p225'
output_folder_path_audio = 'D:/miniconda3/localwhisperx/try_audio/p225'
folder_path_annotation = 'D:/miniconda3/localwhisperx/p225_output'
output_folder_path_annotation = 'D:/miniconda3/localwhisperx/try_ano/p225'


for filename in os.listdir(folder_path_audio):  # iterate through all audios from a speaker
    audio_path = os.path.join(folder_path_audio, filename)
    txt_path = os.path.join(folder_path_annotation, filename.replace('.flac', '.txt'))

    audio = AudioSegment.from_file(audio_path, format="flac")

    # read the word alignment created by whisperx
    with open(txt_path, 'r') as file:
        alignment_data = eval(file.read())

    word_to_pause = random.choice(alignment_data[0]['words'])  # randomly choose a word and add a pause after it
    start_time = round(word_to_pause['start'] * 1000, 3)
    end_time = round(word_to_pause['end'] * 1000, 3)

    # insert the silence
    silence_duration = 1500  # set the long_puase = 1.5s <can be changed later as needed >
    silence_segement = AudioSegment.silent(duration=silence_duration)

    # repeated_segment = audio[start_time:end_time] + silence_segement + audio[start_time:end_time]
    new_audio = audio[:end_time] + silence_segement + audio[end_time:]

    new_audio_path = os.path.join(output_folder_path_audio, filename)
    new_audio.export(new_audio_path, format="flac")

    key = 'type'
    alignment_data[0]['end'] += (silence_duration / 1000)
    alignment_data[0]['end'] = round(alignment_data[0]['end'], 3)

    i = 1
    for word in alignment_data[0]['words']:
        word[key] = None

        if word['start'] * 1000 < start_time:
            i += 1

        if word['start'] * 1000 > end_time:
            word['start'] += (silence_duration / 1000)
            word['start'] = round(word['start'], 3)
            word['end'] += (silence_duration / 1000)
            word['end'] = round(word['end'], 3)

    for entry in alignment_data:
        for word_data in entry['words']:
            word_data.pop('score', None)

    new_word_data = {'word': None, 'start': (end_time/1000), 'end': (end_time + silence_duration)/1000, 'type': 'long_pause'}
    alignment_data[0]['words'].insert(i, new_word_data)

    new_txt_path = os.path.join(output_folder_path_annotation, filename.replace('.flac', '.txt'))
    with open(new_txt_path, 'w', encoding='utf-8') as file:
        file.write(str(alignment_data))

    print(f'Finished processing: {filename}')
