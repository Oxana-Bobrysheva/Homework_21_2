import os.path
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """A special class that is responsible for processing
    incoming HTTP requests"""

    def do_GET(self):
        # Определяем путь к HTML-файлу
        filename = os.path.join("src", "contacts.html")

        # Читаем HTML-файл
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        # Получаем длину данных, переданных в запросе
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)  # Читаем данные

        # Декодируем данные
        parsed_data = urllib.parse.parse_qs(post_data.decode("utf-8"))

        # Печатаем данные в консоль
        print("Полученные данные:", parsed_data)

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Data received")


def run(server_class=HTTPServer, handler_class=MyServer, port=serverPort):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
