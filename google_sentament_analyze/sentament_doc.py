import analyze_sentament
import json

class sentament_doc():

    def populate_doc(self, audio_file=None, input_doc_string=None, sentences=None, words=None):
        self.audio_file = audio_file
        self.doc_string = input_doc_string
        self.sentences = sentences
        self.word_dict = words

    def find_sentament(self, magnitude, score):
        negative = True
        strong = True
        if magnitude < 0.5: 
            strong = False
        if score > 0:
            negative = False
        if strong and negative:
            return True
        return False
    
    def sentence_timing(self, sentence_index):
        min_time = 0
        max_time = 0
        for word in self.word_dict[sentence_index].keys():
            lower_time = self.word_dict[sentence_index][word][0]
            upper_time = self.word_dict[sentence_index][word][1]
            if min_time == 0 or min_time > lower_time:
                min_time = lower_time
            if max_time == 0 or max_time < upper_time:
                max_time = upper_time
        return (min_time, max_time)

    def analyze_sentament(self):
        doc_data = analyze_sentament.analyze(self.doc_string)
        sentences_to_delete = []
        for index, sentence in enumerate(doc_data.sentences):
            word = sentence.text
            magnitude = sentence.sentiment.magnitude
            score = sentence.sentiment.score
            should_delete = self.find_sentament(magnitude, score)
            self.sentence_timing(index)
            if should_delete:
                sentences_to_delete.append(index)
        sentences_to_delete = list(dict.fromkeys(sentences_to_delete)) 
        times_to_delete = []
        for sentence_index in sentences_to_delete:
            times_to_delete.append(self.sentence_timing(sentence_index))
        return times_to_delete

    def remove_audio(self, times_to_delete):
        print(self.audio_file, times_to_delete)



my_sentament_doc = sentament_doc()
my_sentament_doc.populate_doc(audio_file="test_audio", input_doc_string="It's great to see you. I hate Jenna",\
    sentences=["It's great to see you.", "I hate Jenna"], \
    words={0:{"It's":(0,125),"great":(125,200),"to":(200,300),"see":(300,600),"you":(600,1000),}, \
        1:{"I":(1000, 1100), "hate":(1100,1250), "Jenna":(1250,1500)}})
times_to_delete = my_sentament_doc.analyze_sentament()
my_sentament_doc.remove_audio(times_to_delete)