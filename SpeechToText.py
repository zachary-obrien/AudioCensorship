from google.cloud import speech_v1 as speech
import os
import io

credential_path = r"C:\Users\rmcm6\OneDrive\Desktop\College Stuff\My First Project-93317e258743.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

TRANSCRIPT = []
FULL_TRANSCRIPT = ""
sentence = 0
TIMES = dict()


def print_sentences(response):
    global TIMES, sentence, TRANSCRIPT
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        TIMES[sentence] = {}
        TRANSCRIPT.append(transcript)
        sentence = sentence + 1
        print_word_offsets(best_alternative)


def print_word_offsets(alternative):
    global FULL_TRANSCRIPT, TRANSCRIPT, TIMES, sentence
    for word in alternative.words:
        start_s = word.start_time.total_seconds()
        end_s = word.end_time.total_seconds()
        time = (start_s,end_s)

        punctuations = '''.?~!,-'''
        new_word = ""
        for char in word.word:
            if char not in punctuations:
                new_word = new_word + char

        #if new_word not in TIMES[sentence - 1]:
            #TIMES[sentence - 1][new_word] = list()
        TIMES[sentence - 1][new_word] = time

        if len(FULL_TRANSCRIPT) < 1:
            FULL_TRANSCRIPT = word.word
        else:
            FULL_TRANSCRIPT = FULL_TRANSCRIPT + " " + word.word

def transcribe_file(speech_file):
    global TIMES, sentence, TRANSCRIPT

    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        audio_channel_count=2,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    print_sentences(response)
    return FULL_TRANSCRIPT, TRANSCRIPT, TIMES



transcribe_file(r"C:\Users\rmcm6\OneDrive\Desktop\College Stuff\SpeechToText5.wav")
