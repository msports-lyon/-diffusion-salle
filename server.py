#!/usr/bin/env python3
"""
Serveur local pour diffusion vidéo en salle
Lancez ce script, puis ouvrez http://localhost:8080 dans votre navigateur.
Les télés ouvrent l'URL affichée (ex: http://192.168.1.XX:8080/tv)
"""

import os
import socket
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8080
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
VIDEO_PATH = os.path.join(UPLOAD_DIR, 'current_video')

os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

class VideoHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Silencer les logs trop verbeux
        if args and ('GET /video' in str(args[0]) or 'GET /tv' in str(args[0])):
            return
        print(f"  [{self.address_string()}] {format % args}")

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html; charset=utf-8')

        elif path == '/tv':
            self.serve_file('tv.html', 'text/html; charset=utf-8')

        elif path == '/video':
            self.serve_video()

        elif path == '/status':
            exists = os.path.exists(VIDEO_PATH)
            self.send_json({'ready': exists})

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/upload':
            self.handle_upload()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_upload(self):
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self.send_response(400)
            self.end_headers()
            return

        # Lire la boundary
        boundary = content_type.split('boundary=')[-1].encode()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        # Extraire la vidéo du multipart
        parts = body.split(b'--' + boundary)
        for part in parts:
            if b'Content-Disposition' in part and b'filename=' in part:
                # Trouver le début des données (après double CRLF)
                idx = part.find(b'\r\n\r\n')
                if idx == -1:
                    continue
                data = part[idx + 4:]
                # Retirer le CRLF final
                if data.endswith(b'\r\n'):
                    data = data[:-2]

                # Sauvegarder
                with open(VIDEO_PATH, 'wb') as f:
                    f.write(data)

                size_mb = len(data) / 1024 / 1024
                print(f"  ✅ Vidéo reçue : {size_mb:.1f} Mo → {VIDEO_PATH}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
                return

        self.send_response(400)
        self.end_headers()

    def serve_video(self):
        if not os.path.exists(VIDEO_PATH):
            self.send_response(404)
            self.end_headers()
            return

        size = os.path.getsize(VIDEO_PATH)
        range_header = self.headers.get('Range')

        if range_header:
            # Support du Range (nécessaire pour seek vidéo)
            ranges = range_header.strip().replace('bytes=', '').split('-')
            start = int(ranges[0]) if ranges[0] else 0
            end   = int(ranges[1]) if len(ranges) > 1 and ranges[1] else size - 1
            end   = min(end, size - 1)
            length = end - start + 1

            self.send_response(206)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.send_header('Content-Length', str(length))
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            with open(VIDEO_PATH, 'rb') as f:
                f.seek(start)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(65536, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Content-Length', str(size))
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            with open(VIDEO_PATH, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)

    def serve_file(self, filename, content_type):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.exists(filepath):
            self.send_response(404)
            self.end_headers()
            return
        with open(filepath, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, obj):
        import json
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    local_ip = get_local_ip()
    server = HTTPServer(('0.0.0.0', PORT), VideoHandler)

    print()
    print('  ┌─────────────────────────────────────────────┐')
    print('  │         🎬  RÉGIE VIDÉO — SERVEUR LOCAL      │')
    print('  ├─────────────────────────────────────────────┤')
    print(f'  │  Admin (ce PC)  →  http://localhost:{PORT}     │')
    print(f'  │  Lecteur TV     →  http://{local_ip}:{PORT}/tv  │')
    print('  ├─────────────────────────────────────────────┤')
    print('  │  Copiez l\'URL "Lecteur TV" sur chaque télé  │')
    print('  │  Ctrl+C pour arrêter                        │')
    print('  └─────────────────────────────────────────────┘')
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Serveur arrêté.')
