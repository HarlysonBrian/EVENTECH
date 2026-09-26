# EVENTECH — Sistema de Gerenciamento de Eventos Acadêmicos

Projeto desenvolvido para a disciplina de Desenvolvimento Back End do curso de Análise e Desenvolvimento de Sistemas do Centro Universitário Maurício de Nassau — UNINASSAU.

## Sobre o projeto

O EVENTECH é uma API desenvolvida para gerenciar eventos acadêmicos, permitindo o cadastro de usuários e eventos, inscrições de participantes, registro de participação e emissão de certificados.

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de usuários
- Cadastro, consulta, atualização e exclusão de eventos
- Inscrição de usuários em eventos
- Controle das inscrições
- Registro de presença e horas obtidas
- Controle da carga horária do evento
- Emissão de certificados
- Validação das regras de negócio
- Tratamento de erros com códigos HTTP
- Documentação e testes da API pelo Swagger

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Swagger / OpenAPI
- Visual Studio Code
- GitHub

## Principais entidades

- Usuário
- Evento
- Inscrição
- Participação
- Certificado

## Execução da API

Com as dependências instaladas, execute:

uvicorn main:app --reload

Depois, acesse a documentação interativa da API pelo Swagger:

http://127.0.0.1:8000/docs

## Integrantes

- Denilson Francelino Silva de Carvalho
- Harlyson Brian Tertuliano da Silva
- Juan José Marinho
- Pedro Yury Araújo Saatman
- Rodrigo da Silva Pereira
- Samuel Monteiro de Melo

## Disciplina

Desenvolvimento Back End

**Professor:** Vitor Henrique dos Santos Oliveira  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Instituição:** Centro Universitário Maurício de Nassau — UNINASSAU
