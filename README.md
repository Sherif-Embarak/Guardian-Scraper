## Guardian scraper and API
###### This is a Scrpy project to crawl https://www.theguardian.com/international and save it in MongoDB
### Installation
##### 1- download the repo
##### 2- download and install  python3.6, pip install virtualenv, (Mongodb shell for local, Mongo Atlas for Cloud)
##### 3- open cmd and cd to "/path/to/downloaded/repo/"
```
example: $ cd C:\Users\<user>\OneDrive\Documents\Guardian-Scraper
```
##### 4- virtualenv -p "/path/to/installed/python.exe"  venv
```
example: $ virtualenv -p "C:\Users\<user>\AppData\Local\Programs\Python\Python36\python.exe"  venv
```
##### 5- active venv
```
$ venv\scripts\activate
```
##### 6- Install the required packages
```
$ pip install -r requirements.txt
```

### Run Guardian-Scraper
```
$ scrapy crawl guardian
```

### Run Guardian-API
```
$ flask run 
(optional : $ flask run -h localhost -p <port number>)
Or: $ python app.py
```
####  Guardian-Flask-API Usage:
###### http://127.0.0.1:5000/article?query=(word_to_search)&return_list='list_of_fields_to_return(separate_by_comma)'&limit=<int>(maximum_number_of_returned_objects_by_defult_10)
```
http://127.0.0.1:5000/article?query=accept&return_list=article_txt,article_writer&limit=3
```
##### The available fields is:
```python
fields= ['article_url', 'article_txt', 'article_title', 'article_writer', 'article_caption', 'article_time','category', 'subcategory_name', 'page_name']
```
####  Change Mongo Local from/to Atlas:
###### change MONGO_URI in settings.py
```python
#MONGO_URI = 'mongodb://localhost:27017/'
MONGO_URI = 'mongodb://<user>:<password>@<cluster>.mongodb.net:27017/?ssl=true&replicaSet=atlas-13yas1-shard-0&authSource=admin&retryWrites=true&w=majority'
```
you can contact me "sherif.embarak@gmail.com" to send you Mongodb Atlas URI(for test)
