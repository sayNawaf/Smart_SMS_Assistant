# Smart_SMS_Assistant
## ABSTRACT
As part of typical business workflows, some organizations may need to send an adverse action letter
to a customer / prospective customer. Examples of adverse action letters can be: a notice of
foreclosure, a denial of application for a loan, etc. Organizations may want to send such a letter in a compressed format ie summarised in about 350 characters.
I have made an Algoritham that generates an Abstractive summarization i about 350 and sends as Sms or whatsapp message.

## ABOUT
contains a front-end that takes input as a pdf file to be summarized and the number to which to send the sms or whatsapp message.My algoritham summarizes the text and sends a well formed  SMS to respective number.
Also contains a QuestionAnswering API that needs to deployed along with the website that can reply to queries related to the letter sent.
recent:///3aa606d993fa9e1561dfa67963673222

## SUMMARIZATION ALGORITHAM
Can summarize text of any lenght.this is possible by doing it in a recursive way.first the text is  devided  into chunks (since GPT-3 can only take a certain lenght of text at a time) each chunk is
given as input to GPT-3 and prompted to generate an abstractive summary.the summary generated from each chunk is concatenated to form a final summary and this proccess is repeated but with the final summary every itteration.
if the GPT-3 model cannot reduce the summarize size further and the final lenght isnt around 350 character limit it goes to BERT which performs an extractive summarization reducing it to the required lenght.


## QUESTION-ANSWERING
on deploying QuestAnsAPI user can send queries after recieving the summarization through whatsapp and it will respond with an answer.the answer is 
generated using the input pdf file as source so any questions from the input letter can be sent via whatsapp and will respond there itself..

### Yet to Implement....
for now transfer of letter content from website backend to the quest-Ans api for answering generation from input letter is not implemented, a sample letter is hardcoded into the api from which question answering can be done...feel free to implement the dispatch of letter contents to the api once the user inputs it at the website.
