import sys
import datetime
from scipy.io import wavfile
import os
import re,string

sampling_rate = 16000

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
