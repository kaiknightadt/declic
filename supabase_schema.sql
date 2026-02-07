-- Création de la table stories avec les descriptions
CREATE TABLE IF NOT EXISTS stories (
  id BIGSERIAL PRIMARY KEY,
  image_data TEXT,
  photo_description TEXT,
  story_title TEXT,
  story_text TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_stories_created_at ON stories(created_at DESC);

-- RLS (Row Level Security) - optionnel, à adapter selon vos besoins
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;

-- Policy pour permettre la lecture publique
CREATE POLICY "Allow public read on stories"
  ON stories FOR SELECT
  USING (true);

-- Policy pour permettre l'insertion publique
CREATE POLICY "Allow public insert on stories"
  ON stories FOR INSERT
  WITH CHECK (true);
