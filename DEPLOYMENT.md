# Guide Complet de Déploiement - Histoires Inattendues

## 🚀 Déploiement sur Render

### Étape 1 : Préparer votre Repository GitHub

```bash
# Initialiser le repository (si ce n'est pas déjà fait)
cd histoires-inattendues
git init
git remote add origin https://github.com/VOTRE_USERNAME/histoires-inattendues.git
git branch -M main
git add .
git commit -m "Initial commit: Histoires Inattendues app"
git push -u origin main
```

### Étape 2 : Créer un Compte Render

1. Allez sur [render.com](https://render.com)
2. Inscrivez-vous gratuitement
3. Connectez votre compte GitHub

### Étape 3 : Créer un Web Service

1. Sur le **Render Dashboard**, cliquez sur **New +**
2. Sélectionnez **Web Service**
3. Choisissez votre repository `histoires-inattendues`
4. Cliquez **Connect**

### Étape 4 : Configurer le Service

**Informations Générales**
- **Name** : `histoires-inattendues`
- **Environment** : `Python 3.11`
- **Region** : Auto (ou votre région préférée)
- **Branch** : `main`
- **Build Command** : `pip install -r requirements.txt`
- **Start Command** : `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 app.main:app`

**Plan**
- Sélectionnez **Free** (ou **Starter** pour meilleure performance)

### Étape 5 : Configurer les Variables d'Environnement

1. Cliquez sur l'onglet **Environment**
2. Ajoutez les variables suivantes en tant que **Secret** :

```
ANTHROPIC_API_KEY = <votre_clé_anthropic>
SUPABASE_URL = https://votre_projet.supabase.co
SUPABASE_KEY = <votre_clé_supabase>
FLASK_ENV = production
```

### Étape 6 : Lancer le Déploiement

1. Cliquez sur **Create Web Service**
2. Attendez le build (3-5 minutes)
3. Une fois terminé, vous verrez l'URL de votre app : `https://histoires-inattendues.onrender.com`

## 🗄️ Configuration Supabase

### Créer la Table `stories`

1. Allez sur [supabase.com](https://supabase.com)
2. Ouvrez votre projet
3. Allez à **SQL Editor**
4. Cliquez **New Query**
5. Collez ce code :

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

CREATE POLICY "Allow public read on stories"
  ON stories FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert on stories"
  ON stories FOR INSERT
  WITH CHECK (true);
```

6. Cliquez **Execute**

## 🔄 Auto-Déploiement

Une fois configuré, **à chaque push sur votre branche main**, Render redéploiera automatiquement votre application.

```bash
# Effectuer des changements
git add .
git commit -m "Mise à jour du design"
git push origin main
# → Render se redéploie automatiquement !
```

## 📊 Monitoring

### Voir les Logs en Direct

1. Depuis le Render Dashboard
2. Allez à votre service **histoires-inattendues**
3. Onglet **Logs**
4. Voir les logs en temps réel

### Redémarrer le Service

Si quelque chose ne fonctionne pas :
1. Onglet **Settings**
2. Cliquez **Restart Service**

## 🐛 Troubleshooting

### L'app ne démarre pas

1. Vérifiez les logs : Logs → Scroll vers le bas
2. Erreurs courantes :
   - `ModuleNotFoundError` → Vérifiez `requirements.txt`
   - `No such file or directory` → Vérifiez les chemins de fichiers
   - Erreur d'API → Vérifiez les variables d'environnement

### L'app est lente au démarrage

C'est normal pour le plan Free. Attendez 30-60 secondes au premier accès.

### Images ne s'affichent pas

Vérifiez que `ANTHROPIC_API_KEY` est correct en testant localement :
```bash
python app/main.py
```

### Erreur "Connection refused"

Vérifiez que Supabase est accessible :
1. Allez à votre Supabase Dashboard
2. **Settings** → **Database** → Vérifiez que c'est connecté

## ✅ Checklist Finale

- [ ] Repository GitHub créé et prêt
- [ ] Variables d'environnement configurées dans Render
- [ ] Table `stories` créée dans Supabase
- [ ] Service Render créé et déployé
- [ ] App accessible sur `https://histoires-inattendues.onrender.com`
- [ ] Bouton "Prendre une photo" fonctionne
- [ ] Histoires se sauvegardent dans Supabase
- [ ] Galerie affiche les anciennes histoires

## 🎉 Vous Êtes Prêt !

Votre app est maintenant en ligne et prête à générer des histoires inattendues !
