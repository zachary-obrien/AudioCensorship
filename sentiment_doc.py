import Sentiment_Analysis
import SpeechToText
import json
import censorship


class sentiment_doc():

    def populate_doc(self, audio_file=None, input_doc_string=None, sentences=None, words=None):
        self.audio_file = audio_file
        self.doc_string = input_doc_string
        self.sentences = sentences
        self.word_dict = words

    def find_sentiment(self, magnitude, score):
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
        return (int(min_time), int(max_time))

    def analyze_sentiment(self):
        doc_data = Sentiment_Analysis.analyze(self.doc_string)
        sentences_to_delete = []
        for index, sentence in enumerate(doc_data.sentences):
            word = sentence.text
            magnitude = sentence.sentiment.magnitude
            score = sentence.sentiment.score
            should_delete = self.find_sentiment(magnitude, score)
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


my_sentiment_doc = sentiment_doc()
audio_file = "SpeechToText8.wav"
full_string, transcript, word_dict = SpeechToText.transcribe_file(audio_file)
print("full_string")
print(full_string)
print("transcript")
print(transcript)
print("word_dict")
print(word_dict)
my_sentiment_doc.populate_doc(audio_file=audio_file, input_doc_string=full_string, sentences=transcript, words=word_dict)
times_to_delete = my_sentiment_doc.analyze_sentiment()
censorship.censor(audio_file, times_to_delete)
#my_sentiment_doc.remove_audio(times_to_delete)