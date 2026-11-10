# LUCRAR.PY — Termux

Gerenciador local de produtos afiliados, correspondência conservadora,
redirecionamento e importação de conversões oficiais.

## Instalação no Termux

```bash
pkg update -y
pkg install python -y
pip install -r requirements.txt
python3 lucrar.py
```

O banco `data/lucrar.sqlite3` é criado automaticamente. Não precisa root.

## Fluxo

1. Cadastre produto, URL original, link de afiliado aprovado, plataforma,
   palavras-chave e identificador único da campanha.
2. Analise uma descrição de campanha no menu para verificar a correspondência.
3. Rode o servidor:
   `python3 lucrar.py --serve --host 127.0.0.1 --port 8080`
4. Teste localmente:
   `http://127.0.0.1:8080/r/camp-1?q=Fone%20Bluetooth%20JBL%20Tune`
   Substitua `camp-1` e o texto pelos seus dados cadastrados.

## Publicação real

O servidor local só recebe requisições no próprio aparelho/rede. Para cliques
de pessoas na internet, hospede a aplicação em servidor público com HTTPS,
domínio, proxy reverso e controles de abuso. Não exponha diretamente o Termux
sem proteção. O link público deve apontar para `/r/ID_DA_CAMPANHA?q=...`.
O parâmetro `q` descreve o produto anunciado; ele não pode ser usado para
escolher um destino arbitrário. Correspondência abaixo do limiar retorna 404.

## Conversões e comissões

O sistema contabiliza cliques que passam pelo seu endpoint. Ele NÃO consegue
saber que houve compra apenas porque alguém clicou. Importe o CSV exportado
oficialmente pela plataforma no menu 7, com colunas:

`platform,order_id,campaign_id,amount,commission,converted_at`

Os nomes/formatos dos CSVs variam por plataforma; adapte uma cópia ao formato
acima sem inventar registros. A importação deduplica por plataforma + pedido.
Conversões pendentes, canceladas ou atribuídas a outro afiliado devem seguir
o estado e as regras oficiais do programa.

## Segurança e limites

- Apenas URLs HTTPS são aceitas no cadastro.
- O destino vem do banco, nunca de um parâmetro de URL do visitante.
- Os parâmetros do link afiliado cadastrado são preservados literalmente.
- Não altera links de terceiros nem intercepta tráfego fora deste endpoint.
- O identificador `reference_id` é gerado para cada clique.
- Use somente links e campanhas autorizados e divulgue a natureza afiliada.
- A pontuação é heurística, não prova de que dois itens são o mesmo produto.
  Cadastre nomes/modelos específicos e palavras-chave discriminantes.
- Antes de produção, acrescente autenticação administrativa, rate limiting,
  logs com retenção limitada e HTTPS na hospedagem.

## Testes

```bash
python3 -m unittest -v
```

## Arquivos

`lucrar.py`, `main.py`, `database.py`, `affiliate_manager.py`,
`campaign_matcher.py`, `redirect_engine.py`, `analytics.py`, `config.py`.
