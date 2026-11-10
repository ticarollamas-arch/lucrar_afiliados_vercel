#!/usr/bin/env python3
"""Ponto de entrada: python3 lucrar.py"""
import argparse
from main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LUCRAR.PY - gestão legítima de links afiliados")
    parser.add_argument("--serve", action="store_true", help="inicia o servidor HTTP de redirecionamento")
    parser.add_argument("--host", default="127.0.0.1", help="interface de escuta (padrão: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    main(serve=args.serve, host=args.host, port=args.port)
