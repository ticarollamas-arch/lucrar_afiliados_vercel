import re
import unicodedata
from difflib import SequenceMatcher
from config import MATCH_THRESHOLD
from database import connect

STOP = {"para","com","uma","por","das","dos","the","and","de","da","do","em","no","na","e"}

def normalize(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return set(w for w in re.findall(r"[a-z0-9]+", s) if len(w) > 1 and w not in STOP)

def score_campaign(text, category, product):
    query = normalize(text)
    product_terms = normalize(product["name"] + " " + product["keywords"])
    cat_terms = normalize(category)
    product_cat = normalize(product["category"])
    if not query or not product_terms:
        return 0.0
    overlap = len(query & product_terms) / max(1, len(query))
    phrase = SequenceMatcher(None, " ".join(sorted(query)), " ".join(sorted(product_terms))).ratio()
    cat_score = 1.0 if cat_terms and cat_terms & product_cat else 0.0
    # Penaliza correspondência baseada apenas em categoria ampla.
    return min(1.0, 0.70 * overlap + 0.20 * phrase + 0.10 * cat_score)

def match_campaign(text, category=""):
    if len(text) > 500:
        raise ValueError("Texto da campanha excede 500 caracteres.")
    with connect() as con:
        rows = con.execute("SELECT * FROM products").fetchall()
    ranked = []
    for p in rows:
        s = score_campaign(text, category, p)
        # Exige evidência lexical do produto, não apenas categoria.
        if s >= MATCH_THRESHOLD and normalize(text) & normalize(p["name"] + " " + p["keywords"]):
            item = dict(p)
            item["score"] = s
            ranked.append(item)
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
