from generate_embeddings import generate_embeddings_request
from database import execute_fetchall
import pprint as pp
def get_user_input():
    return input("Enter a search for programming languages: ")

def main():
    user_input = get_user_input()
    while user_input != None:
        json_response = generate_embeddings_request(user_input)
        embeddings = json_response["data"][0]["embedding"]
        results = execute_fetchall(embeddings=embeddings)
        pp.pprint(results)

        user_input = get_user_input()

    
if __name__ == "__main__":
    main()