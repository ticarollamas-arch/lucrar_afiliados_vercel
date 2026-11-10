import csv
import getpass
import os
from pathlib import Path
from database import init_db
from affiliate_manager import add_product, list_products, update_affiliate, delete_product
from campaign_matcher import match_campaign
from analytics import click_summary, export_clicks, import_official_conversions, conversion_summary
from redirect_engine import create_app
from config import DB_PATH, EXPORT_DIR

def ask(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("Campo obrigatório.")

def menu():
    print("""
========== LUCRAR.PY ==========
[1] Cadastrar produto e link afiliado
[2] Atualizar link afiliado
[3] Analisar campanha
[4] Testar correspondência
[5] Gerenciar produtos
[6] Consultar cliques
[7] Importar conversões oficiais / consultar vendas
[8] Exportar relatórios CSV
[9] Configurações
[0] Sair
""")

def main(serve=False, host="127.0.0.1", port=8080):
    init_db()
    if serve:
        print(f"Redirecionador em http://{host}:{port}")
        print("Para receber tráfego externo, publique-o em hospedagem HTTPS.")
        create_app().run(host=host, port=port, debug=False)
        return
    while True:
        menu()
        op = input("Escolha: ").strip()
        try:
            if op == "1":
                data = dict(
                    name=ask("Nome do produto: "),
                    category=ask("Categoria: "),
                    original_url=ask("URL original HTTPS: "),
                    affiliate_url=ask("Seu link afiliado HTTPS: "),
                    platform=ask("Plataforma: "),
                    keywords=ask("Palavras-chave (separadas por vírgula): "),
                    campaign_id=ask("Identificador da campanha: ")
                )
                pid = add_product(**data)
                print(f"Produto cadastrado. ID: {pid}")
            elif op == "2":
                pid = int(ask("ID do produto: "))
                url = ask("Novo link afiliado HTTPS: ")
                update_affiliate(pid, url)
                print("Link atualizado.")
            elif op in ("3", "4"):
                text = ask("Texto/título da campanha: ")
                category = ask("Categoria anunciada (opcional): ", False)
                results = match_campaign(text, category)
                if results:
                    for r in results[:5]:
                        print(f"ID {r['id']} | {r['name']} | score={r['score']:.3f} | {r['platform']}")
                    print("Apenas correspondências acima do limiar são elegíveis.")
                else:
                    print("Nenhuma correspondência confiável. Nenhum redirecionamento.")
            elif op == "5":
                rows = list_products()
                if not rows:
                    print("Nenhum produto cadastrado.")
                for r in rows:
                    print(f"ID {r['id']} | {r['name']} | {r['platform']} | {r['affiliate_url']}")
                action = input("[D]eletar ID ou Enter para voltar: ").strip()
                if action.upper().startswith("D"):
                    pid = int(ask("ID: "))
                    delete_product(pid)
                    print("Produto removido.")
            elif op == "6":
                print(click_summary())
            elif op == "7":
                path = ask("CSV oficial de conversões (caminho; Enter para apenas consultar): ", False)
                if path:
                    count = import_official_conversions(path)
                    print(f"Registros oficiais importados: {count}")
                print(conversion_summary())
            elif op == "8":
                EXPORT_DIR.mkdir(parents=True, exist_ok=True)
                out = EXPORT_DIR / "cliques.csv"
                export_clicks(out)
                print(f"Exportado: {out}")
            elif op == "9":
                print(f"Banco SQLite: {DB_PATH}")
                print("Limiar de correspondência: 0.68 (configurável em config.py)")
                print("Servidor HTTP: python3 lucrar.py --serve --host 0.0.0.0 --port 8080")
                print("Não exponha o servidor sem HTTPS, autenticação operacional e proteção na hospedagem.")
            elif op == "0":
                print("Encerrado.")
                break
            else:
                print("Opção inválida.")
        except (ValueError, OSError) as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Falha controlada: {e}")
