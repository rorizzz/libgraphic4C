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

    word_to_repeat = random.choice(alignment_data[0]['words'])   # choose the repeat word randomly

    # retain 3 decimal places to prevent errors from accumulating
    start_time = round(word_to_repeat['start'] * 1000, 3)
    end_time = round(word_to_repeat['end'] * 1000, 3)
    duration_of_repetition = end_time - start_time

    # insert a short silence
    silence_duration = int(duration_of_repetition*0.7)
    silence_segement = AudioSegment.silent(duration=silence_duration)

    # compose the new audio
    repeated_segment = audio[start_time:end_time] + silence_segement + audio[start_time:end_time]
    new_audio = audio[:start_time] + repeated_segment + audio[end_time:]

    # save the modified audio to the destination path
    new_audio_path = os.path.join(output_folder_path_audio, filename)
    new_audio.export(new_audio_path, format="flac")

    # add a new key
    key = 'type'

    # update the alignment
    alignment_data[0]['end'] += ((duration_of_repetition + silence_duration) / 1000)
    alignment_data[0]['end'] = round(alignment_data[0]['end'], 3)

    i = 1  # store the location of repeat word
    for word in alignment_data[0]['words']:
        if word == word_to_repeat:
            word[key] = 'repetition'
        else:
            word[key] = None

        if word['start'] * 1000 < start_time:
            i += 1

        # the 'start' and 'end' keys of words after the repeated word should be shifted
        if word['start'] * 1000 > end_time:
            word['start'] += ((duration_of_repetition + silence_duration) / 1000)
            word['start'] = round(word['start'], 3)
            word['end'] += ((duration_of_repetition + silence_duration) / 1000)
            word['end'] = round(word['end'], 3)

    # delete the 'score' key in the raw alignments created by whisperx 
    for entry in alignment_data:
        for word_data in entry['words']:
            word_data.pop('score', None)

    # insert the repeated word in alignment
    new_word_data = {'word': word_to_repeat['word'], 'start': (end_time + silence_duration)/1000, 'end': (end_time + silence_duration + duration_of_repetition)/1000, 'type': 'repetition'}
    alignment_data[0]['words'].insert(i, new_word_data)

    new_txt_path = os.path.join(output_folder_path_annotation, filename.replace('.flac', '.txt'))
    with open(new_txt_path, 'w', encoding='utf-8') as file:
        file.write(str(alignment_data))

    print(f'Finished processing: {filename}')
