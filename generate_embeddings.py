import wikipediaapi
import requests
import json
from transformers import BertTokenizer
from database import connect_to_db, insert_programming_language
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

def get_env_vars(*args):
    return [os.getenv(arg) for arg in args]

LOCALAI_HOST, LOCALAI_PORT = get_env_vars('LOCALAI_HOST', 'LOCALAI_PORT')

# Initialize the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def fit_text(input_text):
    # Tokenize the text
    tokens = tokenizer.tokenize(input_text)

    # The BERT models include special tokens [CLS] and [SEP], so we have to account for them
    max_tokens = 384 - 2  # Accounting for [CLS] and [SEP]

    # Check how many tokens can fit
    if len(tokens) > max_tokens:
        # If more than 512 tokens, truncate the list of tokens to the maximum size
        fitting_tokens = tokens[:max_tokens]
        print(f"Only the first {len(fitting_tokens)} words/tokens can be sent to BERT for text embeddings.")
    else:
        print(f"All {len(tokens)} words/tokens can be sent to BERT for text embeddings.")

    # Optionally, convert tokens back to text to see what fits
    fitting_text = tokenizer.convert_tokens_to_string(fitting_tokens if len(tokens) > max_tokens else tokens)
    print("Fitting text:", fitting_text)
    return fitting_text

# Function to make a POST request
def generate_embeddings_request(input):
    url = f"http://{LOCALAI_HOST}:{LOCALAI_PORT}/embeddings"
    headers = {"Content-Type": "application/json"}
    payload = {"input": json.dumps(input), "model": "bert-cpp-minilm-v6" }
    print("Executing post request")
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


    
def get_page(page_title):
    page_title = f"{language} (programming language)" 
    wiki_wiki = wikipediaapi.Wikipedia('yb-localai (sampleapp@example.com)', 'en')
    page = wiki_wiki.page(page_title)
    if page.exists() == False:
        page = wiki_wiki.page(language)
    print(page)
    return page.summary


programming_languages = [
    "Python", "JavaScript", "Java", "C#", "C++", "Ruby", "Swift", "Go", "Kotlin", "PHP",
    "Rust", "TypeScript", "Scala", "Perl", "Lua", "Haskell", "Elixir", "Clojure", "Dart", "F#",
    "Objective-C", "Assembly", "Groovy", "Erlang", "Fortran", "COBOL", "Pascal", "R", "Julia", "MATLAB",
    "SQL", "Shell", "Bash", "PowerShell", "Ada", "Visual Basic", "Delphi", "SAS", "LabVIEW", "Prolog",
    "Lisp", "Scheme", "Smalltalk", "Simula", "PL/SQL", "ABAP", "Apex", "VHDL", "Verilog", "Scratch",
    "Solidity", "VBA", "AWK", "OCaml", "Common Lisp", "D", "Elm", "Factor", "Forth", "Hack",
    "Idris", "J#", "Mercury", "Nim", "Oz", "Pike", "PureScript", "Rebol", "Red", "Tcl"
]

def main():
    for language in programming_languages:

        text = get_page(language)

        if text:
            try:
                print(f"Generating embeddings for {language}")
                json_response = generate_embeddings_request(fit_text(text))
                print(json_response)
                embeddings = json_response["data"][0]["embedding"]

                db_connection = connect_to_db()
                insert_programming_language(db_connection, name=language, summary=text, embeddings=embeddings)
            finally:
                db_connection.close()

if __name__ == "__main__":
    main()

