### Guardian-Scraper
###### This is a Scrpy project to crawl https://www.theguardian.com/international and save it in MongoDB
##### 1- download the repo
##### 2- download and install  python3.6, pip install virtualenv
##### 3- open cmd and cd to "/path/to/downloaded/repo/"
```
example: cd C:\Users\<user>\OneDrive\Documents\Guardian-Scraper
```
##### 4- virtualenv -p "/path/to/installed/python.exe"  venv
```
example: virtualenv -p "C:\Users\<user>\AppData\Local\Programs\Python\Python36\python.exe"  venv
```
##### 5- active venv
```
venv\scripts\activate
```
##### 6- Install the required packages
```
pip install -r requirements.txt
```
##### 7- run scrpy
```
scrapy crawl guardian
```
