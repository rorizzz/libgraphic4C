# Need to deploy the Whisperx environment first, refer to: https://github.com/m-bain/whisperX

import whisperx
import gc
import torch
import sys
import os

device = "cuda"
folder_path_to_process = "D:/miniconda3/localwhisperx/VCTK_Corpus/wave/p225"
output_folder_path = 'D:/miniconda3/localwhisperx/alignment_by_whisperx/p225_output'

batch_size = 16  # reduce if low on GPU mem
compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)

# 1. Load the models outside of the loop to save time.
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
model_a, metadata = None, None

# iterate through the folder
for filename in os.listdir(folder_path_to_process):
    if filename.endswith(".flac"):
        audio_file = os.path.join(folder_path_to_process, filename)

        # Transcribe with original whisper (batched)
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)

        # Only load alignment model once for efficiency
        if model_a is None and metadata is None:
            model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

        # Align whisper output
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        # Save result to txt file
        name_without_extension = os.path.splitext(filename)[0]
        txt_filename = name_without_extension + '.txt'
        full_path = os.path.join(output_folder_path, txt_filename)

        original_stdout = sys.stdout
        sys.stdout = open(full_path, 'w', encoding='utf-8')
        print(result["segments"])
        sys.stdout.close()
        sys.stdout = original_stdout

        # Optional: clear GPU resources in the loop if needed
        gc.collect()
        torch.cuda.empty_cache()
