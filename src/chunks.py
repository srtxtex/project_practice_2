import re
import os
import pickle
from bs4 import BeautifulSoup, Tag
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document


def html_to_text(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    strings = []

    title = soup.find(id="title-text")
    if isinstance(title, Tag):
        title_text = title.get_text(strip=True)
        strings.append(title_text)

    content = soup.find(id="content")

    if isinstance(content, Tag):
        main_content = content.find(id="main-content")
        if isinstance(main_content, Tag):
            string = main_content.get_text(" ", strip=True)
            string = re.sub(r"\s+", " ", string)
            string = re.sub(r"\n+", "\n", string)
            string = re.sub(r"\r+", "\r", string)
            string = re.sub(r"•+", " ", string)
            if string != " " and string != "":
                strings.append(string)

    full_text = "\n".join(strings)
    return full_text


def parse_html():
    dir = "./pek"
    source_chunks = []
    splitter = CharacterTextSplitter(
        separator=" ", chunk_size=1024, chunk_overlap=512)

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".html"):
                with open(
                        os.path.join(root, file), "r", encoding="utf-8") as f:
                    html_content = f.read()
                    text = html_to_text(html_content)
                    for chunk in splitter.split_text(text):
                        source_chunks.append(
                            Document(
                                page_content=chunk, metadata={"source": file})
                        )

    return source_chunks


if __name__ == "__main__":
    source_chunks = parse_html()
    with open("./data/source_chunks.pkl", "wb") as file:
        pickle.dump(source_chunks, file)
