from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Docentes, TipoPesquisa, TipoEnsino

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

@receiver(post_migrate)
def inserir_tipopesquisa(sender, **kwargs):
    for tipo in TIPOS_PESQUISA:
        TipoPesquisa.objects.get_or_create(tipo=tipo)

@receiver(post_migrate)
def inserir_tipoensino(sender, **kwargs):
    for tipo in TIPOS_ENSINO:
        TipoEnsino.objects.get_or_create(tipo=tipo)

@receiver(post_migrate)
def criar_dados_iniciais(sender, **kwargs):
    if not Docentes.objects.filter(username='teste').exists():
        Docentes.objects.create(
            nome='Docente Teste',
            username='teste',
            senha='123456',
            email='docente@teste.com'
        )
        print("Docente de teste criado.")
