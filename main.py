import datetime
import json
import os
from typing import Optional
from scraping_scripts import *

def load(fromfile, directory):
    with open(f'{directory}\\{fromfile}', "r") as infile:
        return json.load(infile)


def store(tojson, directory, filename):
    with open(f'{directory}\\{filename}', "w") as outfile:
        json.dump(tojson, outfile)

def main(topics: Optional[list] = None,
         question_list: Optional[str] = None,
         question_links: Optional[list] = None, 
         save_dir: str = os.path.dirname(os.path.realpath(__file__)),
         previous_save_number: int = 0, 
         save_frequency_main: int = 100, 
         get_views: bool = False,
         crawl_questions: bool = True,
         crawl_answers: bool = False
         ) -> None:
    
    if topics is None:
        topics = []
    elif question_links is not None:
        topics = []

    assert type(save_dir) is str, 'save_dir should be a valid string pointing to a directory'
    assert type(topics) is list, 'topics should be a list of topics'


    question_set = dict()

    if len(topics) != 0:
        question_set = get_questions_text(topics)
        for topic in question_set.keys():
            for question in question_set[topic]:
                print(f'{topic}: {question}')
        store(question_set, save_dir, f'topic_question_set{datetime.datetime.now().strftime("%m-%d_%H_%M")}')
        #if get_views:
        #    get_answers_w_views(question_links, n_save=previous_save_number, save_frequency=save_frequency_main)
        #else:
       #     get_answers(question_links, n_save=previous_save_number, save_frequency=save_frequency_main)

    if question_list is not None:
        try:
            setFile = load(question_list, save_dir)
        except FileNotFoundError:
            print("Input question set not found")
            return
        print(f'Found {len(setFile.keys())} topics.')


        answers = dict()
        for topic in setFile.keys():
            print(f"Pulling answers for topic: {topic}")
            topic_answers = get_answers_from_questions(list(setFile[topic]))
            answers[topic] = topic_answers

        store(answers, save_dir, f'topic_answers_set{datetime.datetime.now().strftime("%m-%d_%H_%M")}')

if __name__ == "__main__":
    main(topics=['Albert Einstein (physicist)'], crawl_questions=True, crawl_answers=False, get_views=False)
