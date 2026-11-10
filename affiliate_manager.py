from urllib.parse import urlparse
from database import connect

def validate_https(url):
    p = urlparse(url.strip())
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        raise ValueError("Use uma URL HTTPS válida, sem credenciais embutidas.")
    return url.strip()

def add_product(name, category, original_url, affiliate_url, platform, keywords, campaign_id):
    original_url = validate_https(original_url)
    affiliate_url = validate_https(affiliate_url)
    if not all(x.strip() for x in (name, category, platform, campaign_id)):
        raise ValueError("Nome, categoria, plataforma e campanha são obrigatórios.")
    with connect() as con:
        cur = con.execute("""INSERT INTO products
        (name,category,original_url,affiliate_url,platform,keywords,campaign_id)
        VALUES(?,?,?,?,?,?,?)""",
        (name.strip(), category.strip(), original_url, affiliate_url,
         platform.strip(), keywords.strip(), campaign_id.strip()))
        return cur.lastrowid

def update_affiliate(product_id, affiliate_url):
    affiliate_url = validate_https(affiliate_url)
    with connect() as con:
        cur = con.execute("UPDATE products SET affiliate_url=? WHERE id=?", (affiliate_url, product_id))
        if cur.rowcount == 0:
            raise ValueError("Produto não encontrado.")

def list_products():
    with connect() as con:
        return con.execute("SELECT * FROM products ORDER BY id DESC").fetchall()

def delete_product(product_id):
    with connect() as con:
        cur = con.execute("DELETE FROM products WHERE id=?", (product_id,))
        if cur.rowcount == 0:
            raise ValueError("Produto não encontrado.")
