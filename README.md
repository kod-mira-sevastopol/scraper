# Scrapper-api service 
 
Handle a resume file sent via a POST method or an HH URI and return a parsed ResumeModel.

### Библиотеки:
﻿1. aiohttp
2. docx2txt
3. Flask
4. parse-hh-data (self-rewritten)
5. pdfminer.six
6. SQLAlchemy

### Инструкция:
1. Install requirements ```pip install requirements.txt```
2. Start server ```pytnon app.py```
3. Send curl

```
   curl --location '{hostname}/resume/scrab' \
   --form 'file={filepath}'
```

![image](https://github.com/kod-mira-sevastopol/scraper/assets/159879758/c85afa19-c689-4058-b411-de710834a701)
