#!/bin/bash
echo ""
echo "  Démarrage du serveur de diffusion vidéo..."
echo ""
cd "$(dirname "$0")"
python3 server.py
