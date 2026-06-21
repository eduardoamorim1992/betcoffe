# BET · Gestão & Análise de Apostas Esportivas

Sistema pessoal para **controlar a banca** e **encontrar valor nas odds**, feito em
arquivos HTML _standalone_ (React via CDN + Babel no navegador, **sem build, sem
servidor**). Todos os dados ficam no `localStorage` do próprio navegador.

> Uso pessoal / educacional. Aposte com responsabilidade.

---

## Módulos

### 🏠 `index.html` — Painel inicial
Capa do projeto (HTML/CSS puro) com dois cartões que levam aos módulos abaixo.

### 💰 `banca.html` — Gestão de banca
Registro e acompanhamento das apostas.

- **Registro de apostas:** data, esporte, evento, mercado, casa, odd, stake e
  status (`green` / `red` / `anulada` / `pendente`).
- **Controle de banca e unidades.**
- **KPIs:** lucro, ROI sobre a banca, _yield_ e taxa de acerto.
- **Gráficos:** evolução da banca e lucro por esporte / mercado / casa.
- **Persistência:** `localStorage`.

### 📊 `analise.html` — Análise estatística (Poisson)
Analisador para estimar probabilidades e detectar valor.

- **Modelo de Poisson** a partir das médias de gols: probabilidades de **1X2**,
  **over/under**, **ambas marcam** e **placares prováveis**.
- **Detector de valor:** compara a probabilidade do modelo com a odd da casa.
- **Stake sugerido** por **Kelly fracionado**.
- **Integração com a API-Football** (`api-sports.io`, header `x-apisports-key`):
  busca os últimos jogos para preencher as médias automaticamente. A chave da API
  é salva no `localStorage`.

---

## Como rodar

Não há instalação nem build.

1. Abra o **`index.html`** com duplo clique (ou arraste para o navegador).
2. Navegue pelos cartões até **Banca** ou **Análise**.

> **Internet:** é necessária no **primeiro carregamento** de cada página para baixar
> as bibliotecas via CDN (React, ReactDOM, Recharts, Babel). Depois disso o app
> funciona mesmo offline; só a **busca de jogos na API-Football** exige conexão.

### Configurar a API-Football (opcional, só para o módulo Análise)

1. Crie uma conta em [api-sports.io](https://www.api-sports.io/) e copie sua chave.
2. Abra `analise.html` e cole a chave no campo indicado — ela é guardada no
   `localStorage` (fica apenas no seu navegador).

---

## Estrutura de pastas

```
Bet coffe/
├── index.html      # painel inicial (capa com os links)
├── banca.html      # gestão de banca, KPIs e gráficos
├── analise.html    # modelo de Poisson + detector de valor (Kelly)
└── README.md       # este arquivo
```

---

## Stack

- **React 18** + **ReactDOM** (UMD via CDN)
- **Babel Standalone** (transpila JSX no navegador)
- **Recharts** (gráficos — usado no módulo Banca)
- **API-Football** (api-sports.io — usado no módulo Análise)
- Persistência: **`localStorage`**

## Privacidade

Tudo roda **localmente no navegador**. Não há backend: apostas, banca e a chave da
API ficam apenas no `localStorage` da máquina. Limpar os dados do navegador apaga
o histórico — convém exportar/fazer backup antes, se o módulo oferecer essa opção.
