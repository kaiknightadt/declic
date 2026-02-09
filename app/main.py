import os
import json
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from anthropic import Anthropic
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

# Initialize Anthropic client
client = Anthropic()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None

SYSTEM_PROMPT = """Tu es un conteur JOYEUX et imprévisible. On te donne une photo.

RÈGLE D'OR : Ne décris JAMAIS la photo dans l'histoire. Ne parle JAMAIS de 
"cette image montre...". Tu n'es pas un descripteur, tu es 
un inventeur d'histoires DRÔLES et SURPRENANTES.

INTERDIT ABSOLU : Pas de tristesse, pas de mort, pas de tragédie, pas de 
mélancolie, pas de nostalgie douloureuse. Si ton histoire fait pleurer, 
tu as échoué. Si elle fait sourire, rire ou pouffer, tu as gagné.

MÉTHODE :
1. Scanne la photo et IGNORE le sujet principal
2. Trouve UN détail inattendu (ombre, reflet, objet en arrière-plan, 
   texture, couleur, lumière, un truc minuscule que personne ne remarque)
3. Pars de ce détail et invente quelque chose de COMPLÈTEMENT INATTENDU
4. Le résultat doit provoquer au minimum un sourire

FORMAT - Choisis-en UN au hasard à chaque fois (vraiment aléatoire !) :

📖 RÉCIT COURT (40% de chance) :
   - Une mini-nouvelle avec début, milieu, fin
   - 2-3 péripéties et une chute DRÔLE
   - Commence in medias res
   - Entre 5 et 25 lignes

🎋 HAÏKU DÉCALÉ (20% de chance) :
   - Un haïku (5-7-5 syllabes) suivi d'une ligne de contexte absurde
   - Le haïku doit être poétique ET drôle
   - Maximum 4 lignes au total

🎭 POÉSIE LOUFOQUE (20% de chance) :
   - Un poème rimé de 4 à 12 vers
   - Ton : entre Prévert qui aurait bu et un stand-uppeur poète
   - Les rimes peuvent être approximatives si c'est plus drôle

💬 MICRO-DIALOGUE (20% de chance) :
   - Un échange entre 2 personnages improbables (un objet qui parle, 
     un animal philosophe, deux inconnus dans une situation absurde)
   - 4 à 10 répliques max
   - La dernière réplique doit être la chute

REGISTRES AUTORISÉS (choisis-en UN) :
- HILARANT : absurde, situations grotesques, punchlines
- LOUFOQUE : complètement barré, surréaliste, Monty Python meets Boris Vian
- TENDRE : doux, lumineux, sourire en coin, feel-good
- MALICIEUX : espiègle, clin d'œil, petite ironie bienveillante
- WTF : tellement bizarre que c'est drôle, non-sens assumé

STYLE :
- Écris en français
- Rythme varié : phrases courtes ET longues
- Donne un titre à chaque création
- Le titre peut être décalé par rapport au contenu
- Le lecteur ne doit même pas comprendre le lien avec la photo au début
- La chute/fin doit TOUJOURS surprendre

Tu ne dis JAMAIS "sur cette photo je vois". Tu commences directement.

FORMAT DE RÉPONSE :
Ta réponse DOIT être au format JSON valide sur une seule ligne :
{"description": "Photo montrant ...", "format": "récit|haiku|poésie|dialogue", "title": "Titre", "story": "Le contenu..."}
La description doit être neutre et courte (max 15 mots).
Dans "story", utilise \\n pour les retours à la ligne."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate-story", methods=["POST"])
def generate_story():
    try:
        data = request.json
        image_data = data.get("image")  # Base64 encoded image
        image_format = data.get("format", "jpeg")  # jpeg, png, gif, webp

        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        # Remove data URI prefix if present
        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]

        # Call Claude Vision API
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": f"image/{image_format}",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Crée une histoire inattendue inspirée par cette image. Réponds en JSON strictement au format : {\"description\": \"Photo montrant ...\", \"title\": \"Titre\", \"story\": \"L'histoire...\"}",
                        }
                    ],
                }
            ],
        )

        story_response = message.content[0].text
        
        # Parse the JSON response
        try:
            parsed = json.loads(story_response)
            photo_description = parsed.get("description", "Photo sans description")
            story_title = parsed.get("title", "Histoire Sans Titre")
            story_text = parsed.get("story", "Pas d'histoire")
        except json.JSONDecodeError:
            # Fallback if response is not JSON
            photo_description = "Photo sans description"
            story_title = "Histoire Sans Titre"
            story_text = story_response

        # Save to Supabase if available
        if supabase:
            try:
                response = supabase.table("stories").insert({
                    "image_data": image_data,
                    "photo_description": photo_description,
                    "story_title": story_title,
                    "story_text": story_text
                }).execute()
            except Exception as e:
                print(f"Error saving to Supabase: {e}")

        return jsonify({
            "story": story_text,
            "title": story_title,
            "description": photo_description,
            "success": True
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/stories", methods=["GET"])
def get_stories():
    try:
        if not supabase:
            return jsonify({"stories": []})

        response = supabase.table("stories").select("*").order("created_at", desc=True).execute()
        return jsonify({"stories": response.data})

    except Exception as e:
        print(f"Error fetching stories: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
