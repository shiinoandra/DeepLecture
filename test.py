import SrtUtil
srtool = SrtUtil.SrtTool()
wav_filename = ""
srt_filename = ""

srtool.process_srt(srt_filename)
sentences = srtool.sentences
rate,wavedata = wavfile.read(wav_filename)
for sentence in sentences:
    wave_chunk = wavedata[int(sentence.sample_start):int(sentence.sample_end)]
