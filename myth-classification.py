# sample script to classify human-generated responses (from Reddit) promoting M1 (Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another)

import openai
import pandas as pd
from tqdm import tqdm
import json
import time

# load the API
# provide Open API credentials below
openai.api_type = "API_TYPE"
openai.api_version = "API_VERSION"
openai.api_base = "API_BASE"
openai.api_key = "API_KEY"

# few-shot examples
examples = ["Ok but you're just replacing one addiction with another so what's the point.",
            "So you're exchanging one drug habit for another. Good idea.",
            "Seperate yourself far enough from the drug game and then make the jump. Do not use MAT. You will end up with another addiction.",
            "Is the heroin assisted treatment just for addicts? Or can pain patients get it as well?",
            "It's suboxone. It's used as opioid replacement therapy. Or you can use it to do a rapid taper and be clean of all opiates."
]

# binary labels
answers = ["Yes",
           "Yes",
           "Yes",
           "No",
           "No"
]

# reasoning for chain-of-thought prompting
reasoning = ["This response promotes the myth that 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another' since the author restates the myth by saying that medication-assisted treatment replaces one addiction (i.e. to opioids) with another (i.e. to medication-assisted treatment drugs).",
             "This response promotes the myth that 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another' since the author restates the myth by saying that medication-assisted treatment is equivalent to exchanging one drug habit with another.",
             "This response promotes the myth that 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another' since the author advocates against MAT i.e. medication-assisted treatement, saying that it will lead to another addiction.",
             "This response does not promote the myth that 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another' since the author is asking a question related to medication-assisted treatment, which is who all are eligible to enroll into medication-assisted treatment.",
             "This response does not promote the myth that 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another' since the author is informing or spreading knowledge about suboxone, a medication-assisted treatment for opioid use disorder."
]

# llm prompt to classifiy M1
initial_prompt = f'''You are an expert in social media analysis and opioid use disorder. First, please analyze the following examples where we indicate if a response actively promotes or restates a myth on opioid use disorder. \
            The myth is 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another'. \
            There are five examples, one on each line. Each example contains the response, the human-generated answer as either 'Yes' or 'No' to determine whether the response promotes the myth or not, and the reasoning for why the response promotes or does not promote the myth.
            'Response': {examples[0]}; 'Answer': {answers[0]}; 'Reasoning': {reasoning[0]} \n
            'Response': {examples[1]}; 'Answer': {answers[1]}; 'Reasoning': {reasoning[1]} \n
            'Response': {examples[2]}; 'Answer': {answers[2]}; 'Reasoning': {reasoning[2]} \n
            'Response': {examples[3]}; 'Answer': {answers[3]}; 'Reasoning': {reasoning[3]} \n
            'Response': {examples[4]}; 'Answer': {answers[4]}; 'Reasoning': {reasoning[4]} \n
            Task: Given what you learned from the examples, your task is to determine whether the following response actively promotes the myth: 'Agonist therapy or medication assisted treatment for opioid use disorder is merely replacing one drug with another'. \
            Answer with a binary 'Yes' or 'No'. \
            Answer No if the response's author only talks about their personal experience with opioid use disorder or an issue other that the provided myth. \
            Also provide a reasoning for your answer, quoting excerpts from the response.\
            Do not restate the response and only provide one answer. Please think through step by step. \
            Format your response as: \
            Answer: <insert 'Yes' or 'No' here> \n\n Reasoning: <insert your reasoning here> \n
        '''

# load reddit responses to be classified
df = pd.read_csv("") # add link to the dataset
comment_ids = list(df["comment_id"])
comment_text = list(df["comment_text"])

for i in tqdm(range(len(comment_text))): # iterate over the entire human-generated reddit dataset
    id = comment_ids[i] # reddit response ID
    text = comment_text[i] # reddit response

    skip_current_case = False  # Add this flag variable
    success = False  # Variable to track if API call was successful
    retries = 0  # Variable to track number of retries
    
    while not success and retries < 5:  # Retry up to 5 times
        try:
            # generate response
            response = openai.ChatCompletion.create(
                model="gpt-35-turbo",
                engine="", # specify engine here
                messages=[
                    {
                        "role": "user",
                        "content": initial_prompt + "\n\n" + "Statement: " + text,
                    },
                ],
                temperature=0.0
            )
            success = True  # Set success to True if API call succeeds
            
            # write llm response to output file
            chatgpt_output = json.dumps(response['choices'][0]['message']['content'])
            output_filename = "comment-" + id + "-llm-classification-output.txt" # contains classification output 
            output_path = "gpt-3_output/" + output_filename
                                
            with open(output_path, 'w') as output_file:
                output_file.write(chatgpt_output)

        except openai.error.APIConnectionError:
            retries += 1  # Increment retries variable on APIConnectionError
            time.sleep(600)  # Wait for 10 minutes before retrying

        except (openai.error.InvalidRequestError, KeyError):
            # content filter issue occurred, write "filter_issue" to the output file
            output_filename = "comment-" + id + "-llm-classification-output.txt"
            output_path = "gpt-3_output/" + output_filename

            with open(output_path, 'w') as output_file:
                output_file.write("filter_issue")

            skip_current_case = True
            time.sleep(60)
            break

        time.sleep(2)

    if skip_current_case:  # Check the flag here
        continue  # Skip to the next iteration of the for loop

    if retries >= 5:  # Check if all retry attempts have been exhausted
        output_filename = "comment-" + id + "-llm-classification-output.txt"
        output_path = "gpt-3_output/" + output_filename
        with open(output_path, 'w') as output_file:
            output_file.write("API_issue")  # Write "API_issue" to output file