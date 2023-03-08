
import os.path
import os
from fileinput import filename
import json
import openai

#Апи ключ openai
openai.api_key ="YOUR API KEY HERE!"
#Файл в который будет записываться история сообщений
FileName = "example.json"

def Dialog():
    Task = input("You > ")
    try:
        ##Этот блок проверяет существует ли файл или его требуется создать
        ##Так же используется для правильного его начала чтобы сохранить структуру
        if os.path.isfile(FileName):
            print(f"[+]Файл '{FileName}' существует.")
        else:
            print(f"[!]Файл '{FileName}' не существует, создаю...")
            file = open(FileName, "a", encoding = "utf-8")
            #Перевод в адекватный для json вариант и запись файла введенного пользователем текста
            DumpedTask = json.dumps('"'+Task+'"')
            file.write("""[{"role": "user", "content": """+DumpedTask+"""}\n""")
            file.close()
            #Получение ответа от ChatGPT, дамп, сохранение структуры и запись в файл
            Completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": Task}])
            dumped_answer = json.dumps('"'+Completion.choices[0].message.content+'"')
            #Вывод ответа
            print ("ChatGPT > " + Completion.choices[0].message.content)
            #запись ответа
            with open(FileName, "a",encoding = "utf-8") as modified:
                modified.write(""",{"role": "assistant", "content": """+dumped_answer+'}]\n')
                modified.close()
            Dialog()
        
        #
        #Если файл существует, то идет обработка. 
        #Сохранение порядка скобок 
        with open(FileName, "r",encoding = "utf-8") as original:
            old_data = original.read()
            old_data = old_data.replace(']','')
            old_data = old_data.replace('[','')
            original.close()
        #Запись запроса. Без первый квадратной скобочки, с ней перезапись файла будет с лишней скобочкой
        with open(FileName, "a",encoding = "utf-8") as modified:
            modified.truncate(1)
            dumped_task = json.dumps('"'+Task+'"')
            modified.write(old_data+""",{"role": "user", "content": """+dumped_task+'}]\n')
            modified.close()
        #Загрузка данных из файла
        with open(FileName, "r",encoding = "utf-8") as file:
            data = json.load(file)
        Completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=data)

        #Дамп текста ответа, надо чтобы спецсимволы не ломали json строки
        dumped_answer = json.dumps('"'+Completion.choices[0].message.content+'"')
        #Сохранение порядка скобок 
        with open(FileName, "r",encoding = "utf-8") as original:
            old_data = original.read()
            old_data = old_data.replace(']','')
            old_data = old_data.replace('[','')
            original.close()
        #Перезапись файла с добавлением ответа
        with open(FileName, "a",encoding = "utf-8") as modified:
            modified.truncate(1)
            modified.write(old_data + """,{"role": "assistant", "content": """+dumped_answer+'}]\n')
            modified.close()

        #Вывод ответа
        print("ChatGPT > " + Completion.choices[0].message.content)


    except Exception as error:#Этот случай наступает при ошибке
        print ("[-]"+str(error))
    Dialog()



Dialog()
