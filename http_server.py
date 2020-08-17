"""A simple Python HTTP server to show results."""

import http.server
import json
import os


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Handle all HTTP requests."""

    def __set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def __send_results(self):
        dirs = os.listdir("results")
        return [os.path.join("results", dir) for dir in dirs
                if not os.path.isfile(os.path.join("results", dir))]

    def do_GET(self):
        """Handle GET requests."""
        path = self.path
        if path.startswith("/web") or path.startswith("/results"):
            return super().do_GET()
        self.__set_headers()
        ret = {
            "msg": "not found path"
        }
        if path == "/dirs":
            dirs = self.__send_results()
            ret = {
                "dirs": dirs
            }
        ret = bytes(json.dumps(ret), "utf-8")
        self.wfile.write(ret)


def main():
    """Run the main HTTP server."""
    server_address = ("", 8000)
    httpd = http.server.HTTPServer(server_address, HTTPHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
