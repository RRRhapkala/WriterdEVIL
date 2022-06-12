from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
import re

def get_topic(title, sentences, topic_change_chance):
    first_title = title
    black_list = []
    with open("topic.txt", "w") as file:
        file.write(f"{title}:\n")
        for s_count in range(sentences):
            try:
                sentence = get_info(title, black_list)
            except:
                sentence = get_info(first_title, black_list)
                
            black_list.append(sentence)
            file.write(f'{sentence}. ')
            sentence_arr = sentence.split(" ")
            if random.random() < topic_change_chance:
                title = get_random_word_by_length(sentence_arr, get_max_length(sentence_arr))

def get_max_length(arr):
    length = 0
    for word in arr:
        length = max(length, len(word))
    return length

def get_random_word_by_length(arr, length):
    words = [el for el in arr if len(el) == length]
    return words[random.randint(0, len(words) - 1)]

def get_info(text, black_list):
    driver.get("https://s13.ru/")
    sleep(0.5)
    search_button = driver.find_element(By.CLASS_NAME, "search")
    search_button.click()
    search_top = driver.find_element(By.ID, "search_top")
    search_top.send_keys(text)
    submit_button = driver.find_element(By.CLASS_NAME, "vertical").find_element(By.TAG_NAME, "input")
    submit_button.click()
    links = driver.find_element(By.CLASS_NAME, "content").find_elements(By.TAG_NAME, "a")
    href = links[random.randint(0, len(links) - 1)].get_attribute("href")
    content = get_page_content(href)
    return next_sentence(content, text, black_list)

    
def next_sentence(text, keyword, black_list):
    text = text.replace('!', '.').replace('?', '.').replace('\n', ' ').replace('\xa0', ' ')
    text_splitted = text.split(".")
    text_splitted = [el for el in text_splitted if len(el) > 7]
    sentence = ''
    for i, el in enumerate(text_splitted):
        if keyword in el:
            try:
                sentence = text_splitted[i + 1]
            except:
                sentence = text_splitted[i - 1]
    if sentence not in black_list and sentence != '':
        return sentence
    return text_splitted[random.randint(0, len(text_splitted) - 1)]
        
def get_page_content(href):
    sleep(0.5)
    driver.get(href)
    sleep(0.3)
    text_elements = driver.find_element(By.CLASS_NAME, "content").find_elements(By.TAG_NAME, "p")
    return "".join([element.get_attribute("innerText") for element in text_elements])

search = input()
driver = webdriver.Edge("msedgedriver.exe")
get_topic(search, 10, 0.1)



