import sys

baseline = sys.argv[1]
test = sys.argv[2]

def calculate_WER(baseline,test):

    correct_counter=0
    total_len=0
    with open(baseline) as f:
        sentence_baseline = f.readlines()
    with open(baseline) as f:
        sentence_test = f.readlines()
    for i in range(len(sentence_baseline)):
        words = sentence_baseline[i].split()
        total_len = total_len + len(words)
        for word in words:
            if sentence_test[i].find(word) >=0:
                correct_counter=correct_counter+1
    print "Found Word   : " + str(correct_counter)
    print "Total Word   : " + str(total_len)
    print "WER          : " + str(((total_len - correct_counter)/total_len * 100))+"%"


calculate_WER(baseline,test)
