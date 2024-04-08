from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from midi2audio import FluidSynth
from django.core.files import File
from django.core.files.storage import default_storage
from music21 import instrument, note, stream  # For music21
import random
from django.http import JsonResponse
import midi2audio
# from midi2audio import FluidSynth


import os
import json
import numpy as np
import tensorflow.keras as keras
import music21 as m21

@csrf_exempt


def sendMidi(request) :
    req = json.loads(request.body)
    noOfOutputs = int(req['no'])
    temperature = float(req['temp'])
    length = int(req['length'])
    genre = req['genre']

    # Check if seed is provided?
    isSeed = False

    if "seed" in req:
        print("Seed is provided")
        isSeed = True
        seedInput = req['seed']
        
    # seedInput = req['seed']
    seedPoolPop = ['67 _ _ _ 64 64 62', '64 _ _ _ 60 _ r _ 67', '64 _ 67 _ 67 _ 65 _', '62 _ 64 _ 65 _ 67 _', '60 _ 67 _ 67 _ 67 _ 69', '64 _ _ _ 69 _ 67 _ _', '60 _ _ _ 55 _ 55 _','55 _ 55 _ 55 _ 55 _ _ _ 60', '64 _ 62 _ 62 _ 64 _ 60 _ 62', '69 _ 67 _ _ _ 64 _ r _', '65 65 67 _ 65 _ 67', '64 62 _ 62 _ 62 _ 64']
    seedPoolBallad = ['64 _ 62 _ 60 _ r _','65 65 62 _ 62 62 64','67 _ 72 _ 71 _ 69 _ 69','64 _ 67 _ _ _ 64 _ 67','72 _ 71 _ 69 _ 67 _ _','71 _ 72 _ 74 _ _ _ 72','55 _ _ _ 60 _ _ _ 59 _ _ _ 57']
    seedPoolBoehme = ['64 _ _ _ _ _ 64 _ 62 _','52 _ 52 _ _ _ 60 _ 60','62 _ 60 _ 60 _ 65 _ _ _ 64','71 _ _ _ 69 _ _ _ 67','55 _ 60 _ 59 _ _ 57 55','62 60 59 57 55 55 _ 57','65 _ 74 _ 72 _ 71 _']
    seedPoolChorale = ['53 _ 57 _ 55 _ _ _ 60','60 _ r _ r _ _ _ 60 62','60 62 _ _ _ 55 _ _ _ 65','69 _ 71 _ 72 _','55 _ _ _ 60 _ 59 _ 57','81 _ r _ 81 _ 79 _ 81 79']
    model_path=f"C:/Users/gaura/OneDrive/Desktop/python/testrun/static/models/{genre}_model.h5"
    # print("model path ====="model_path)
    # if len(seedInput) == 0:
    MAPPING_PATH = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/static/models/mapping.json'
    # if isSeed == False:
    #     print("No seed")
    #     model_path=f"C:/Users/gaura/OneDrive/Desktop/python/testrun/static/fles/{genre}_model.h5"
    #     MAPPING_PATH = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/static/fles/{genre}_mapping.json'

    # else:
        # MAPPING_PATH = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/static/fles/mapping.json'

    # MAPPING_PATH = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/static/fles/{genre}_mapping.json'

    SEQUENCE_LENGTH = 64
    respData = {}
    
    model = keras.models.load_model(model_path)
    
    # print(no)

    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    start_symbols = ["/"] * SEQUENCE_LENGTH

    def generate_melody(seed, num_steps, max_sequence_length, temperature):

        seed = seed.split()
        melody = seed
        seed = start_symbols + seed

        seed = [mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            seed = seed[-max_sequence_length:]

            # one-hot encode the seed
            onehot_seed = keras.utils.to_categorical(seed, num_classes=len(mappings))
            onehot_seed = onehot_seed[np.newaxis, ...]

            # make a prediction
            probabilities = model.predict(onehot_seed)[0]
            output_int = sample_with_temperature(probabilities, temperature)

            # update seed
            seed.append(output_int)

            output_symbol = [k for k, v in mappings.items() if v == output_int][0]

            if output_symbol == "/":
                # break
                continue
            
            #Setting length of generated sequence
            if len(melody) > length:
                break
            
            # update melody
            melody.append(output_symbol)

        return melody


    def sample_with_temperature(probabilites, temperature):

        predictions = np.log(probabilites) / temperature
        probabilites = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilites)) # [0, 1, 2, 3]
        index = np.random.choice(choices, p=probabilites)

        return index

    # oks = ''
    def save_melody(melody, num, step_duration=0.25, format="midi", file_name="mel.mid"):

        stream = m21.stream.Stream()

        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):

            if symbol != "_" or i + 1 == len(melody):

                if start_symbol is not None:

                    quarter_length_duration = step_duration * step_counter # 0.25 * 4 = 1

                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength=quarter_length_duration)

                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)

                    stream.append(m21_event)

                    step_counter = 1

                start_symbol = symbol

            else:
                step_counter += 1
        
        # paths
        temppath = random.randrange(1,10) 
        # tt = os.path.join('/meida',temppath)
        savePath =  f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/{temppath}.mid'
        savePathWav = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/{temppath}.wav'
        # savePath =  f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/6.mid'
        # savePathWav = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/4.wav'
        # savePathWav1 = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/8general.wav'
        # savePathWav2 = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/8creative.wav'
        # savePathWav3 = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/8muse.wav'
        # savePathMid = f'C:/Users/gaura/OneDrive/Desktop/python/testrun/media/8.mid'
        respPath = f'/media/{temppath}.wav'
        
        respData[f'path{num}'] = respPath
        json_data = json.dumps(respData)

        # write the m21 stream to a midi file
        stream.write(format,savePath)
                
        def midi_to_wav(midi_file, soundfont, save):
            os.system(f'fluidsynth -ni {soundfont} {midi_file} -F {save} -r 44100')

    # Converting to wav
        # soundfont1 = r'C:/Users/gaura/OneDrive/Desktop\python\GeneralUser\GeneralUser.sf2'
        # soundfont2 = r'C:/Users/gaura/OneDrive/Desktop\python\CREATIVE_8MBGM.sf2'
        soundfont = r'C:\Users\gaura\OneDrive\Desktop\python\MuseScore.sf2'
        # midi_to_mp3(savePath, soundfont1, savePathWav1)
        # midi_to_mp3(savePath, soundfont2, savePathWav2)
        midi_to_wav(savePath, soundfont, savePathWav)
        return json_data
    
    num = 0
    selectedSeedPool = seedPoolPop
    if(genre == 'ballad'):
        selectedSeedPool = seedPoolBallad
    elif(genre == 'chorale'):
        selectedSeedPool = seedPoolChorale
    else:
        selectedSeedPool = seedPoolBoehme

    # print("selected pool ==== ", selectedSeedPool)   
    for x in range(noOfOutputs):
        seedIndex = random.randrange(0,len(selectedSeedPool)-1)
        num = num+1
        # if len(seedInput) == 0:
        if isSeed:
            seed = seedInput
        else:
            seed = selectedSeedPool[seedIndex]
        # else:
        #     seed = seedInput
        
        print(seed)
        # seed2 = "67 _ _ _ _ _ 65 _ 64 _ 62 _ 60 _ _ _"
        melody = generate_melody(seed, 900, SEQUENCE_LENGTH, temperature)
        json_data = save_melody(melody,num)
    

    return JsonResponse(json_data,safe=False)