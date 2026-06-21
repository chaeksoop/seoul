import http.server
import socketserver
import os

PORT = 8000
DIR = os.path.dirname(os.path.abspath(__file__))

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def translate_path(self, path):
        p = super().translate_path(path)
        return os.path.join(DIR, os.path.relpath(p, os.getcwd()))

if __name__ == '__main__':
    os.chdir(DIR)
    with socketserver.TCPServer(('0.0.0.0', PORT), NoCacheHandler) as srv:
        print(f'Serving no-cache at http://0.0.0.0:{PORT}')
        srv.serve_forever()
