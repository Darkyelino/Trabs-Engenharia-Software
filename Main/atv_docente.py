import abc

class Atv_Docente(abc.ABC):
    """Isso é uma classe abstrata utilizada para criar atividades docentes únicas."""
    def __init__(categoria, nome, data_inicio, data_fim, descricao, local_do_curso, periodo):
        _id = Atv_Docente._id_atividades
        _categoria = categoria
        _nome = nome
        _data_inicio = data_inicio
        _data_fim = data_fim
        _descricao = descricao
        _local_do_curso = local_do_curso
        _periodo = periodo

    #Getter de id
    @property
    def id(self):
        return self._id
    #Getter-setter de categoria
    @property
    def categoria(self):
        return self._categoria
    @categoria.setter
    def categoria(self, categoria):
        self._categoria = categoria
    #Getter-setter de nome
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, nome):
        self._nome = nome
    #Getter-setter de data_inicio
    @property
    def data_inicio(self):
        return self._data_inicio
    @data_inicio.setter
    def data_inicio(self, data_inicio):
        self._data_inicio = data_inicio
    #Getter-setter de data_fim
    @property
    def data_fim(self):
        return self._data_fim
    @data_fim.setter
    def data_fim(self, data_fim):
        self._data_fim = data_fim
    #Getter-setter de descricao
    @property
    def descricao(self):
        return self._descricao
    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao
    #Getter-setter de local_do_curso
    @property
    def local_do_curso(self):
        return self._local_do_curso
    @local_do_curso.setter
    def local_do_curso(self, local_do_curso):
        self._local_do_curso = local_do_curso
    #Getter-setter de periodo
    @property
    def periodo(self):
        return self._periodo
    @periodo.setter
    def periodo(self, periodo):
        self._periodo = periodo
    
    #Métodos de Instância
    @abc.abstractmethod
    def adicionar_atividade(self):
        """Método abstrato para adicionar atividade docente."""
        pass


    def __str__(self):
        return f"ID: {self._id}, Categoria: {self._categoria}, Nome: {self._nome}, Data de Início: {self._data_inicio}, Data de Fim: {self._data_fim}, Descrição: {self._descricao}, Local do Curso: {self._local_do_curso}, Período: {self._periodo}"