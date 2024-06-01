import csv
import os

from docx2txt import docx2txt

def format_dt():
    folder = 'dataset'
    file_contents = []

    for filename in os.listdir(folder):
        if filename.endswith(".docx"):
            filename = os.path.join(folder, filename)
            result = scrap_file(filename)
            file_contents.append(result)

    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerows(file_contents)


def scrap_file(path):
    text = docx2txt.process(path)
    return scrap(text)


def scrap(text):
    sentences = text.split('\n')
    result = [' '.join(filter(None, sentences[i:j])) for i in range(len(sentences)) for j in range(i + 1, len(sentences) + 1)
              if '' not in sentences[i:j]]
    result = [element.strip() for element in result]
    return result

if __name__ == '__main__':
    format_dt()