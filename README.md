# Project Documentation

## Overview

This project is designed to automatically generate answers from a PDF document and post these answers to a Slack channel. It involves extracting text from a PDF, generating embeddings for chunks of text, storing these embeddings, retrieving relevant chunks based on questions, generating answers, and finally posting these answers to Slack.

## Requirements

- Python 3.x
- Libraries: PyMuPDF, Slack SDK, OpenAI's GPT (for embeddings generation and completions)
- A Slack API token with permissions to post messages
- OpenAI API token

## Installation

1. Clone the repository:

    `git clone https://github.com/sidharthancr/pdf-rag-slack`

2. Install the required Python packages:

   `pip install -r requirements.txt`

3. Copy the `.env.example` file to `.env` and replace `your_slack_token_here` and `your_openai_token_here` with your actual Slack API token and OpenAI API token respectively:

    - Copy `.env.example` to `.env`:

      `cp .env.example .env`
    
    replace the `your_slack_token_here` and `your_openai_token_here` with respective values.


## Usage

1. Place the PDF document from which you want to extract information in the `data/content.pdf` directory.
2. Add your questions in JSON format in the `data/questions.json` file.
3. Ensure you have set up your Slack API token and OpenAI API key as environment variables:
    - `SLACK_TOKEN`
    - `OPENAI_API_KEY`
4. Run the script:
    `python main.py`


## How It Works

1. **Extract Text from PDF**: The script reads the PDF document and extracts text.
2. **Generate Embeddings**: It then generates embeddings for chunks of text using OpenAI's GPT.
3. **Store Embeddings**: These embeddings are stored for later retrieval.
4. **Retrieve Relevant Chunks**: Based on the questions, the script retrieves relevant chunks of text.
5. **Generate Answers**: It generates answers from the retrieved chunks.


6. **Post to Slack**: Finally, the answers are posted to a specified Slack channel.
## Configuration

The following configurations can be adjusted in the `main.py` file:

- `pdf_path`: Specifies the path to the PDF document from which text will be extracted.
- `questions`: Defines the path to a JSON file containing the questions to be answered based on the PDF document's content.
- `index_file`: Indicates the path where the embeddings index, used for retrieving relevant chunks of text, will be stored.
- `slack_channel_id`: The ID of the Slack channel where answers will be posted.
