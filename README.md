# 🎬 Régie Vidéo — Diffusion en Salle

Diffusez une vidéo en boucle sur 3 télés via votre réseau Wi-Fi local.

## Prérequis

- **Python 3** installé sur le PC diffuseur  
  👉 https://www.python.org/downloads/ (cochez "Add Python to PATH")
- Toutes les télés et le PC sur le **même réseau Wi-Fi**
- Un navigateur sur chaque télé (Chrome, Firefox, navigateur intégré Smart TV…)

---

## Utilisation

### 1. Lancez le serveur

**Windows :** double-cliquez sur `LANCER-SERVEUR.bat`  
**Mac / Linux :** ouvrez un terminal et tapez :
```bash
cd chemin/vers/ce/dossier
python3 server.py
```

Une URL s'affiche dans le terminal, par exemple :
```
Admin (ce PC)  →  http://localhost:8080
Lecteur TV     →  http://192.168.1.42:8080/tv
```

### 2. Uploadez votre vidéo

Ouvrez **http://localhost:8080** sur votre PC et glissez votre vidéo.

### 3. Branchez les télés

Sur chaque télé, ouvrez le navigateur et entrez l'URL **Lecteur TV** affichée dans le terminal.  
La vidéo démarre automatiquement en boucle, plein écran.

---

## Structure des fichiers

```
diffusion-salle/
├── index.html          ← Interface web (admin + lecteur)
├── server.py           ← Serveur Python
├── LANCER-SERVEUR.bat  ← Lanceur Windows
├── lancer-serveur.sh   ← Lanceur Mac/Linux
├── uploads/            ← Dossier des vidéos (créé automatiquement)
└── README.md           ← Ce fichier
```

---

## Notes

- Gardez votre PC **allumé et branché** pendant la diffusion.
- MP4 (H.264) est recommandé pour la meilleure compatibilité.
- La vidéo joue **sans son** par défaut (règle navigateur). Appuyez sur la touche Unmute si besoin.
- Pour arrêter : `Ctrl+C` dans le terminal du serveur.
