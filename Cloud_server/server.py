#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

IP = '172.30.0.4'
PORT = 50000
sensor_data = []


# Class for handling each HTTP requests in separate thread
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


# Class for handling incoming HTTP requests
class server_handler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_GET(self):
        self._set_response()
        file_string = open('index.html', 'rb').read()
        self.wfile.write(file_string)
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Gets the size of data
        data = self.rfile.read(content_length)
        self._set_response()

        html_file = open("index.html", "w")
        for i in range(len(html_string)):
            if html_string[i] == '        <script>\n':
                the_data = data.decode()
                sensor_data.append(the_data)
                data_as_html = '<p>' + the_data + '</p>\n'
                html_string.insert(i, data_as_html)
                for text in html_string:
                    html_file.write(text)
                break
        html_file.close()
        self.send_header('Content-length', content_length)
        self.wfile.write(self.headers.as_bytes() + data)
        return


# Read the HTML file for file update during POST request
html_file = open("index.html", "r")
html_string = html_file.readlines()
html_file.close()

server = ThreadedHTTPServer((IP, PORT), server_handler)
print("Server started")
server.serve_forever()