# Agendador Inteligente de Aulas

**Projeto de Programação Dinâmica - Weighted Interval Scheduling**

Um sistema que usa **Programação Dinâmica** para encontrar o melhor conjunto de aulas que podem ser agendadas em **1 sala**, maximizando a prioridade total sem conflitos de horários.

---

# Autor

* Eduardo de Almeida Morais - 231011275
---

## O Problema

Uma universidade precisa agendar múltiplas aulas em **uma única sala**, mas muitas delas têm horários conflitantes.

**Desafio:** Qual é o melhor conjunto de aulas que podem ser agendadas simultaneamente em 1 sala, maximizando a prioridade total?

**Exemplo:**
```
Aulas disponíveis:
- Python Avançado: 08:00-10:00, Prioridade 10
- Java Básico: 08:30-09:30, Prioridade 3
- C++ Essencial: 09:00-11:00, Prioridade 8
- Machine Learning: 10:30-12:00, Prioridade 9

Problema: Python Avançado e Java conflitam!
Solução: Agendar Python (P:10) e rejeitar Java (P:3)
```

---

## A Solução: Weighted Interval Scheduling

### O que é?

**Weighted Interval Scheduling** é um algoritmo de **Programação Dinâmica** que resolve o problema de selecionar intervalos de tempo (com pesos/prioridades) de forma ótima.

### Como funciona?

```
1. ENTRADA: Lista de aulas com (início, fim, prioridade)

2. ORDENAÇÃO: Ordena aulas por tempo de término

3. PROGRAMAÇÃO DINÂMICA: 
   Para cada aula i:
   ├─ Opção 1: Incluir aula i
   │  valor = prioridade(i) + máximo_compatível(i-1)
   └─ Opção 2: Não incluir aula i
      valor = máximo(i-1)
   
   Escolhe a opção com maior valor

4. RECONSTRUÇÃO: Backtracking para encontrar aulas selecionadas

5. SAÍDA: Aulas selecionadas com prioridade máxima
```

## Como Usar

### 1. Instalação

```bash
pip install -r requirements.txt
```

### 2. Executar

```bash
streamlit run app.py
```

### 3. Usar a Interface

**Aba Entrada:**
- Upload CSV ou adicionar manualmente

**Aba Processamento:**
- Clique "EXECUTAR ALGORITMO"

**Aba Resultados:**
- Veja aulas agendadas vs rejeitadas
- Visualização em timeline

---

## Exemplo

### Entrada (12 aulas)
```
Python Avançado: 08:00-10:00, P:10
Java Básico: 08:30-09:30, P:3
C++ Essencial: 09:00-11:00, P:8
Machine Learning: 10:30-12:00, P:9
Segurança: 13:00-14:00, P:7
... (mais 7 aulas)
```

### Saída
```
 AGENDADAS (6 aulas, Prioridade Total: 27):
- Python Avançado (P:10)
- Java Básico (P:4)
- C++ Essencial (P:5)
- Machine Learning (P:5)
- Segurança (P:4)
- Docker (P:4)

 REJEITADAS (6 aulas):
- Aulas que conflitam com as agendadas
```

---

## Por que aulas são rejeitadas?

Uma aula é rejeitada quando:
1. Seu horário **conflita** com uma aula já agendada
2. Sua **prioridade é menor**

O algoritmo maximiza a **prioridade total**, não o número de aulas.

---

## Tecnologias

- Python 3.9+
- Streamlit (interface web)
- Plotly (visualizações)
- Pandas (dados)

---

## Arquivos

```
├── algorithm.py       # Algoritmo WIS
├── app.py            # Interface Streamlit
├── requirements.txt  # Dependências
├── exemplo-aulas.csv # Dados de teste
└── README.md         # Este arquivo
```