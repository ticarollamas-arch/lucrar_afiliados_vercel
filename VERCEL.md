# Publicar LUCRAR.PY na Vercel

## Arquivos adicionados
- `vercel.json`: encaminha as rotas para a função Python.
- `api/index.py`: cria a aplicação Flask para execução serverless.
- `.vercelignore`: exclui arquivos locais e bancos SQLite do deploy.

## Publicação
1. Extraia o ZIP e envie a pasta completa para um repositório GitHub.
2. Importe o repositório em https://vercel.com/new.
3. Deixe o Framework Preset como Other.
4. Não configure Build Command nem Output Directory.
5. Faça o deploy.
6. Teste `https://SEU-PROJETO.vercel.app/health`.

## ATENÇÃO: persistência do banco
A Vercel executa funções serverless. O sistema de arquivos da função não
é um banco persistente: `/tmp/lucrar.sqlite3` pode desaparecer e cada
instância pode ter seu próprio arquivo. Portanto, produtos e cliques
gravados no SQLite dentro da Vercel NÃO têm persistência garantida.

Este pacote permite publicar/testar a camada HTTP, mas NÃO deve ser usado
para operação comercial real até migrar o banco para PostgreSQL gerenciado
(por exemplo, Neon ou Supabase) e adaptar `database.py` e as consultas.
Não coloque credenciais de afiliado ou chaves privadas no código/repositório.
Configure segredos em Project Settings > Environment Variables.

## Rota
`/r/ID_DA_CAMPANHA?q=texto-do-produto&category=categoria&source=origem`

O endpoint só redireciona se encontrar produto cadastrado e correspondência
acima do limiar. Não cria venda nem comissão; confirme conversões no painel
oficial da plataforma.
