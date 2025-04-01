import json
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class ChatBot: 

    def __init__(self, corpus_path):
        with open(corpus_path, 'r') as file:
            data = json.load(file)
        self.corpus = data['freq']

    def start_chat(self, mode):
        while True:
            question = input("ask question (write exit to finish): ")
            if question == "exit":
                break
            question_words = question.split(" ")
            
            if len(question_words) == 1:
                print("please write more specific question")
            else:
                frequency_dict = self.__questions_to_dictionary()
                self.__process_question(question_words, frequency_dict, mode)

    def __questions_to_dictionary(self):
        frequency_dict = {}
        for row in self.corpus:
            frequency_dict[row["question"]] = 0
        return frequency_dict

    def __process_question(self, question_words, frequency_dict, mode):
        if mode == 'frequency':
            question = self.__frequency(question_words, frequency_dict)[0][0]
            answer = self.__find_answer(question)
            print(answer)
        elif mode == 'bigram':
            question = self.__bigram(question_words, frequency_dict)[0][0]
            answer = self.__find_answer(question)
            print(answer)
        else:
            "method not implemented"
            
    def __frequency(self, words_to_process, frequency_dict):
        for answer in frequency_dict:
            for word in words_to_process:
                if word in answer:
                    frequency_dict[answer] += 1
        frequency_dict = sorted(frequency_dict.items(), key=lambda x:x[1],reverse=True)
        return frequency_dict
    
    def __bigram(self, words_to_process, frequency_dict):
        for answer in frequency_dict:
            words_count = len(words_to_process) - 1
            for i in range(words_count):
                bigram = words_to_process[i] + " " + words_to_process[i+1]
                if bigram in answer:
                    frequency_dict[answer] +=1
        frequency_dict = sorted(frequency_dict.items(), key=lambda x:x[1], reverse=True)
        return frequency_dict
    
    def __find_answer(self, question):
        for row in self.corpus:
            if row["question"] == question:
                return row['answer']

chatbot = ChatBot("Minecraft_FAQ.json")
chatbot.start_chat(mode="bigram")