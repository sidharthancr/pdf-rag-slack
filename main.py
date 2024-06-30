import json
from dotenv import load_dotenv
from utils.pdfUtils import extract_text_from_pdf 
from utils.embeddingUtils import chunk_text ,load_index, save_index, store_embeddings
from clients.openAiClient import generate_embeddings_openai, retrieve_relevant_chunks, generate_answer
from clients.slackClient import post_message_to_slack

# Load environment variables
load_dotenv()

# Main function
def main(pdf_path, questions, index_file, slack_channel_id):
    pdf_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(pdf_text)
    
    # Load or generate embeddings and store index
    try:
        index = load_index(index_file)
    except:
        embeddings = generate_embeddings_openai(chunks)
        index = store_embeddings(embeddings)
        save_index(index, index_file)

    answers = {}
    for question in questions:
        retrieved_chunks = retrieve_relevant_chunks(question, index, chunks)
        answer = generate_answer(question, retrieved_chunks)
        answers[question] = answer
    ## Replace with your Slack channel ID
    post_message_to_slack(slack_channel_id, json.dumps(answers))
    print("Answers posted to Slack channel.")
    print(answers)
    return answers

if __name__ == "__main__":
    pdf_path = "data/content.pdf"
    with open('data/questions.json', 'r') as file:
        questions = json.load(file)
    index_file = "data/index.index"
    main(pdf_path, questions, index_file,"C057QPUCD63")