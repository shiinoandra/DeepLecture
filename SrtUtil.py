import sys
import datetime
from scipy.io import wavfile
import os
import re,string

# filename = sys.argv[1]
# sampling_rate = int(sys.argv[2])
# wav_filename = sys.argv[3]
# output_name = sys.argv[4]
# filename = sys.argv[1]
# wav_filename = sys.argv[3]
# output_name = sys.argv[4]

sampling_rate  = 16000
class Sentence:
    time_start = 0
    time_end = 0
    sample_start = 0
    sample_end = 0
    text = ""

    def calculate_sample_diff(self,_time_end,_time_start,_time_start_remainder,_time_end_remainder):
        return (((_time_end-_time_start).total_seconds()*sampling_rate)+((_time_end_remainder - _time_start_remainder) * (sampling_rate/1000)))

    def calculate_sample_start(self,_time_start,_time_start_remainder):
        return (((_time_start.hour*3600+_time_start.minute*60+_time_start.second)*sampling_rate)+(_time_start_remainder*(sampling_rate/1000)))

    def __init__(self,_time_start,_time_start_remainder,_time_end,_time_end_remainder,_text):
        self.time_start =  datetime.datetime.strptime(_time_start, '%H:%M:%S')
        self.time_end =    datetime.datetime.strptime(_time_end, '%H:%M:%S')
        self.sample_start = self.calculate_sample_start(datetime.datetime.strptime(_time_start, '%H:%M:%S'),_time_start_remainder)
        self.sample_end = self.sample_start+self.calculate_sample_diff(self.time_end, self.time_start,_time_start_remainder,_time_end_remainder)
        self.text = _text
    def print_info(self):
        print("time start :"+str(self.time_start.hour)+":"+str(self.time_start.minute)+":"+str(self.time_start.second))
        print("time end :"+str(self.time_end.hour)+":"+str(self.time_end.minute)+":"+str(self.time_end.second))
        print("sample start :"+str(self.sample_start))
        print("sample end :"+str(self.sample_end))
        print("sample text :"+self.text)


class SrtTool:
    sentences = []


    def sentence_cleaning(self,_subs_chunk):
        clean_chunk = _subs_chunk
        clean_chunk  = clean_chunk.replace("--", "")
        clean_chunk  = clean_chunk.replace(",", "")
        clean_chunk  = clean_chunk.replace("PROFESSOR:", "")
        clean_chunk  = clean_chunk.replace("AUDIENCE:", "")
        clean_chunk  = clean_chunk.replace("[AUDIENCE TALKS]:","")
        regex = re.compile('[^a-zA-Z0-9 ]')
        clean_chunk = regex.sub('', clean_chunk)
        if _subs_chunk.find("[") != -1 or _subs_chunk.find("]") != -1:
            clean_chunk = ""
        return clean_chunk

    def process_srt(self,filename):
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
                sub_text = self.sentence_cleaning(sub_text)
                if sub_text !="" and idx+3<len(subs_buffer) :
                    # print len(subs_buffer)
                    # print idx
                    if subs_buffer[idx+3]!="" :
                        sub_text=sub_text+" "+subs_buffer[idx+3]
                        idx=idx+5
                    else:
                        idx=idx+4
                    new_sentence = Sentence(time_label_start,int(time_label_start_remainder), time_label_end,int(time_label_end_remainder),sub_text)
                    if len(self.sentences) > 0 and self.sentences[-1].time_end != new_sentence.time_start:
                        self.sentences[-1].time_end = new_sentence.time_start
                        self.sentences[-1].sample_end = new_sentence.sample_start
                    self.sentences.append(new_sentence)
