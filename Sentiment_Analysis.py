#    client = language_v1.LanguageServiceClient(credentials="google_creds.json")
import argparse

from google.cloud import language_v1
from google.oauth2 import service_account
# [END language_sentiment_tutorial_imports]


# [START language_sentiment_tutorial_print_result]
def print_result(annotations):
    print(annotations)
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print(
            "Sentence {} has a sentiment score of {}".format(index, sentence_sentiment)
        )

    print(
        "Overall Sentiment: score of {} with magnitude of {}".format(score, magnitude)
    )
    return 0


# [END language_sentiment_tutorial_print_result]


# [START language_sentiment_tutorial_analyze_sentiment]
def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    credentials = service_account.Credentials.from_service_account_file("google_creds.json")
    client = language_v1.LanguageServiceClient(credentials=credentials)
    encoding_type = language_v1.EncodingType.UTF8

    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    #annotations = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    #response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})
    # Print the results
    #print(annotations)
    return annotations
    #print(response)
    #print_result(annotations)


# [END language_sentiment_tutorial_analyze_sentiment]



analyze("It's great to see how little thought you give things. It leaves so much time for doing random stuff rather than being productive.")