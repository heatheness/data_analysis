# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

"""пишем web-server как-то так """

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html, charset = utf-8' )
        self.end_headers()
        # self.wfile.write('Hello World!')
        self.wfile.write("""
        Hello World!
        <form method=POST>
            <input type=submit value = "OK"/>
        </form>
        """)
        return

    def do_POST(self):

        """не работает"""

        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT-TYPE':self.headers['Content-type']})
        print form.getvalue("""
        <form method = POST>
            <input type=hidden name="n" value="0"/>
            <input type=submit value="RE"/ >
        </form>
        """)


        self.send_response(301)
        self.send_header('Location','/')
        self.end_headers()

        return


    """/experiment=121 - это наш запрос, показываем этот эксперимент, пользователь выбирает, POST возвращает результат
    по 121, записывает его в hiddenpoint , а потом перекидывает на 122"""


server = HTTPServer(('',8080), MyHandler)

try:
    server.serve_forever()
except:
    server.socket.close()


