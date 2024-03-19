import json
from difflib import get_close_matches

#opens knowledge_base.json file
def load_knowledge(fp: str) -> dict:
    with open(fp, 'r') as file:
        data: dict = json.load(file)
    return data

#writes to knowledge_base.json file
def save_knowledge(fp: str, data:dict):
    with open(fp, 'w') as file:
        json.dump(data, file, indent=2)

#gets closest matching questions string in knowledge_base.json
def find_match(user: str, questions:list[str]) -> str | None:
    matches: list = get_close_matches(user, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#returns answer of questions string found through find_match 
def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

#chatbot that takes user input and responds based on knowledge_base
def chat_bot():
    #use knowloedge_base.json to create dictionary for questions and answers
    knowledge_base: dict = load_knowledge('knowledge_base.json')

    #infinite loop *replace condition to better suit use case* 
    while 1:
        #Intro Bot to user *implement predetermined responses to guide user*
        #print("This is fiber chat bot, please describe the issue you are having. If you have no more questions enter [q]uit")
        #Take user input
        user_in: str = input("You: ")
        if user_in.lower() == 'quit' or user_in.lower() == 'q': #break loop to end session
            break

        elif user_in == '1234':  #admin key to input questions and answers to avoid user adding to knowledge_base
            new_answer: str = input('Input a user question or [d]one to return to menu: ')
            while new_answer.lower() != 'd' or new_answer.lower() != 'done':
                if new_answer.lower() == 'done' or new_answer.lower() == 'd':
                    print("Exiting admin mode")
                    user_in: str = input("You: ")
                    break
                
                else:
                    user_in: str = input("Input the answer: ")
                    knowledge_base["questions"].append({"question":  new_answer, "answer": user_in})
                    save_knowledge('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you, I have now learned this response.')

        best_match: str | None = find_match(user_in, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer(best_match, knowledge_base)
            print(f'Bot: {answer}')

        else:
            print('Bot: Sorry I cannot answer this question.')
            

chat_bot()