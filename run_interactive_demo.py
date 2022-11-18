import os
import sys
import warnings

import torch

from InferenceInterfaces.FastSpeech2Interface import InferenceFastSpeech2

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=UserWarning)
    available_models = os.listdir("Models")
    available_fastspeech_models = list()
    for model in available_models:
        if model.startswith("FastSpeech2_"):
            available_fastspeech_models.append(model.lstrip("FastSpeech_2"))
    model_id = input("Which model do you want? \nCurrently supported are: {}\n".format(
        "".join("\n\t- {}".format(key) for key in available_fastspeech_models)))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = InferenceFastSpeech2(device=device, model_name=model_id)
    tts.set_language(lang_id=input("Which Language?\n"))
    while True:
        speaker_reference = input(
            "Path to a reference .wav of a speaker? \nPress enter without typing anything to use the default voice\n").strip()
        # generate the out path
        fpath_without_ext = os.path.splitext(str(speaker_reference))[0]
        speaker_name = os.path.normpath(fpath_without_ext).split(os.sep)[-1]
        filename = f"out_audios/{speaker_name}_syn.wav"

        if speaker_reference != "":
            if os.path.exists(speaker_reference):
                tts.set_utterance_embedding(speaker_reference)
            else:
                print(
                    f"File {speaker_reference} could not be found, please check for typos and re-run. Using default for now.")

        text = input("\nWhat should I say? (or 'exit')\n")
        if text == "exit":
            sys.exit()
        tts.read_aloud(text,
                       filename,
                       view=True,
                       blocking=False,
                       duration_scaling_factor=1.0,
                       energy_variance_scale=1.0,
                       pitch_variance_scale=1.0)
