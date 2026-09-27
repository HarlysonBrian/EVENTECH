from sqlalchemy import Column, Integer, String, Date, ForeignKey
from core.database import Base, engine


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    perfil = Column(String, nullable=False)


class Evento(Base):
    __tablename__ = "eventos"

    id_evento = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_evento = Column(Date, nullable=False)
    capacidade = Column(Integer, nullable=False)
    carga_horaria = Column(Integer, nullable=False)


class Inscricao(Base):
    __tablename__ = "inscricoes"

    id_inscricao = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False
    )
    id_evento = Column(
        Integer,
        ForeignKey("eventos.id_evento"),
        nullable=False
    )
    status = Column(String, nullable=False)


class Participacao(Base):
    __tablename__ = "participacoes"

    id_participacao = Column(Integer, primary_key=True, index=True)
    id_inscricao = Column(
        Integer,
        ForeignKey("inscricoes.id_inscricao"),
        nullable=False
    )
    presente = Column(Integer, nullable=False)
    horas_obtidas = Column(Integer, nullable=False)


class Certificado(Base):
    __tablename__ = "certificados"

    id_certificado = Column(Integer, primary_key=True, index=True)
    id_participacao = Column(
        Integer,
        ForeignKey("participacoes.id_participacao"),
        nullable=False
    )
    data_emissao = Column(Date, nullable=False)


Base.metadata.create_all(bind=engine)