from pydub import AudioSegment
import random
import os

# set the path for read and output (audio and alignment respectively)
folder_path_audio = 'D:/miniconda3/localwhisperx/VCTK_Corpus/wave/p225'
output_folder_path_audio = 'D:/miniconda3/localwhisperx/try_audio/p225'
folder_path_annotation = 'D:/miniconda3/localwhisperx/alignment_by_whisperx/p225_output'
output_folder_path_annotation = 'D:/miniconda3/localwhisperx/try_ano/p225'


for filename in os.listdir(folder_path_audio):  # iterate through all audios from a speaker
    audio_path = os.path.join(folder_path_audio, filename)
    txt_path = os.path.join(folder_path_annotation, filename.replace('.flac', '.txt'))

    audio = AudioSegment.from_file(audio_path, format="flac")

    # read the word alignment created by whisperx
    with open(txt_path, 'r') as file:
        alignment_data = eval(file.read())

    word_to_remove = random.choice(alignment_data[0]['words'])

    # retain 3 decimal places to prevent errors from accumulating
    start_time = round(word_to_remove['start'] * 1000, 3)
    end_time = round(word_to_remove['end'] * 1000, 3)
    duration_of_removal = round(end_time - start_time, 3)

    # compose the new audio
    new_audio = audio[:start_time] + audio[end_time:]

    # save the modified audio to the destination path
    new_audio_path = os.path.join(output_folder_path_audio, filename)
    new_audio.export(new_audio_path, format="flac")

    # add a key
    key = 'type'

    # update the alignmnet
    alignment_data[0]['end'] -= round((duration_of_removal / 1000), 3)
    alignment_data[0]['end'] = round(alignment_data[0]['end'], 3)

    for word in alignment_data[0]['words']:
        if word == word_to_remove:
            word[key] = 'missing'
            word['start'] = round(start_time/1000, 3)
            word['end'] = round(start_time/1000, 3)
        else:
            word[key] = None

        # the 'start' and 'end' keys of words after the repeated word should be moved forward
        if word['start'] * 1000 > end_time:
            word['start'] -= duration_of_removal / 1000
            word['start'] = round(word['start'], 3)
            word['end'] -= duration_of_removal / 1000
            word['end'] = round(word['end'], 3)

    for entry in alignment_data:
        for word_data in entry['words']:
            word_data.pop('score', None)

    new_txt_path = os.path.join(output_folder_path_annotation, filename.replace('.flac', '.txt'))
    with open(new_txt_path, 'w', encoding='utf-8') as file:
        file.write(str(alignment_data))

    print(f'Finished processing: {filename}')
