import sys
import datetime
import os
import re,string
import sentence

# filename = sys.argv[1]
# sampling_rate = int(sys.argv[2])
# wav_filename = sys.argv[3]
# output_name = sys.argv[4]
# filename = sys.argv[1]
# wav_filename = sys.argv[3]
# output_name = sys.argv[4]




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
                    new_sentence = sentence.Sentence(time_label_start,int(time_label_start_remainder), time_label_end,int(time_label_end_remainder),sub_text)
                    if len(self.sentences) > 0 and self.sentences[-1].time_end != new_sentence.time_start:
                        self.sentences[-1].time_end = new_sentence.time_start
                        self.sentences[-1].sample_end = new_sentence.sample_start
                    self.sentences.append(new_sentence)
