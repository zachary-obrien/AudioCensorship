from google.cloud import speech_v1 as speech
import os
import io

credential_path = "google_creds.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

TRANSCRIPT = []
FULL_TRANSCRIPT = ""
sentence = 0
TIMES = dict()


def print_sentences(response):
    global TIMES, sentence, TRANSCRIPT
    TIMES[sentence] = {}
    for result in response.results:
        best_alternative = result.alternatives[0]
        transcript = best_alternative.transcript
        confidence = best_alternative.confidence
        TRANSCRIPT.append(transcript)
        print_word_offsets(best_alternative)


def print_word_offsets(alternative):
    global FULL_TRANSCRIPT, TRANSCRIPT, TIMES, sentence
    for word in alternative.words:
        start_s = word.start_time.total_seconds() * 1000
        end_s = word.end_time.total_seconds() * 1000
        time = (start_s,end_s)

        punctuations = '''.?~!,-'''
        puncts = '''.?!'''
        new_word = ""
        for char in word.word:
            if char not in punctuations:
                new_word = new_word + char

        TIMES[sentence][new_word] = time

        for char in word.word:
            if char in puncts:
                sentence = sentence + 1
                TIMES[sentence] = {}

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
    i = len(TIMES) -1
    del TIMES[i]
    return FULL_TRANSCRIPT, TRANSCRIPT, TIMES