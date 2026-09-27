from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
import models
from schemas import Usuario, Evento, Inscricao, Participacao, Certificado
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuario, db: Session = Depends(get_db)):
        usuario_existente = db.query(models.Usuario).filter(
            models.Usuario.email == usuario.email
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="E-mail já cadastrado"
            )

        novo_usuario = models.Usuario(
            nome=usuario.nome,
            email=usuario.email,
            perfil=usuario.perfil
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(models.Usuario).all()
    return usuarios

@router.get("/usuarios/{id_usuario}")
def buscar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@router.put("/usuarios/{id_usuario}")
def atualizar_usuario(
    id_usuario: int,
    dados: Usuario,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    email_existente = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email,
        models.Usuario.id_usuario != id_usuario
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado"
        )

    usuario.nome = dados.nome
    usuario.email = dados.email
    usuario.perfil = dados.perfil

    db.commit()
    db.refresh(usuario)

    return usuario

@router.delete("/usuarios/{id_usuario}")
def excluir_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {"mensagem": "Usuário excluído com sucesso"}

@router.post("/eventos", status_code=201)
def criar_evento(evento: Evento, db: Session = Depends(get_db)):
    if evento.capacidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A capacidade deve ser maior que zero"
        )

    if evento.carga_horaria <= 0:
        raise HTTPException(
            status_code=400,
            detail="A carga horária deve ser maior que zero"
        )

    novo_evento = models.Evento(
        titulo=evento.titulo,
        descricao=evento.descricao,
        data_evento=evento.data_evento,
        capacidade=evento.capacidade,
        carga_horaria=evento.carga_horaria
    )

    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)

    return novo_evento

@router.get("/eventos")
def listar_eventos(db: Session = Depends(get_db)):
    eventos = db.query(models.Evento).all()
    return eventos

@router.get("/eventos/{id_evento}")
def buscar_evento(id_evento: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == id_evento
    ).first()

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    return evento

@router.put("/eventos/{id_evento}")
def atualizar_evento(
    id_evento: int,
    dados: Evento,
    db: Session = Depends(get_db)
):
    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == id_evento
    ).first()

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    if dados.capacidade <= 0:
        raise HTTPException(
            status_code=400,
            detail="A capacidade deve ser maior que zero"
        )

    if dados.carga_horaria <= 0:
        raise HTTPException(
            status_code=400,
            detail="A carga horária deve ser maior que zero"
        )

    evento.titulo = dados.titulo
    evento.descricao = dados.descricao
    evento.data_evento = dados.data_evento
    evento.capacidade = dados.capacidade
    evento.carga_horaria = dados.carga_horaria

    db.commit()
    db.refresh(evento)

    return evento

@router.delete("/eventos/{id_evento}")
def excluir_evento(id_evento: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == id_evento
    ).first()

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    db.delete(evento)
    db.commit()

    return {"mensagem": "Evento excluído com sucesso"}

@router.post("/inscricoes", status_code=201)
def criar_inscricao(inscricao: Inscricao, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == inscricao.id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == inscricao.id_evento
    ).first()

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    inscricao_existente = db.query(models.Inscricao).filter(
        models.Inscricao.id_usuario == inscricao.id_usuario,
        models.Inscricao.id_evento == inscricao.id_evento
    ).first()

    if inscricao_existente:
        raise HTTPException(
            status_code=400,
            detail="Usuário já inscrito neste evento"
        )

    total_inscritos = db.query(models.Inscricao).filter(
        models.Inscricao.id_evento == inscricao.id_evento
    ).count()

    if total_inscritos >= evento.capacidade:
        raise HTTPException(
            status_code=400,
            detail="Evento sem vagas disponíveis"
        )

    nova_inscricao = models.Inscricao(
        id_usuario=inscricao.id_usuario,
        id_evento=inscricao.id_evento,
        status="Ativa"
    )

    db.add(nova_inscricao)
    db.commit()
    db.refresh(nova_inscricao)

    return nova_inscricao

@router.get("/inscricoes")
def listar_inscricoes(db: Session = Depends(get_db)):
    inscricoes = db.query(models.Inscricao).all()
    return inscricoes

@router.get("/inscricoes/{id_inscricao}")
def buscar_inscricao(id_inscricao: int, db: Session = Depends(get_db)):
    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == id_inscricao
    ).first()

    if not inscricao:
        raise HTTPException(
            status_code=404,
            detail="Inscrição não encontrada"
        )

    return inscricao

@router.put("/inscricoes/{id_inscricao}")
def atualizar_inscricao(
    id_inscricao: int,
    dados: Inscricao,
    db: Session = Depends(get_db)
):
    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == id_inscricao
    ).first()

    if not inscricao:
        raise HTTPException(
            status_code=404,
            detail="Inscrição não encontrada"
        )

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == dados.id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == dados.id_evento
    ).first()

    if not evento:
        raise HTTPException(
            status_code=404,
            detail="Evento não encontrado"
        )

    inscricao.id_usuario = dados.id_usuario
    inscricao.id_evento = dados.id_evento

    db.commit()
    db.refresh(inscricao)

    return inscricao

@router.delete("/inscricoes/{id_inscricao}")
def excluir_inscricao(id_inscricao: int, db: Session = Depends(get_db)):
    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == id_inscricao
    ).first()

    if not inscricao:
        raise HTTPException(
            status_code=404,
            detail="Inscrição não encontrada"
        )

    db.delete(inscricao)
    db.commit()

    return {"mensagem": "Inscrição excluída com sucesso"}

@router.post("/participacoes", status_code=201)
def criar_participacao(participacao: Participacao, db: Session = Depends(get_db)):
    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == participacao.id_inscricao
    ).first()

    if not inscricao:
        raise HTTPException(
            status_code=404,
            detail="Inscrição não encontrada"
        )

    participacao_existente = db.query(models.Participacao).filter(
        models.Participacao.id_inscricao == participacao.id_inscricao
    ).first()

    if participacao_existente:
        raise HTTPException(
            status_code=400,
            detail="Participação já registrada para esta inscrição"
        )

    if participacao.horas_obtidas < 0:
        raise HTTPException(
            status_code=400,
            detail="As horas obtidas não podem ser negativas"
        )

    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == inscricao.id_evento
    ).first()

    if participacao.horas_obtidas > evento.carga_horaria:
        raise HTTPException(
            status_code=400,
            detail="As horas obtidas não podem ser maiores que a carga horária do evento"
        )

    nova_participacao = models.Participacao(
        id_inscricao=participacao.id_inscricao,
        presente=participacao.presente,
        horas_obtidas=participacao.horas_obtidas
    )

    db.add(nova_participacao)
    db.commit()
    db.refresh(nova_participacao)

    return nova_participacao

@router.get("/participacoes")
def listar_participacoes(db: Session = Depends(get_db)):
    participacoes = db.query(models.Participacao).all()
    return participacoes

@router.get("/participacoes/{id_participacao}")
def buscar_participacao(id_participacao: int, db: Session = Depends(get_db)):
    participacao = db.query(models.Participacao).filter(
        models.Participacao.id_participacao == id_participacao
    ).first()

    if not participacao:
        raise HTTPException(
            status_code=404,
            detail="Participação não encontrada"
        )

    return participacao

@router.put("/participacoes/{id_participacao}")
def atualizar_participacao(
    id_participacao: int,
    dados: Participacao,
    db: Session = Depends(get_db)
):
    participacao = db.query(models.Participacao).filter(
        models.Participacao.id_participacao == id_participacao
    ).first()

    if not participacao:
        raise HTTPException(
            status_code=404,
            detail="Participação não encontrada"
        )

    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == dados.id_inscricao
    ).first()

    if not inscricao:
        raise HTTPException(
            status_code=404,
            detail="Inscrição não encontrada"
        )

    participacao.id_inscricao = dados.id_inscricao
    participacao.presente = dados.presente
    participacao.horas_obtidas = dados.horas_obtidas

    db.commit()
    db.refresh(participacao)

    return participacao

@router.delete("/participacoes/{id_participacao}")
def excluir_participacao(id_participacao: int, db: Session = Depends(get_db)):
    participacao = db.query(models.Participacao).filter(
        models.Participacao.id_participacao == id_participacao
    ).first()

    if not participacao:
        raise HTTPException(
            status_code=404,
            detail="Participação não encontrada"
        )

    db.delete(participacao)
    db.commit()

    return {"mensagem": "Participação excluída com sucesso"}

@router.post("/certificados", status_code=201)
def criar_certificado(certificado: Certificado, db: Session = Depends(get_db)):
    participacao = db.query(models.Participacao).filter(
        models.Participacao.id_participacao == certificado.id_participacao
    ).first()

    if not participacao:
        raise HTTPException(
            status_code=404,
            detail="Participação não encontrada"
        )

    if not participacao.presente:
        raise HTTPException(
            status_code=400,
            detail="Participante não esteve presente no evento"
        )
    inscricao = db.query(models.Inscricao).filter(
        models.Inscricao.id_inscricao == participacao.id_inscricao
    ).first()

    evento = db.query(models.Evento).filter(
        models.Evento.id_evento == inscricao.id_evento
    ).first()

    if participacao.horas_obtidas < evento.carga_horaria:
        raise HTTPException(
            status_code=400,
            detail="Carga horária insuficiente para emissão do certificado"
        )
    certificado_existente = db.query(models.Certificado).filter(
    models.Certificado.id_participacao == certificado.id_participacao
).first()

    if certificado_existente:
        raise HTTPException(
            status_code=400,
            detail="Certificado já emitido para esta participação"
        )

    novo_certificado = models.Certificado(
        id_participacao=certificado.id_participacao,
        data_emissao=certificado.data_emissao
    )

    db.add(novo_certificado)
    db.commit()
    db.refresh(novo_certificado)

    return novo_certificado

@router.get("/certificados")
def listar_certificados(db: Session = Depends(get_db)):
    certificados = db.query(models.Certificado).all()
    return certificados

@router.get("/certificados/{id_certificado}")
def buscar_certificado(id_certificado: int, db: Session = Depends(get_db)):
    certificado = db.query(models.Certificado).filter(
        models.Certificado.id_certificado == id_certificado
    ).first()

    if not certificado:
        raise HTTPException(
            status_code=404,
            detail="Certificado não encontrado"
        )

    return certificado

@router.put("/certificados/{id_certificado}")
def atualizar_certificado(
    id_certificado: int,
    dados: Certificado,
    db: Session = Depends(get_db)
):
    certificado = db.query(models.Certificado).filter(
        models.Certificado.id_certificado == id_certificado
    ).first()

    if not certificado:
        raise HTTPException(
            status_code=404,
            detail="Certificado não encontrado"
        )

    participacao = db.query(models.Participacao).filter(
        models.Participacao.id_participacao == dados.id_participacao
    ).first()

    if not participacao:
        raise HTTPException(
            status_code=404,
            detail="Participação não encontrada"
        )

    certificado.id_participacao = dados.id_participacao
    certificado.data_emissao = dados.data_emissao

    db.commit()
    db.refresh(certificado)

    return certificado

@router.delete("/certificados/{id_certificado}")
def excluir_certificado(id_certificado: int, db: Session = Depends(get_db)):
    certificado = db.query(models.Certificado).filter(
        models.Certificado.id_certificado == id_certificado
    ).first()

    if not certificado:
        raise HTTPException(
            status_code=404,
            detail="Certificado não encontrado"
        )

    db.delete(certificado)
    db.commit()

    return {"mensagem": "Certificado excluído com sucesso"}