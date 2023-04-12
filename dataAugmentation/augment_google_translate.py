import json
from google.cloud import translate_v2 as translate

# Authenticate with the API using your API key
translate_client = translate.Client.from_service_account_json('dissertation-379215-6246093de5f4.json')


INPUT_ORACLE_FILE = 'maximeOracles/non-augmented/Product/qmsum_train_with_oracle.jsonl'
OUTPUT_ORACLE_FILE = 'google_translate_augmented_product_train.jsonl'

# Function to paraphrase a given text using Google Translate API
def paraphrase(text):
    # Define your source and target languages
    source_lang = 'en'
    target_lang = 'fr'

    # Translate the source text to the target language
    translation = translate_client.translate(text, target_language=target_lang)

    # Backtranslate the translated text to the source language
    backtranslation = translate_client.translate(translation['translatedText'], target_language=source_lang)

    return backtranslation['translatedText']

    # Print the original text, the translated text, and the backtranslated text
    # print('Source text:', text)
    # print('Translated text:', translation['translatedText'])
    # print('Backtranslated text:', backtranslation['translatedText'])
    # print("\n")


def process_line(line):
    data = json.loads(line.strip())
    new_data = data.copy()

    # Paraphrase queries and answers in general_query_list
    for i, query_item in enumerate(data["general_query_list"]):
        new_query = paraphrase(query_item["query"])
        new_answer = paraphrase(query_item["answer"])

        new_data["general_query_list"][i]["query"] = new_query
        new_data["general_query_list"][i]["answer"] = new_answer
        

    # Paraphrase queries and answers in specific_query_list
    for i, query_item in enumerate(data["specific_query_list"]):
        new_query = paraphrase(query_item["query"])
        new_answer = paraphrase(query_item["answer"])

        new_data["specific_query_list"][i]["query"] = new_query
        new_data["specific_query_list"][i]["answer"] = new_answer
        
        
    original_meeting_transcripts = data["meeting_transcripts"]
    augmented_meeting_transcripts = augment_meeting_transcripts(original_meeting_transcripts)
    new_data["meeting_transcripts"] = augmented_meeting_transcripts

    return json.dumps(new_data)


def run():
    with open(INPUT_ORACLE_FILE, "r") as infile, open(OUTPUT_ORACLE_FILE, "w") as outfile:
        for line in infile:
            new_line = process_line(line)
            outfile.write(new_line + "\n") #write the new augmented line

            outfile.write(line) #Write the original line


def augment_meeting_transcripts(meeting):  
    new_meeting = meeting.copy()
    
    for i, turn in enumerate(meeting):
        content = turn["content"]
        
        if len(content) > 15:
            new_meeting[i]["content"] = paraphrase(content)
        
    return new_meeting
        
        
if __name__ == "__main__":
    run()