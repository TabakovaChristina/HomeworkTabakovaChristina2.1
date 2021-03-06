# -*- coding: utf-8 -*-

# Домашняя работа 3.
# Задание: Оформить в виде репозитария на github.
# 1. Написать WSGI сервер который отдает статикой файлы по HTTP при обращении по IP адресу.
# 2. Написать WSGI middleware которое будет вставлять в тело HTML страниц строки следующим образом:
# <html>
# <head>
#  ...
# </head>
# <body>
#   <div class='top'>Middleware TOP</div>
#    ...
#   <div class='botton'>Middleware BOTTOM</div>
# </body>
# </html>

from waitress import serve # Из waitress импортируем серверы.
import os # Модуль предоставляет множество функций для работы с операционной системой.

# Необходимые переменные:
MiddlewareTop = "<div class='top'>Middleware TOP</div>"
MiddlewareBottom =  "<div class='botton'>Middleware BOTTOM</div>"

class WSGI(object):
    def __init__(self, blog):
        self.blog = blog
    def __call__(self, environ, start_response):
        answer = self.request(environ, start_response)[0].decode()
        if answer.find('<body>') > -1:
            # Разделяем с помощью метода split().
            head, body = answer.split('<body>')
            bodyDocument, end = body.split('</body>')
            # Получаем новое тело документа.
            bodyDocument = '<body>'+ MiddlewareTop + bodyDocument + MiddlewareBottom +'</body>'
            return [head + bodyDocument + end]
        else:
            return [MiddlewareTop + answer + MiddlewareBottom]

def blog(environ, start_response):
    pathFile = '.' + environ['PATH_INFO']
    if not os.path.isfile(pathFile):
        pathFile ='./index.html'
    newFile = open(pathFile,'r')
    textFile = newFile.read()
    newFile.close()
    # Формируем ответ:
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [textFile]

request = WSGI(blog)

if __name__ == '__main__':
    from waitress import serve
    serve(request, host='localhost', port=8000)
