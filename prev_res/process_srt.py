import sys
import datetime
from scipy.io import wavfile
import os

filename = sys.argv[1]
sampling_rate = int(sys.argv[2])
wav_filename = sys.argv[3]
output_name = sys.argv[4]
sentences = []


def calculate_sample_diff(_time_end,_time_start,_time_start_remainder,_time_end_remainder):
    return (((_time_end-_time_start).total_seconds()*sampling_rate)+((_time_end_remainder - _time_start_remainder) * (sampling_rate/1000)))

def calculate_sample_start(_time_start,_time_start_remainder):
    return (((_time_start.hour*3600+_time_start.minute*60+_time_start.second)*sampling_rate)+(_time_start_remainder*(sampling_rate/1000)))


class Sentence:
    time_start = 0
    time_end = 0
    sample_start = 0
    sample_end = 0
    text = ""
    def __init__(self,_time_start,_time_start_remainder,_time_end,_time_end_remainder,_text):
        self.time_start =  datetime.datetime.strptime(_time_start, '%H:%M:%S')
        self.time_end =    datetime.datetime.strptime(_time_end, '%H:%M:%S')
        self.sample_start = calculate_sample_start(datetime.datetime.strptime(_time_start, '%H:%M:%S'),_time_start_remainder)
        self.sample_end = self.sample_start+calculate_sample_diff(self.time_end, self.time_start,_time_start_remainder,_time_end_remainder)
        self.text = _text
    def print_info(self):
        print("time start :"+str(self.time_start.hour)+":"+str(self.time_start.minute)+":"+str(self.time_start.second))
        print("time end :"+str(self.time_end.hour)+":"+str(self.time_end.minute)+":"+str(self.time_end.second))
        print("sample start :"+str(self.sample_start))
        print("sample end :"+str(self.sample_end))
        print("sample text :"+self.text)

def process_wav():
    counter = 1
    if not os.path.exists("wav48/"+output_name):
        os.makedirs("wav48/"+output_name)
    if not os.path.exists("txt/"+output_name):
        os.makedirs("txt/"+output_name)
    #output_name = wav_filename.replace(".wav","")
    rate,wavedata = wavfile.read(wav_filename)
    for sentence in sentences:
        wave_chunk = wavedata[int(sentence.sample_start):int(sentence.sample_end)]
        subs_chunk = sentence.text
        wavfile.write(("wav48/"+output_name+"/"+output_name+"-"+str(counter)+".wav"),sampling_rate,wave_chunk)
        with open(("txt/"+output_name+"/"+output_name+"-"+str(counter)+".txt"), "w") as text_file:
            text_file.write(subs_chunk)
        counter=counter+1





def sentence_cleaning(_subs_chunk):
    clean_chunk = _subs_chunk
    clean_chunk  = clean_chunk.replace("--", "")
    clean_chunk  = clean_chunk.replace(",", "")
    clean_chunk  = clean_chunk.replace("PROFESSOR:", "")
    clean_chunk  = clean_chunk.replace("AUDIENCE:", "")
    clean_chunk  = clean_chunk.replace("[AUDIENCE TALKS]:", "")
    if _subs_chunk.find("[") != -1 or _subs_chunk.find("]") != -1:
        clean_chunk = ""
    return clean_chunk

def process_srt():
    with open(filename, mode='r') as file_srt:
        subs = file_srt.read()
    subs_buffer = subs.split('\n')
    for idx, val in enumerate(subs_buffer):
        if val.isdigit():
            time_label = subs_buffer[idx+1].split(" --> ")
            time_label_start = time_label[0].split(',')[0]
            time_label_start_remainder = time_label[0].split(',')[1]
            time_label_end = time_label[1].split(',')[0]
            time_label_end_remainder = time_label[1].split(',')[1]
            sub_text = subs_buffer[idx+2]
            sub_text = sentence_cleaning(sub_text)
            if sub_text !="" and idx+3<len(subs_buffer) :
                # print len(subs_buffer)
                # print idx
                if subs_buffer[idx+3]!="" :
                    sub_text=sub_text+" "+subs_buffer[idx+3]
                    idx=idx+5
                else:
                    idx=idx+4
                new_sentence = Sentence(time_label_start,int(time_label_start_remainder), time_label_end,int(time_label_end_remainder),sub_text)
                if len(sentences) > 0 and sentences[-1].time_end != new_sentence.time_start:
                    sentences[-1].time_end = new_sentence.time_start
                    sentences[-1].sample_end = new_sentence.sample_start
                sentences.append(new_sentence)


process_srt()
process_wav()
