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

- **Modelo de Poisson** com **separação por mando (casa/fora)**: usa o ataque/defesa
  do mandante **em casa** e do visitante **fora**, com **suavização (shrinkage)** para
  amostras pequenas — evita valores degenerados quando o time tem poucos jogos na base.
  Calcula **1X2**, **over/under**, **ambas marcam** e **placares prováveis**.
- **Históricos:** **forma recente** de cada time (últimos jogos, com V/E/D e placar) e
  **confrontos diretos (H2H)** entre os dois.
- **Detector de valor:** compara a probabilidade do modelo com a odd da casa.
- **Stake sugerido** por **Kelly fracionado**.
- **Jogos pela API** (`football-data.org`, header `X-Auth-Token`): escolha a
  **competição** (Copa do Mundo, Brasileirão, Premier League, Champions, Libertadores,
  La Liga, Serie A, Bundesliga, Ligue 1, etc.), clique em **Carregar jogos** para
  listar as partidas agendadas e, ao clicar num jogo, o app busca a **forma recente**
  dos dois times (e os confrontos diretos) e preenche as médias de gols. As chamadas
  passam pelo **mini-servidor local** (`server.py`), que faz proxy e evita o bloqueio
  de CORS — veja [Como rodar](#como-rodar).
  > Quando a amostra de jogos é pequena (ex.: início de um torneio), o app avisa para
  > você revisar os números antes de confiar.

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
`/api/...`, que o `server.py` repassa para `https://api.football-data.org/v4/...`
com o token no header `X-Auth-Token`.

> **Internet:** é necessária no **primeiro carregamento** de cada página para baixar
> as bibliotecas via CDN (React, ReactDOM, Recharts, Babel). Depois disso o app
> funciona mesmo offline; só a **busca de jogos na API** exige conexão.

### Configurar o token da API (football-data.org)

A API usada é a **football-data.org** (o plano free dela dá temporada atual + jogos
recentes; cobre ~12 competições grandes e tem limite de **10 req/min**).

1. Registre-se grátis em [football-data.org](https://www.football-data.org/client/register)
   e copie o **API token** que enviam por e-mail.
2. Cole o token no arquivo **`apikey.txt`** (na 1ª linha que não for comentário). O
   `server.py` lê de lá automaticamente — não precisa digitar na página.
3. Suba o `server.py`, abra `http://localhost:8000/` (aba **Análise**) → painel
   **Jogos pela API** → escolha a competição → **Carregar jogos** → clique num jogo.

O token também pode vir da variável de ambiente `FOOTBALL_DATA_TOKEN` (alternativa
ao `apikey.txt`). O `apikey.txt` está no `.gitignore`, então não vai para o GitHub.

---

## Estrutura de pastas

```
Bet coffe/
├── index.html      # APP ÚNICO: abas Banca + Análise (use este)
├── banca.html      # versão standalone da Banca (backup)
├── analise.html    # versão standalone da Análise (backup)
├── server.py       # mini-servidor: serve os HTML + proxy da football-data.org
├── apikey.txt      # token da football-data.org — ignorado pelo git
├── .gitignore
└── README.md       # este arquivo
```

---

## Stack

- **React 18** + **ReactDOM** (UMD via CDN)
- **Babel Standalone** (transpila JSX no navegador)
- **Recharts** (gráficos — usado no módulo Banca)
- **football-data.org** (API de futebol — usada no módulo Análise)
- **Python 3** (biblioteca padrão) — `server.py`, serve os arquivos e faz proxy da API
- Persistência: **`localStorage`**

## Privacidade

Tudo roda **localmente no navegador**. Não há backend: apostas, banca e a chave da
API ficam apenas no `localStorage` da máquina. Limpar os dados do navegador apaga
o histórico — convém exportar/fazer backup antes, se o módulo oferecer essa opção.
