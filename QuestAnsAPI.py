from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import textwrap
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from twilio.rest import Client

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example question through the model.
    outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                                    token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from answer_text

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    start_scores = outputs.start_logits

    end_scores = outputs.end_logits

    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    print('Answer: "' + answer + '"')
    return answer

def computeWhatsAppMessage(text):
    # account_sid = 'AC836bb0f81c5a79925addb8d0cb265b73' 
    # auth_token = '4e0542b1317d1f73a9601ee2f0459963' 
    account_sid = "ACfd60968ab978cef2c3aff06833063dcb"
    auth_token = "9a2b05eaa01f97f7855cf9c181ff3e1e"
    client = Client(account_sid, auth_token)
    
    '+14699566640'
    message = client.messages.create( 
                                from_='whatsapp:+14155238886',   
                                body=text,      
                                to='whatsapp:+919901934660'
                            ) 
    
    print(message.sid)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():

    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {}".format(msg))
    
    source = "Sara is a talented literary critic and poet who has had great success in her writing and reading habits since she was a young girl. She has a high- recommendation as a student and writer. Sara is also a very intelligent woman, and her writing here at Mark Twain High School showed it. She was very passionate about reading and writing, and had a great time during her year long course. Sara is a dedicated literary companion who publishes her poetry in our school's literary magazine as well as online magazines. She is an insightful sensitive and deeply self-aware individual drive to explore art writing and a deeper understanding of humanconditions. Throughout the year, she was an active participant in our conversations and always supported her peers. Her caring nature and personality allows her to work well with others in a team setting, which makes her a successful member of the class. When we held a class debate about gun laws, she opted to speak for the side of the side she believes. Sara is a high school student who is talented, caring, and dedicated to writing. She is constantly seeking feedback to improve her writing skills, and her skills have won her a following among her peers and among herself. She is an outstanding student and an excellent writer, and she would be a great addition to any high school program."
    answer = answer_question(msg, source)
    computeWhatsAppMessage(answer)
    return str(resp)

if __name__ == "_main_":
    app.run(debug=True)
