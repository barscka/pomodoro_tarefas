# Pomodoro Personalizado - Backend

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4%2B-red)](https://www.sqlalchemy.org)

Backend para o aplicativo Pomodoro Personalizado que gerencia atividades, agendamentos, histórico e dados do usuário.

## Funcionalidades

- Agendamento aleatório de atividades
- Ciclos de trabalho e descanso (1h trabalho / 5min descanso)
- Limite diário de atividades (máx. 6 por dia)
- Restrição por categoria (máx. 2 da mesma categoria por dia)
- Rotina semanal automática (segunda a sábado)
- Histórico de tarefas com visualização mensal
- Categorização de atividades
- Opção de pausa e retomada

## Tecnologias

- Python 3.8+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- SQLite (Banco de dados)
- Poetry (Gerenciamento de dependências)

## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pomodoro-personalizado.git
   cd pomodoro-personalizado