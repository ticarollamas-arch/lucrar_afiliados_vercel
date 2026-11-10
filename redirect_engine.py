import secrets
from flask import Flask, request, abort, redirect, jsonify
from database import connect
from campaign_matcher import match_campaign
from config import MAX_QUERY_LENGTH

def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/r/<campaign_id>")
    def redirect_campaign(campaign_id):
        # O ID de campanha identifica um registro local; o destino nunca vem do visitante.
        text = request.args.get("q", "")
        if not text or len(text) > MAX_QUERY_LENGTH:
            abort(400, "Informe q com o nome/descrição do produto anunciado.")
        matches = match_campaign(text, request.args.get("category", ""))
        if not matches:
            abort(404, "Correspondência insuficiente; redirecionamento bloqueado.")
        chosen = matches[0]
        if chosen["campaign_id"] != campaign_id:
            abort(404, "Produto não associado a esta campanha.")
        ref = secrets.token_urlsafe(18)
        source = request.args.get("source", "direct")[:100]
        # Não aceitar destino externo enviado pelo usuário.
        with connect() as con:
            con.execute("""INSERT INTO clicks
            (product_id,campaign_id,source,referrer,destination,reference_id)
            VALUES(?,?,?,?,?,?)""",
            (chosen["id"], campaign_id, source, request.headers.get("Referer","")[:500],
             chosen["affiliate_url"], ref))
        # Mantém intactos os parâmetros já cadastrados no link afiliado.
        return redirect(chosen["affiliate_url"], code=302)

    return app
