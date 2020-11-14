import analyze_sentament
import json

class sentament_doc():

    def populate_doc(self, input_doc_string=None, sentences=None, words=None):
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
    
    def sentence_timing(self, sentence_dict):
        min_time = 0
        max_time = 0
        print(sentence_dict)

    def analyze_sentament(self):
        doc_data = analyze_sentament.analyze(self.doc_string)
        for index, sentence in enumerate(doc_data.sentences):
            word = sentence.text
            magnitude = sentence.sentiment.magnitude
            score = sentence.sentiment.score
            should_delete = self.find_sentament(magnitude, score)
            self.sentence_timing(self.sentences[index])
            # print("\n\n\n\n")
            # print(sentence)
            


my_sentament_doc = sentament_doc()
my_sentament_doc.populate_doc(input_doc_string="It's great to see you. I hate Jenna",\
    sentences=["It's great to see you.", "I hate Jenna"], \
    words={0:{"It's":(0,125),"great":(125,200),"to":(200,300),"see":(300,600),"you":(600,1000),}, \
        1:{"I":(1000, 1100), "hate":(1100,1250), "Jenna":(1250,1500)}})
my_sentament_doc.analyze_sentament()