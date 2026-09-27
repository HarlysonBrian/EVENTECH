from pydantic import BaseModel
from datetime import date


class Usuario(BaseModel):
    nome: str
    email: str
    perfil: str


class Evento(BaseModel):
    titulo: str
    descricao: str
    data_evento: date
    capacidade: int
    carga_horaria: int


class Inscricao(BaseModel):
    id_usuario: int
    id_evento: int


class Participacao(BaseModel):
    id_inscricao: int
    presente: bool
    horas_obtidas: int


class Certificado(BaseModel):
    id_participacao: int
    data_emissao: date