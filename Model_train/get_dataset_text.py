
import wikipedia
import wikipediaapi
import os

img_path = "D:/NUS_IntelligentSystem\ISY5002\project\data/train"
dat_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\coplemet_forQA"
lal_path="D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm\labels"
# 列出 img_path 路径下的所有文件和文件夹。
labels = os.listdir(img_path)
# Convert all labels to lowercase
lowercase_labels = [label.lower() for label in labels] #wiki is lower senstive ,
print(lowercase_labels)

user_agent = "e1221753@u.nus.edu"
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

def get_wiki_info(label):
    page_py = wiki_wiki.page(label)
    return page_py.text if page_py.exists() else "Page not found"

# for label in lowercase_labels:  #seacrch first time
#     info = get_wiki_info(label)
#     # Save the information into a text file
#     with open(f"{dat_path}/{label}.txt", "w", encoding="utf-8") as file:
#         file.write(info)

not_found_labels = []

# find some null file for muanual search
for filename in os.listdir(dat_path):

    filepath = os.path.join(dat_path, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        if content.strip() == "Page not found":

            not_found_labels.append(os.path.splitext(filename)[0])
            #delete the null file


print("this numbber of first not find\n")
print(len(not_found_labels))  #184 not found
print(not_found_labels)

#I find if abbotts babbler changed to abbott's babbler, we can find information,. so change these lable and search again

def insert_s(label):
    words = label.split(' ')

    for i in range(len(words)):
        if words[i].endswith('s'):
            new_label = ' '.join(words[:i] + [words[i][:-1] + "'s"] + words[i + 1:])
            return new_label
        else:
            return label


second_labels=[]
for label in not_found_labels:
    second_labels.append(insert_s(label))
print("this is second labels")
print(second_labels)

# for i in  range(len(second_labels)):  #seacrch second time
#     info = get_wiki_info(second_labels[i])
#     # Save the information into a text file
#     with open(f"{dat_path}/{second_labels[i]}.txt", "w", encoding="utf-8") as file:
#         file.write(info)

third_not_found=[]
for filename in os.listdir(dat_path):

    filepath = os.path.join(dat_path, filename)
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        if content.strip() == "Page not found":

                third_not_found.append(os.path.splitext(filename)[0])
                #delete the null file


print("this numbber of third not find\n")
print(len(third_not_found))  #117 not found
print(third_not_found)


#剩下118个，不太规则，来手动吧
def manual(wikilable,store_label):

    info = get_wiki_info(wikilable)
    # Save the information into a text file
    with open(f"{dat_path}/{store_label}.txt", "w", encoding="utf-8") as file:
        file.write(info)

manual_list=["Oystercatcher ", "Ashy thrush","Crested ibis","Oriental dollarbird","Asian green bee-eater","European shag",
             "Azure-breasted pitta","Tanager","Band-tailed guan","Pita Pinta Asturiana","Black-breasted puffbird","Black cockatoo",
             "Egretta","Black-headed parrot","Black-winged stilt","Corn crake","Bushtit","Sparrow","Dunnock","Wedge-tailed shearwater",
             "Dunnock ","Woodpecker","Cuckoo","Blue-throated piping guan","Blue-throated toucanet","Bornean peacock-pheasant",
             "Brandt's cormorant","Brown creeper","Brown noddy","Cape May warbler"

]
write=[]
# text= '\n'.join(third_not_found[:30])
# text2='\n'.join(third_not_found[30:60])
# text3='\n'.join(third_not_found[60:90])
# text4='\n'.join(third_not_found[90:117])
#
# with open(f"{dat_path}/manual1 .txt", 'w') as file:
#     # 将文本写入文件
#     file.write(text)
# with open(f"{dat_path}/manual2 .txt", 'w') as file:
#     # 将文本写入文件
#     file.write(text2)
# with open(f"{dat_path}/manual3 .txt", 'w') as file:
#     # 将文本写入文件
#     file.write(text3)
# with open(f"{dat_path}/manual4 .txt", 'w') as file:
#     # 将文本写入文件
#     file.write(text4)
with open("D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm/after_correction\manual2_done .txt", 'r') as file:
    # 读取文件的每一行，并将每一行作为一个元素存入列表
    lines = file.readlines()
manual2=[line.strip() for line in lines]

try:
    index = manual2.index("Woodhouse's scrub jay")
    # 保留 '正确的名字' 及其之后的所有元素
    manual2 = manual2[index:]
    # print(result_list)
except ValueError:
    # 如果 '正确的名字' 不在列表中，会抛出 ValueError
    print('元素 "正确的名字" 不在列表中')

with open("D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm/after_correction\manual3 .txt", 'r') as file:
    # 读取文件的每一行，并将每一行作为一个元素存入列表
    lines = file.readlines()
manual3=[line.strip() for line in lines]

try:
    index = manual3.index("Knob-billed duck")
    # 保留 '正确的名字' 及其之后的所有元素
    manual3= manual3[index:]
    # print(result_list)
except ValueError:
    # 如果 '正确的名字' 不在列表中，会抛出 ValueError
    print('元素 "正确的名字" 不在列表中')

with open("D:/NUS_IntelligentSystem\ISY5002\project\data/bird_llm/after_correction\manual4.txt", 'r',encoding='utf-8') as file:
    # 读取文件的每一行，并将每一行作为一个元素存入列表
    lines = file.readlines()
manual4=[line.strip() for line in lines]

try:
    index = manual4.index("Liocichla ripponi")
    # 保留 '正确的名字' 及其之后的所有元素
    manual4= manual4[index:]
    # print(result_list)
except ValueError:
    # 如果 '正确的名字' 不在列表中，会抛出 ValueError
    print('元素 "正确的名字" 不在列表中')

# print(manual4)

# for i in range(len(manual_list)):
#     manual(manual_list[i],manual_list[i])
# for i in range(len(manual2)):
#     manual(manual2[i],manual2[i])
# for i in range(len(manual3)):
#     manual(manual3[i],manual3[i])
# for i in range(len(manual4)):
#     manual(manual4[i],manual4[i])
#after this remain 2

#do this mamunallly
# manual("Redhead (bird)","Redhead (bird)")
# manual("Rough-legged buzzard","Rough-legged buzzard")
#after this finished

#delete the not found labels in lowercaselabels
# for file_name in not_found_labels:
#     try:
#         file_path = os.path.join(dat_path, file_name + '.txt')  # 确保文件名有正确的路径和扩展名
#         os.remove(file_path)
#         print(f"File {file_name}.txt removed successfully")
#     except Exception as e:
#         print(f"Cannot delete {file_name}.txt: {e}")

# old_labels = os.listdir(dat_path)
# print(old_labels)
# #remove the .txt
# labels = [os.path.splitext(label)[0] for label in old_labels]
# print(labels)
# #witre into the lable file
# with open(f"{lal_path}/labels.txt", "w", encoding="utf-8") as file:
#     for label in labels:
#         file.write(label + '\n')


#go on shit code
repiar_labels=['African oystercatcher.txt',
               'Auckland Shag.txt', 'Banded pitta.txt',
               'Black-faced spoonbill.txt', 'Black-necked stilt.txt', 'Black-tailed crake.txt', 'Black-throated blue warbler.txt', 'Black-throated bushtit.txt', 'Black-throated huet-huet.txt', 'Black-vented shearwater.txt', 'Blackburnian warbler.txt', 'Blond-crested woodpecker.txt', 'Blue coua.txt', 'Grey go-away-bird.txt', 'Nuthatch.txt', 'Scarlet-faced liocichla.txt','Frigatebird.txt','teal duck.txt']
repaired_labels = [label.replace('.txt', '') for label in repiar_labels]
print(repaired_labels)
# for i in range(len(repaired_labels)):
#     info=get_wiki_info(repaired_labels[i])
#     with open(f"{dat_path}/{repaired_labels[i]}.txt", "w", encoding="utf-8") as file:
#         file.write(info)





print(not_found_labels)#delet
for file_name in not_found_labels:
    try:
        file_path = os.path.join(dat_path, file_name + '.txt')  # 确保文件名有正确的路径和扩展名
        os.remove(file_path)
        print(f"File {file_name}.txt removed successfully")
    except Exception as e:
        print(f"Cannot delete {file_name}.txt: {e}")