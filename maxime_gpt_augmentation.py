import json
import openai

# Replace 'your_api_key_here' with your actual API key
openai.api_key = "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"
# openai.api_key = "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"

# I HAVE ALREADY AUGMENTED COMMITEE
# I HAVE ALREADY AUGMENTED ACADEMIC
# I AM CURRENTLY AUGMENTING PRODUCT

# INPUT_ORACLE_FILE = 'maximeOracles/non-augmented/Product/qmsum_train_with_oracle.jsonl'
INPUT_ORACLE_FILE = 'PRODUCT_DUPLICATE_qmsum_train_with_oracle.jsonl'
OUTPUT_ORACLE_FILE = 'gpt_augmented_product_train_part_2.jsonl'

# Function to paraphrase a given text using OpenAI's GPT-3 Davinci model
def paraphrase(text):
    response = openai.Completion.create(
        # engine="davinci",
        engine="text-davinci-003",
        # prompt=f"Explain what data augmentation is",
        prompt=f"I will give you some text. I want you to paraphrase the text. Only output the paraphrased text in 1 line. Here is the text to paraphrase: '{text}'",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    paraphrased_text = response.choices[0].text.strip()
    
    return paraphrased_text



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