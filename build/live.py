from http.server import SimpleHTTPRequestHandler
from socketserver import ForkingTCPServer
import os
import mimetypes
import urllib.parse

from build.rendering import render_markdown_file


def serve_live(host, port):
    while True:
        try:
            httpd = ForkingTCPServer((host, port), LiveServer)
            break
        except OSError:
            print(f"port {port} in use...")
            port += 1

    try:
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


class LiveServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.unquote(self.path)
        print(f"serving {p}")

        if p.endswith("/"):
            p += "index.html"

        match p.split("/")[1:]:
            case ["static", *parts]:
                return self.send_static(os.path.join(*parts))
            case ["favicon.ico"]:
                return self.send_static("favicon.ico")
            case [*path, file] if file.endswith(".html"):
                return self.serve_markdown(path, file)

    def serve_markdown(self, path: list[str], file: str):
        result = render_markdown_file(os.path.join("content", *path, file[:-5] + ".md"))

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(result.encode())

    def send_static(self, path: str):
        static_path = os.path.join("static", path)
        if not os.path.exists(static_path):
            return self.send_404()

        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(path)[0] or "text/plain")
        self.end_headers()
        with open(static_path, "rb") as f:
            self.copyfile(f, self.wfile)

    def send_404(self):
        self.send_response(200)
        self.send_header(
            "Content-Type", mimetypes.guess_type(self.path)[0] or "text/plain"
        )
        self.end_headers()
