import nltk
from nltk import sent_tokenize
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration,AutoTokenizer, AutoModelForSeq2SeqLM
os.environ['TRANSFORMERS_CACHE'] = "D:/NUS_IntelligentSystem\ISY5002\project/testapp\gittest/bird_species_guide-main\our_model_train/transfomer_load"     #change transformer cache path

# model = T5ForConditionalGeneration.from_pretrained('t5-small')
# tokenizer = T5Tokenizer.from_pretrained('t5-small')

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

# folder_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm/new_for_lables"
# result_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\QA_pairs"

result_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\STD_QA"
folder_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\coplemet_forQA"

documents = {}
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def clean_text(text):
    # Remove <pad> and </s> tokens
    cleaned_text = text.replace("<pad> ", "").replace("</s>", "")
    return cleaned_text

def generate_question(sentence):
    # Simple rule: if 'is' in sentence, replace the first occurrence of 'is' with 'What is' and add '?'
    if 'is' in sentence:
        return sentence.replace('is', 'What is', 1) + '?'
    # Add more rules as needed
    return None

def generate_question_byT5(text):
    # Tokenize the text and generate question
    input_ids = tokenizer.encode('generate question: ' + text, return_tensors='pt')
    output = model.generate(input_ids)
    question = tokenizer.decode(output[0])
    return question


def find_empty_files(path):
    """
    在指定的路径中查找空的文本文件。

    参数:
        path (str): 文件夹路径。

    返回:
        empty_files (list of str): 空文件的名字列表。
    """
    empty_files = []

    # 遍历路径下的所有文件
    for root, dirs, files in os.walk(path):
        for file in files:
            # 检查文件扩展名是否为 .txt
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                # 检查文件是否为空
                if os.path.getsize(file_path) == 0:
                    empty_files.append(file)

    return empty_files


def find_matching_files(labels, folder_path):
    """
    在指定的文件夹中查找与标签匹配的文件。

    参数:
        labels (list of str): 文件标签列表。
        folder_path (str): 文件夹路径。

    返回:
        int or list of str: 如果找到匹配的文件，返回它们的数量。如果没有找到匹配的文件，返回所有不匹配标签的列表。
    """
    # 移除文件名中的 ".txt" 后缀
    labels_without_extension = [label.replace('.txt', '') for label in labels]

    # 获取文件夹中的所有文件名（不带路径和扩展名）
    files_in_folder = [os.path.splitext(file)[0] for file in os.listdir(folder_path)]

    # 查找与标签匹配的文件
    matching_files = [label for label in labels_without_extension if label in files_in_folder]

    # 如果找到匹配的文件，返回它们的数量
    # if matching_files:
    #     return len(matching_files)


    non_matching_labels = [label for label in labels_without_extension if label not in files_in_folder]
    return non_matching_labels



#
# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a text file
    if filename.endswith('.txt'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            document_content = file.read()
            # Store the content in the dictionary
            documents[filename] = document_content


#tesing
# print(documents["abbotts babbler.txt"])  #

# sentences = sent_tokenize(documents["abbotts babbler.txt"])
# qa_pairs = []
# for sentence in sentences:
#     question = generate_question_byT5(sentence)
#     if question:  # If a question is generated
#         qa_pairs.append((question, sentence))
#
# # Print generated QA pairs
# for q, a in qa_pairs:
#     print(f"Question: {q}")
#     print(f"Answer: {a}")
#     print('---')

#
# #start run all files
# if not os.path.exists(result_path):
#     os.makedirs(result_path)
#
# for filename, content in documents.items():
#     # Tokenize content into sentences
#     sentences = sent_tokenize(content)
#
#     # Initialize list for storing QA pairs
#     qa_pairs = []
#
#     # Generate QA pairs for each sentence
#     for sentence in sentences:
#         question = generate_question_byT5(sentence)
#         if question:  # If a question is generated
#             # You might want to clean up the generated question here
#             cleaned_question = clean_text(question)
#             qa_pairs.append((cleaned_question, sentence))
#
#     # Convert QA pairs to string
#     qa_string = ""
#     for q, a in qa_pairs:
#         qa_string += f"Question: {q}\nAnswer: {a}\n---\n"
#
#     # Write QA pairs to new file
#     result_file_path = os.path.join(result_path, filename)
#     with open(result_file_path, 'w', encoding='utf-8') as result_file:
#         result_file.write(qa_string)
#
#     # Print message to indicate progress
#     print(f"Processed and saved QA pairs for {filename}")

#
if __name__ == "__main__":
    pth1="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\STD_QA"
    empty= find_empty_files(pth1)
    print(empty) #find thoese empty files
#     repiar_labels = ['African oystercatcher.txt',
#                      'Auckland Shag.txt', 'Banded pitta.txt',
#                      'Black-faced spoonbill.txt', 'Black-necked stilt.txt', 'Black-tailed crake.txt',
#                      'Black-throated blue warbler.txt', 'Black-throated bushtit.txt', 'Black-throated huet-huet.txt',
#                      'Black-vented shearwater.txt', 'Blackburnian warbler.txt', 'Blond-crested woodpecker.txt',
#                      'Blue coua.txt', 'Grey go-away-bird.txt', 'Nuthatch.txt', 'Scarlet-faced liocichla.txt',
#                      'Frigatebird.txt', 'Teal duck.txt']
#
#     # a=find_matching_files(repiar_labels, pth1)
#     # print(a) #find thoese not found files, all file matches start next step


