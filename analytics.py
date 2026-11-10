import csv
from pathlib import Path
from database import connect

def click_summary():
    with connect() as con:
        total = con.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]
        rows = con.execute("""SELECT campaign_id, COUNT(*) AS clicks
          FROM clicks GROUP BY campaign_id ORDER BY clicks DESC""").fetchall()
    return "Cliques registrados: %s\n%s" % (total, "\n".join(f"{r['campaign_id']}: {r['clicks']}" for r in rows))

def conversion_summary():
    with connect() as con:
        total = con.execute("SELECT COUNT(*) FROM conversions").fetchone()[0]
        sums = con.execute("SELECT COALESCE(SUM(amount),0), COALESCE(SUM(commission),0) FROM conversions").fetchone()
    return (f"Conversões importadas de relatórios oficiais: {total}\n"
            f"Valor de vendas informado pela plataforma: R$ {sums[0]:.2f}\n"
            f"Comissão informada pela plataforma: R$ {sums[1]:.2f}")

def import_official_conversions(path):
    """CSV esperado: platform,order_id,campaign_id,amount,commission,converted_at"""
    count = 0
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"platform","order_id"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV precisa conter platform e order_id.")
        with connect() as con:
            for row in reader:
                amount = float(row["amount"]) if row.get("amount") else None
                commission = float(row["commission"]) if row.get("commission") else None
                con.execute("""INSERT OR IGNORE INTO conversions
                (platform,external_order_id,campaign_id,amount,commission,converted_at)
                VALUES(?,?,?,?,?,?)""",
                (row["platform"], row["order_id"], row.get("campaign_id") or None,
                 amount, commission, row.get("converted_at") or None))
                count += con.execute("SELECT changes()").fetchone()[0]
    return count

def export_clicks(path):
    with connect() as con:
        rows = con.execute("""SELECT c.id,p.name,c.campaign_id,c.source,c.referrer,
          c.destination,c.reference_id,c.clicked_at
          FROM clicks c JOIN products p ON p.id=c.product_id ORDER BY c.id""").fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["click_id","product","campaign_id","source","referrer","destination","reference_id","clicked_at"])
        writer.writerows([tuple(r) for r in rows])
