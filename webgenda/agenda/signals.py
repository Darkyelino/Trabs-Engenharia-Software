from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Docentes, TipoPesquisa, TipoEnsino, TipoAdministracao, TipoExtensao

TIPOS_PESQUISA = [
    "Bolsista de produtividade",
    "Apresentação com palestra ou curso",
    "Resenha publicada em revista especializada",
    "Produção artística, curadoria ou tradução",
    "Produção técnica aprovada",
    "Obra artística, recital, palestra técnica",
    "Orientação de bolsista (concluído)",
    "Co-orientação de bolsista (concluído)",
    "Conselho editorial de revistas",
    "Revisão de artigos nacionais",
    "Revisão de artigos internacionais",
    "Coordenação de projeto por edital",
    "Coordenação de projeto interno",
    "Participação em projeto institucional",
    "Coordenação de convênios técnicos",
    "Participação em convênios técnicos",
    "Consultoria a instituições de fomento",
    "Revisão de textos da UFAC",
    "Parecer técnico (individual ou coletivo)",
    "Parecer ou perícia técnica",
    "Revisão de livros",
    "Propriedade intelectual registrada",
    "Prêmios científicos ou culturais",
    "Organização de coletâneas",
    "Patente registrada",
    "Produção artística reconhecida",
    "Experiência profissional comprovada",
    "Publicação em periódico internacional",
    "Publicação em periódico nacional",
    "Livro por editora internacional",
    "Livro por editora nacional",
    "Livro por editora regional",
    "Capítulo por editora internacional",
    "Capítulo por editora nacional",
    "Capítulo por editora regional",
    "Resumo expandido em anais",
    "Resumo em anais",
    "Artigo completo em anais (nacional)",
    "Artigo completo em anais (internacional)",
]

TIPOS_ENSINO = [
    "Disciplina graduação/pós Lato - 15h",
    "Disciplina pós Stricto - 15h",
    "Preceptoria residência médica",
    "Orientação monitoria",
    "Orientação PIBEX",
    "Co-orientação PIBEX",
    "Orientação PIBIC/PIVIC/PIBIT",
    "Co-orientação PIBIC/PIVIC/PIBIT",
    "Orientação PET",
    "Orientação TCC/monografia",
    "Orientação dissertação",
    "Orientação tese",
    "Co-orientação dissertação",
    "Co-orientação tese",
    "Coord. disciplina (múltiplas turmas)",
    "Coord. disciplina (múltiplos docentes)",
    "Coordenação de estágios",
    "Coordenação de TCC/Monografia",
    "Coord. programa/grupo de pesquisa",
    "Coordenação de monitoria",
    "Coordenação PET",
    "Coordenação residência médica",
    "Coord. projetos coop. internacional",
    "Banca de TCC/Monografia",
    "Banca de dissertação/tese",
    "Banca de concurso prof. efetivo",
    "Evento científico com trabalho",
    "Banca seleção pós-graduação",
    "Banca de qualificação pós-graduação",
    "Texto didático aprovado",
    "Banca concurso prof. substituto",
]

TIPOS_EXTENSAO = [
    "Coordenação de Programas ou Projetos institucionais.",
    "Participantes de Programas ou Projetos de extensão.",
    "Coordenação de Cursos de extensão acima de 180 horas.",
    "Coordenação de Cursos de extensão entre 91 e 179 horas.",
    "Coordenação de Cursos de extensão entre 20 e 90 horas.",
    "Coordenação de Evento Internacional.",
    "Coordenação de Evento Nacional. ",
    "Coordenação de eventos  regionais ou locais.",
    "Conferencista convidado para eventos regionais ou locais.",
    "Conferencista convidado para eventos nacionais.",
    "Conferencista convidado para eventos internacionais.",
    "Comissão organizadora de eventos internacionais.",
    "Comissão organizadora de eventos nacionais.",
    "Comissão organizadora de eventos regionais ou locais.",
    "Prestação de serviço acadêmico de interesse institucional decorrente de convênios ou contratos."
]

TIPOS_ADMINISTRATIVA = [
    "Reitor, Vice-Reitor e Pró-Reitor (CD1, CD2 e CD3).",
    "Diretor de Centro e Similares (CD4).",
    "Coord. de Núcleo de Área.",
    "Coord. de Cursos e Pós-graduação Stricto Sensu, Graduação e Presidente ou Comissão Permanente.",
    "Vice-Presidente de Comissão Permanente.",
    "Vice-Coord. de Cursos de Pós-graduação Stricto Sensu e Graduação.",
    "Coord. de Cursos de Pós-graduação Lato Sensu.",
    "Coord. de laboratório.",
    "Presidente de comissão temporária, membro de comissão permanente, membro de comissão diretora",
    "Representação ou membro de comissão temporária nomeada pelo Reitor.",
    "Membro de colegiados de cursos de graduação e de pós-graduação.",
    "Membro do CONSU e outros."
]

@receiver(post_migrate)
def inserir_tipoadministrativa(sender, **kwargs):
    for tipo in TIPOS_ADMINISTRATIVA:
        TipoAdministracao.objects.get_or_create(tipo=tipo)

@receiver(post_migrate)
def inserir_tipoextensao(sender, **kwargs):
    for tipo in TIPOS_EXTENSAO:
        TipoExtensao.objects.get_or_create(tipo=tipo)

@receiver(post_migrate)
def inserir_tipopesquisa(sender, **kwargs):
    for tipo in TIPOS_PESQUISA:
        TipoPesquisa.objects.get_or_create(tipo=tipo)

@receiver(post_migrate)
def inserir_tipoensino(sender, **kwargs):
    for tipo in TIPOS_ENSINO:
        TipoEnsino.objects.get_or_create(tipo=tipo)
