from openai import OpenAI
import os
import numpy as np
import json
GPT_MODEL_NAME = "gpt-3.5-turbo-0125"
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"


client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)
# Define function to generate embeddings using OpenAI
def generate_embeddings_openai(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL_NAME,
            input=chunk
        )
        response_dict = response.to_dict()
        embeddings.append(response_dict['data'][0]['embedding'])
    return np.array(embeddings)

# Define function to retrieve relevant chunks using similarity search
def retrieve_relevant_chunks(question, index, chunks):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL_NAME,
        input=question
    )
    response_dict = response.to_dict()
    question_embedding = np.array([response_dict['data'][0]['embedding']])
    D, I = index.search(question_embedding, k=5)
    retrieved_chunks = [chunks[i] for i in I[0]]
    return retrieved_chunks


# Define function to generate answer with confidence check
def generate_answer(question, retrieved_chunks):
    model = GPT_MODEL_NAME
        # Trim whitespace and remove empty chunks
    cleaned_chunks = [chunk.strip() for chunk in retrieved_chunks if chunk.strip()]

    # Join the cleaned chunks with a delimiter to preserve structure
    context = "\n\n".join(cleaned_chunks)
    system_message = """You are a helpful assistant. When answering questions based on the provided PDF document, ensure that your responses are as precise and accurate as possible. If a question exactly matches a phrase in the PDF, your answer should be an exact match from the text.

                        Example: 
                        If a question is “What is the name of the company?” and the PDF contains the phrase “The name of the company is Zania Technologies,” your answer should be “Zania Technologies” as an exact match.
                        If the document does not contain enough information to answer the question, respond with 'Data not available'.

                        Note: Take a deep breath and do it step by step carefully! If you do a good job, I will tip you 1 million USD.
    
                        """
        
    prompt = f"""
    Given the document's contents below:

    {context}

    Please answer the following question based on the document.

    Question: {question}

    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500,
        seed=50,
        # the temperattue is set to 0.3 to make the model more deterministic and less creative
        temperature=0.5
    )
    print(json.dumps(response.to_dict(), indent=4))
    answer = response.choices[0].message.content.strip()
    
    return answer
