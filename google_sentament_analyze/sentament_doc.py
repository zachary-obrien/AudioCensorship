import analyze_sentament


class sentament_doc(input_doc_string, sentences, words):
    self.doc_string = input_doc_string
    self.sentences = sentences
    self.word_dict = words

    def analyze_sentament(self):
        doc_data = analyze(self.doc_string)
        print(doc_data)

