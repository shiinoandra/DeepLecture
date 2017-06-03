import SrtUtil
# import spell
#import recognize
from scipy.io import wavfile

srtool = SrtUtil.SrtTool()
wav_filename = "l08-23.wav"
srt_filename = "HarvardCS50-0.srt"
result_sentence = []
result_sentence_LM = []

def write_to_text():
    with open(wav_filename+"-result_noLM.txt", "w") as text_file:
        for sentence in result_sentence:
            text_chunk = sentence.text
            text_file.write(text_chunk+"\n")
    with open(wav_filename+"-result_LM.txt", "w") as text_file:
        for sentence in result_sentence_LM:
            text_chunk = sentence.text
            text_file.write(text_chunk+"\n")


srtool.process_srt(srt_filename)
sentences = srtool.sentences
rate,wavedata = wavfile.read(wav_filename)
# for sentence in sentences:
#     wave_chunk = wavedata[int(sentence.sample_start):int(sentence.sample_end)]
#     result = recognize.do_recognize(wave_chunk)
#     dummy_sentence = sentence
#     dummy_sentence.text = result[0]
#     result_sentence.append(dummy_sentence)
#     dummy_sentence.text = resultp[1]
#     result_sentence_LM.append(dummy_sentence)
result_sentence = sentences
result_sentence_LM = sentences
write_to_text()
