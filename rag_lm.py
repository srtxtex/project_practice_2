import re
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
import openai
import tools as tls
import os
import re
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup, Tag
from dotenv import load_dotenv


load_dotenv()

LL_MODEL = os.environ.get("LL_MODEL")

def html_to_text(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    strings = []

    title = soup.find(id ='title-text')
    if type(title) == Tag:
       title_text = title.get_text(strip=True)
       strings.append(title_text)

    content = soup.find(id ='content')  

    if type(content) == Tag:
      main_content = content.find(id='main-content')
      if type(main_content) == Tag:
        string = main_content.get_text(' ', strip=True)
        string = re.sub(r'\s+', ' ', string)
        string = re.sub(r'\n+', '\n', string)
        string = re.sub(r'\r+', '\r', string)
        string = re.sub(r'•+', ' ', string)
        if string != ' ' and string != '':
          strings.append(string)  


    full_text = '\n'.join(strings)
    return full_text



def parse_html():
    dir = '/content/pek'
    source_chunks = []
    splitter = CharacterTextSplitter(separator=" ",  chunk_size=1024, chunk_overlap=512)
    # splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "(?<=\. )", ". "],  chunk_size=1024, chunk_overlap=512)

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".html"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    html_content = f.read()
                    text = html_to_text(html_content)
                    for chunk in splitter.split_text(text):
                        source_chunks.append(Document(page_content=chunk, metadata={'source': file}))

    return source_chunks

def create_index_db(source_chunks):
    model_id = LL_MODEL
    # model_kwargs = {'device': 'cpu'}
    model_kwargs = {'device': 'cuda'}
    embeddings = HuggingFaceEmbeddings(
      model_name=model_id,
      model_kwargs=model_kwargs
    )

    db = FAISS.from_documents(source_chunks, embeddings)
    return db



def get_message_content(topic, index_db, k_num):
    # Поиск релевантных отрезков из базы знаний
    docs = index_db.similarity_search(topic, k = k_num)
    message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\n#### Document excerpt №{i+1}####\n' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
    sources = re.sub(r'\n{2}', ' ', '\n '.join([doc.metadata['source'] + '\n' for i, doc in enumerate(docs)]))
    print(f"message_content={message_content}")
    return message_content, sources


def answer_index(system, topic, message_content, temp):
    openai.api_type = "open_ai"
    openai.api_base = "http://localhost:5000/v1"
    openai.api_key = "no need anymore"

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Here is the document with information to respond to the client: {message_content}\n\n Here is the client's question: \n{topic}"}
    ]


    completion = openai.ChatCompletion.create(
        model='no need anymore',
        messages=messages,
        temperature=temp
    )


    answer = completion.choices[0].message.content

    return answer  # возвращает ответ

# Загружаем текст Базы Знаний из файла
source_chunks = parse_html()
# Создаем индексную Базу Знаний
index_db = create_index_db(source_chunks)
# Загружаем промпт для модели, который будет подаваться в system
# system = 'Ты сотрудник поддержки компании занимающейся логистикой, тебя зовут пекGPT и ты отвечаешь на вопросы сотрудников в чате. У тебя есть документ со всеми материалами о внутренних процессах и регламентах. Не упоминай документ или его отрывках при ответе, сотрудник ничего не должен знать о документе, по которому ты отвечаешь. Ответь так, чтобы сотрудник решил свой вопрос. То чего нет в документе мы не можем это ответить. Не употребляй фразы вида “По нашему документу”, “в нашем документе”, “в документе с материалами”.'

system = 'Ты сотрудник поддержки компании занимающейся логистикой, тебя зовут пекGPT и ты отвечаешь на вопросы сотрудников в чате. У тебя есть документ со всеми материалами о внутренних процессах и регламентах. Ответь так, чтобы сотрудник решил свой вопрос. То чего нет в документе мы не можем это ответить. Не употребляй фразы вида “По нашему документу”, “в нашем документе”, “в документе с материалами”.'




def answer_user_question(topic):
    # Ищем реливантные вопросу чанки и формируем контент для модели, который будет подаваться в user
    message_content, sources = get_message_content(topic, index_db, k_num=5)
    # Делаем запрос в модель и получаем ответ модели
    answer = answer_index(system, topic, message_content, temp=0.1)
    answer = answer + '\n' + sources
    return answer, message_content

if __name__ == '__main__':
    topic ="Что делать, если клиент отказывается получения сопроводительных документов? "
    answer, message_content = answer_user_question(topic)
    print(f'answer={answer}')