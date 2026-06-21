# BET · Gestão & Análise de Apostas Esportivas

Sistema pessoal para **controlar a banca** e **encontrar valor nas odds**, feito em
arquivos HTML _standalone_ (React via CDN + Babel no navegador, **sem build**). Os
dados ficam no `localStorage` do próprio navegador. Um mini-servidor opcional em
Python (`server.py`) entra em cena só para a **busca automática na API-Football**.

> Uso pessoal / educacional. Aposte com responsabilidade.

---

## Módulos

### 🏠 `index.html` — Aplicativo único (recomendado)
App completo num só arquivo, com **abas no topo** alternando entre **Banca** e
**Análise** (a última aba fica salva no `localStorage`). É o arquivo a abrir no dia
a dia. As duas abas usam exatamente a mesma lógica descrita abaixo.

> `banca.html` e `analise.html` continuam existindo como **versões standalone /
> backup** de cada módulo — úteis para abrir um módulo isolado, mas o `index.html`
> já reúne os dois.

### 💰 Aba Banca (também em `banca.html`) — Gestão de banca
Registro e acompanhamento das apostas.

- **Registro de apostas:** data, esporte, evento, mercado, casa, odd, stake e
  status (`green` / `red` / `anulada` / `pendente`).
- **Controle de banca e unidades.**
- **KPIs:** lucro, ROI sobre a banca, _yield_ e taxa de acerto.
- **Gráficos:** evolução da banca e lucro por esporte / mercado / casa.
- **Persistência:** `localStorage`.

### 📊 Aba Análise (também em `analise.html`) — Análise estatística (Poisson)
Analisador para estimar probabilidades e detectar valor.

- **Modelo de Poisson** a partir das médias de gols: probabilidades de **1X2**,
  **over/under**, **ambas marcam** e **placares prováveis**.
- **Detector de valor:** compara a probabilidade do modelo com a odd da casa.
- **Stake sugerido** por **Kelly fracionado**.
- **Integração com a API-Football** (`api-sports.io`, header `x-apisports-key`):
  busca os times pelo nome e usa os últimos jogos para preencher as médias de gols
  automaticamente. A chave da API é salva no `localStorage`. As chamadas passam pelo
  **mini-servidor local** (`server.py`), que faz proxy e evita o bloqueio de CORS do
  navegador — veja [Como rodar](#como-rodar).

---

## Como rodar

### Modo simples (sem servidor)

Para **Banca** e para a análise com entrada **manual** de gols, não precisa de nada:

1. Abra o **`index.html`** com duplo clique (ou arraste para o navegador).
2. Alterne entre as abas **Banca** e **Análise** no topo.

### Modo com API-Football (recomendado para a Análise automática)

A busca automática de médias precisa do mini-servidor local, que faz **proxy** das
chamadas à API-Football e evita o bloqueio de **CORS** do navegador. Requer apenas
**Python 3** (sem `pip install` — só biblioteca padrão):

```bash
python server.py            # sobe em http://localhost:8000
python server.py 8080       # ou em outra porta
```

Depois abra **http://localhost:8000/** no navegador. Nesse modo a página chama
`/api/...`, que o `server.py` repassa para `https://v3.football.api-sports.io/...`
com a chave no header certo.

> **Internet:** é necessária no **primeiro carregamento** de cada página para baixar
> as bibliotecas via CDN (React, ReactDOM, Recharts, Babel). Depois disso o app
> funciona mesmo offline; só a **busca de jogos na API-Football** exige conexão.

### Configurar a chave da API-Football

1. Crie uma conta em [api-sports.io](https://www.api-sports.io/) e copie sua chave.
2. Suba o `server.py` e abra `http://localhost:8000/` (aba **Análise**).
3. No painel **Preencher pela API-Football**, cole a chave (fica salva no
   `localStorage`), digite os nomes dos times e clique em **Buscar médias**.

A chave pode também ser fornecida ao servidor sem digitá-la na página, por:

- variável de ambiente `APISPORTS_KEY`, ou
- um arquivo `apikey.txt` na pasta (uma linha com a chave — já está no `.gitignore`).

---

## Estrutura de pastas

```
Bet coffe/
├── index.html      # APP ÚNICO: abas Banca + Análise (use este)
├── banca.html      # versão standalone da Banca (backup)
├── analise.html    # versão standalone da Análise (backup)
├── server.py       # mini-servidor: serve os HTML + proxy da API-Football
├── apikey.txt      # (opcional) chave da API — ignorado pelo git
├── .gitignore
└── README.md       # este arquivo
```

---

## Stack

- **React 18** + **ReactDOM** (UMD via CDN)
- **Babel Standalone** (transpila JSX no navegador)
- **Recharts** (gráficos — usado no módulo Banca)
- **API-Football** (api-sports.io — usado no módulo Análise)
- **Python 3** (biblioteca padrão) — `server.py`, serve os arquivos e faz proxy da API
- Persistência: **`localStorage`**

## Privacidade

Tudo roda **localmente no navegador**. Não há backend: apostas, banca e a chave da
API ficam apenas no `localStorage` da máquina. Limpar os dados do navegador apaga
o histórico — convém exportar/fazer backup antes, se o módulo oferecer essa opção.
