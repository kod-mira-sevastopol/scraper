import asyncio
import datetime
import os
import re
from typing import Optional
from parse_hh_data import download, parse
import docx2txt
from pdfminer.high_level import extract_text
from striprtf.striprtf import rtf_to_text

import src.services.modal_model_service as modal
import src.services.analyze_service as analyze

from src.models.education import Education
from src.models.resume import Resume
from src.models.stack import Stack
from src.models.contact import Contact
from src.models.jobs import Job
from src.models.person import Person
from src.models.achievements import Achievement

class Scraber:
    @staticmethod
    async def scrab_url(resume_url:str) -> Optional[str]:
        path_parts = resume_url.split('/')
        resume_id = path_parts[-1]

        hh_resume = download.resume(resume_id)
        hh_resume = parse.resume(hh_resume)

        return await Scraber.__scrab(hh_resume)

    @staticmethod
    async def scrab_file(file) -> Optional[str]:
        """
        Scrab a file based on its format.

        Args:
        file: The file to be scrapped.

        Returns:
        The scrapped content if successful, None otherwise.
        """
        path = Scraber.save_file(file)
        format = file.filename.split('.')[-1].lower()

        match format:
            case 'docx':
                return await Scraber.__scrab_docx(file)
            case 'doc':
                return await Scraber.__scrab_docx(file)
            case 'rtf':
                return await Scraber.__scrab_rtf(path)
            case 'pdf':
                return await Scraber.__scrab_pdf(path)

        return None

    @staticmethod
    def save_file(file):
        now = datetime.datetime.now()
        format = file.filename.split('.')[-1].lower()

        filename = now.strftime("%Y%m%d%H%M%S%f") + f'.{format}'

        folder_path = "files"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        path = os.path.join(folder_path, filename)
        file.save(path)

        return path

    @staticmethod
    async def __scrab_pdf(path) -> Optional[str]:
        """
        Scrab a PDF file.

        Args:
        file: The PDF file to be scrapped.

        Returns:
        The scrapped content if successful, None otherwise.
        """
        text = extract_text(path)
        return await Scraber.__scrab(text)

    @staticmethod
    async def __scrab_rtf(path) -> Optional[str]:
        with open(path, 'r') as file:
            encoded_rtf = file.read()

        text = rtf_to_text(encoded_rtf)
        print(text)
        return await Scraber.__scrab(text)

    @staticmethod
    async def __scrab_docx(file) -> Optional[str]:
        """
        Scrab a DOCX file.

        Args:
        file: The DOCX file to be scrapped.

        Returns:
        The scrapped content if successful, None otherwise.
        """
        text = docx2txt.process(file)
        result = await Scraber.__scrab(text)

        return result

    @staticmethod
    async def __scrab(data) -> Optional[str]:
        """
        Scrab generic data.

        Args:
        data: The data to be scrapped.

        Returns:
        The scrapped content if successful, None otherwise.
        """
        count_retry = 1
        count_trim = 0

        while count_retry > 0:
            try:
                data = data.replace('"', "").replace('»', '').replace('«', '')
                result = await Scraber.get_scrabed_model(data[0:(len(data))-(10*count_trim)])
                print(result)
                return result
            except Exception as e:
                print(e)

            count_retry -= 1
            count_trim += 1


        return {'result':'Document cant\'t be scrapped.'}

    @staticmethod
    async def get_scrabed_model(data):
        json = await modal.ModalModelService.modal_scrab(data)
        json['choices'][0]['message']['content'] = (json['choices'][0]['message']['content'].replace("'", '"')
                                                    .replace('\n', '')).replace('\\"', '"').replace('\\', '\\\\')

        print(json['choices'][0]['message']['content'])

        result = Resume.parse_json(json['choices'][0]['message']['content'])
        result = result.to_dict()

        analyzer = analyze.AnalyzeService(data, result)
        (skills) = analyzer.analyze()

        print(skills)
        result['skills'] = [skill.__dict__ for skill in skills]
        return result

    @staticmethod
    def scrabed_preview():
        person = Person("Константин", "Константинович", "Руднев", "29.09.2000", 49)
        contact = Contact("test@gmail.com", '+7(949)313-34-29', '@pulseneon')
        stacks = [Stack('yolov5'), Stack('SpringBoot'), Stack('Asp.Net'),
                  Stack('FastApi'), Stack('Python')]
        educations = [Education('Донецкий национальный технический университет', 'Высшее учебное заведение (бакалавр)',
                                'Кафедра программной инженерии им. Фельдмана', '2021', '2025'),
                      Education('Донецкий национальный технический университет', 'Высшее учебное заведение (бакалавр)',
                                'Кафедра программной инженерии им. Фельдмана', '2021', '2025') ]
        jobs = [Job('Sberbank', 'Junior', 'Писал то-то то-то тогда-то тогда-то так-то так-то',
                    'Москва', '29.09.2000', '13.12.2001')]
        achievements = [Achievement('Усовершенствовал навыки адаптивной верстки, обеспечивая корректное отображение сайтов на различных устройствах (ПК, планшеты, смартфоны).'),
                        Achievement('Использовать Fetch API как современную альтернативу XMLHttpRequest.')]


        resume = Resume(hh_url='hh.rudnev.com', contact=contact, stack=stacks,
                        educations=educations, achievements=achievements, jobs=jobs, person=person)

        result = resume.to_dict()

        return result

def divide_string(s):
    half = len(s) // 2
    result = []

    result.append(s[:half])
    result.append(s[half:])

    return result