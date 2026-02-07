# Histoires Inattendues

Une web app minimaliste et élégante qui transforme vos photos en histoires captivantes grâce à Claude Vision.

## 🎬 Fonctionnement

1. **Prendre une photo** - Cliquez sur le bouton pour prendre une photo avec votre téléphone ou choisir depuis votre galerie
2. **Claude Vision traite l'image** - L'IA détecte un détail inattendu et invente une histoire complètement surprenante
3. **L'histoire s'affiche** - Avec une belle typographie et une mise en page élégante
4. **Sauvegarde automatique** - Les histoires sont conservées dans Supabase
5. **Galerie personnelle** - Consultez vos anciennes histoires en bas de page

## 🎨 Design

- **Minimaliste et mobile-first** - Conçu pour prendre des photos au téléphone
- **Fond crème avec typographie serif** - Élégance intemporelle
- **Responsive complètement** - Fonctionne parfaitement sur tous les appareils
- **Animations fluides** - "L'histoire se tisse..." avec spinner élégant

## 🛠️ Stack Technique

- **Backend** : Flask (Python)
- **IA** : Claude Sonnet 4 (claude-sonnet-4-20250514) avec vision
- **Base de données** : Supabase (PostgreSQL)
- **Déploiement** : Render
- **Frontend** : HTML/CSS/JavaScript vanille

## 📋 Prérequis

- Python 3.11+
- Compte Anthropic avec accès à l'API
- Compte Supabase (optionnel, pour la galerie)

## 🚀 Installation Locale

1. **Cloner et installer**
```bash
cd histoires-inattendues
python -m venv venv
source venv/bin/activate  # ou: venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos clés API
```

3. **Lancer l'application**
```bash
python app/main.py
```

L'app est disponible sur `http://localhost:5000`

## 🌐 Variables d'Environnement

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
FLASK_ENV=production
```

## 📦 Déploiement sur Render

### Prérequis

- Un compte [Render](https://render.com) (gratuit)
- Un repository GitHub avec votre code
- Vos variables d'environnement Supabase et Anthropic prêtes

### Étapes de Déploiement

#### 1. Préparer le repository

```bash
# À la racine de votre projet
git init
git add .
git commit -m "Initial commit"
git push origin main
```

#### 2. Créer un Web Service sur Render

1. Connectez-vous à [Render Dashboard](https://dashboard.render.com)
2. Cliquez sur **"New +"** → **"Web Service"**
3. Suivez les étapes :

**Configuration du service**
- **Name** : `histoires-inattendues`
- **Environment** : `Python 3`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 app.main:app`
- **Plan** : Free

#### 3. Ajouter les Variables Secrètes

Dans l'onglet **"Environment"** du service, ajouter :

| Clé | Valeur | Type |
|-----|--------|------|
| `ANTHROPIC_API_KEY` | Votre clé API | Secret |
| `SUPABASE_URL` | Votre URL Supabase | Secret |
| `SUPABASE_KEY` | Votre clé JWT Supabase | Secret |
| `FLASK_ENV` | `production` | Public |

#### 4. Déploiement

Cliquez sur **"Create Web Service"** et attendez que le build se termine.

**Votre application sera disponible à** : `https://histoires-inattendues.onrender.com`

### Auto-déploiement

À chaque push sur votre branche `main`, Render redéploiera automatiquement votre application.

## 🗄️ Schéma Supabase

### Configuration de la base de données

1. Créer un projet Supabase
2. Aller à l'onglet "SQL Editor"
3. Créer une nouvelle query
4. Copier le contenu de `supabase_schema.sql` et l'exécuter

Ou exécuter manuellement ces commandes SQL :

```sql
CREATE TABLE IF NOT EXISTS stories (
  id BIGSERIAL PRIMARY KEY,
  image_data TEXT,
  photo_description TEXT,
  story_title TEXT,
  story_text TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stories_created_at ON stories(created_at DESC);
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;

-- Permissions publiques
CREATE POLICY "Allow public read on stories"
  ON stories FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on stories"
  ON stories FOR INSERT
  WITH CHECK (true);
```

La table sauvegarde :
- `image_data` : l'image en base64
- `photo_description` : "Photo montrant..." (généré par Claude)
- `story_title` : titre de l'histoire
- `story_text` : contenu de l'histoire
- `created_at` : date/heure de création

## 🤖 Système de Prompt Claude

Le prompt système est conçu pour :

- **Ne JAMAIS décrire la photo** - Ne pas dire "cette image montre..."
- **Trouver UN détail inattendu** - Ombre, reflet, objet intérieur, texture
- **Inventer une histoire complètement inattendue** - 2-4 péripéties avec chute surprenante
- **Alterner les registres** :
  - Hilarant : absurde, dialogues savoureux
  - Tragique : poignant, un nœud dans la gorge
  - Loufoque : surréaliste, Monty Python
  - Tendre : doux, lumineux
  - Philosophique : vérité profonde cachée
  - Thriller : tension, mystère

- **Style variés** : Phrases courtes et longues, dialogues, monologues, longueur surprenante
- **Toujours in medias res** - Commencer au milieu de l'action
- **Chute inattendue** - Finale qui surprend

## 📱 Utilisation Mobile

Sur téléphone, le bouton "Prendre une photo" utilise :
```html
<input type="file" accept="image/*" capture="environment">
```

Cela ouvre directement la caméra au lieu de la galerie.

## 🎯 Fonctionnalités Futures

- [ ] Partage sur les réseaux sociaux
- [ ] Mode hors ligne avec cache local
- [ ] Filtres sur la galerie (par ton, par date)
- [ ] Export des histoires en PDF
- [ ] Notifications push pour les utilisateurs abonnés

## 📝 Licence

Ce projet est open source. Libre d'utilisation et de modification.

## 👨‍💻 Contribution

Les contributions sont bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
