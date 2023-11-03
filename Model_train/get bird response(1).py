import requests
import pandas as pd
import time
import os

API_KEY = "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"
url = "https://api.openai.com/v1/chat/completions"
dat_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm/new_for_lables"
reponse_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\gpt_response"
# 获取所有txt文件的文件名
txt_files = [filename for filename in os.listdir(dat_path) if filename.endswith(".txt")]
# print(txt_files)
# 创建一个空的DataFrame用于保存结果
columns = ["name", "taxonomy", "description", "voice", "distribution", "behaviour", "breeding", "feeding",
           "predators", "cultural_importance", "status", "reference"]
df = pd.DataFrame(columns=columns)

# 创建一个用于记录跳过文件的列表
skipped_files = []

# 定义一个函数来获取鸟类的信息
def get_bird_info(bird_name, bird_text):
    # 将输入分为多个片段，每个片段长度不超过模型最大上下文长度
    max_context_length = 4096  # 模型的最大上下文长度
    prompts = []
    while len(bird_text) > max_context_length:
        prompt_part = bird_text[:max_context_length]
        bird_text = bird_text[max_context_length:]
        prompts.append(prompt_part)
    prompts.append(bird_text)
    
    info_parts = []
    
    for i, prompt in enumerate(prompts):
        prompt_message = [{"role": "user", "content": f"{prompt}. \n Please give me taxonomy, description, voice, distribution, behaviour, breeding, feeding, predators, cultural importance, status of this kind of birds based on above information."}]
        
        response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"},
                                 json={'messages': prompt_message, 'model': 'gpt-3.5-turbo'})
        
        if response.status_code == 200:
            info = response.json()["choices"][0]["message"]["content"]
            info_parts.append(info)
        else:
            # API调用失败，打印错误信息并跳过当前文件
            print(f"Error response for '{bird_name}.txt' (part {i + 1}):")
            print(response.text)
            skipped_files.append(f"Error response for '{bird_name}.txt' (part {i + 1})")
            return None
    
    info = "\n".join(info_parts)
    # file_name = f"D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\gpt_response/{bird_name}_response.txt"
    file_name=os.path.join(reponse_path, f"{bird_name}_response.txt")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(info)
    print(info)
    return [bird_name] + info.split("\n")

# 循环处理每个txt文件
for txt_file in txt_files:
    bird_name = os.path.splitext(txt_file)[0]
    
    # 读取鸟类信息
    file_path1 = os.path.join(dat_path, txt_file)
    with open(file_path1, "r", encoding="utf-8") as file:
        bird_text = file.read()
        bird_info = get_bird_info(bird_name, bird_text)
    
    # time.sleep(2)  # 2秒的延迟时间，可以根据需要调整

# 保存跳过的文件列表到文本文件
file_path = os.path.join(reponse_path, "skipped_files.txt")
with open(file_path, "w", encoding="utf-8") as skipped_file:
    skipped_file.write("\n".join(skipped_files))
