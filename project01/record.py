import re
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import queue
import os, shutil
from underthesea import sent_tokenize

q = queue.Queue()
category = ['thoi_su', 'goc_nhin', 'the_gioi', 'kinh_doanh', 'giai_tri', 'the_thao', 'phap_luat', 'giao_duc', 'suc_khoe', 'doi_song',
            'du_lich', 'khoa_hoc', 'so_hoa', 'xe', 'y_kien', 'tam_su']

recordingCat = category[12]
pathToData = 'data/' + recordingCat + '/'

folder = pathToData
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     try:
#         if os.path.isfile(file_path) or os.path.islink(file_path):
#             os.unlink(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     except Exception as e:
#         print('Failed to delete %s. Reason: %s' % (file_path, e))

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status)
    q.put(indata.copy())

with open('article/' + recordingCat + '.txt', 'r', encoding='utf-8') as f:
    # To not to read the url in the first line
    f.readline()
    text = f.read()

sentences = sent_tokenize(text)
# text = re.sub('[\n]+', ' ', text)
# sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

i = 16
for sentence in sentences[16:]:
    print(str(i) + '\t' + sentence)
    input('Press Enter to start recording...')
    try:
        fileName = pathToData + recordingCat + '_' + str(i) + '.wav'
        if os.path.exists(pathToData + fileName):
            os.remove(pathToData + fileName)
        file = sf.SoundFile(fileName, mode='x', samplerate=44100, channels=2)
        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
            print('press Ctrl+C to stop the recording')
            while True:
                file.write(q.get())
    except KeyboardInterrupt:
        print('Recording finished: ' + repr(fileName))
    i+=1
