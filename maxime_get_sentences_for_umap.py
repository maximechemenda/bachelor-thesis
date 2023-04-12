import os
import json

domain = "Product"
AUGMENTED_WITH_GPT_PATH = f"maximeOracles/augmented/{domain}/qmsum_train_with_oracle.jsonl"
AUGMENTED_WITH_GOOGLE_PATH = f"maximeOracles/augmented_with_google_translate/{domain}/qmsum_train_with_oracle.jsonl"

# 1 augmented
# 2 original

class SentencesGetter(object):
    def __init__(self):
        self.augmented_with_gpt_file_content = None
        self.augmented_with_google_file_content = None

        self.gpt_sentences = []
        self.google_sentences = []
        self.original_sentences = []

        with open(AUGMENTED_WITH_GPT_PATH) as f:
            self.augmented_with_gpt_file_content = f.readlines()

        with open(AUGMENTED_WITH_GOOGLE_PATH) as f:
            self.augmented_with_google_file_content = f.readlines()

    def process_gpt_file(self):
        for i, item in enumerate(self.augmented_with_gpt_file_content):
            json_item = json.loads(item)
            meeting_transcripts = json_item['meeting_transcripts']

            for utterance in meeting_transcripts:
                content = utterance['content']

                if len(content) > 15:
                    # Augmented 
                    if i % 2 == 0:
                        self.gpt_sentences.append(content)
                    # Original
                    else:
                        self.original_sentences.append(content)

    def process_google_file(self):
        for i, item in enumerate(self.augmented_with_google_file_content):
            json_item = json.loads(item)
            meeting_transcripts = json_item['meeting_transcripts']

            for utterance in meeting_transcripts:
                content = utterance['content']

                # Augmented 
                if i % 2 == 0:
                    self.google_sentences.append(content)



if __name__ == "__main__":
    SentencesGetter = SentencesGetter()
    SentencesGetter.process_gpt_file()
    SentencesGetter.process_google_file()

    # Write the list to a file as a JSON object
    with open('sentences_product_original.json', 'w') as f:
        json.dump(SentencesGetter.original_sentences, f)

    with open('sentences_product_gpt.json', 'w') as f:
        json.dump(SentencesGetter.gpt_sentences, f)

    with open('sentences_product_google.json', 'w') as f:
        json.dump(SentencesGetter.google_sentences, f)