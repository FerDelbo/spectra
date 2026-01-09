from django.db import models
from django.contrib.auth.models import User

# --- MODELO 1: TURMA ---
# Necessário para criar os botões (A TDS, B TDS) e vincular ao Professor
class Turma(models.Model):
    serie_choices = [
        ('6º', '6º'),
        ('7º', '7º'),
        ('8º', '8º'),
        ('9º', '9º'),
        ('1ª', '1ª'),
        ('2ª', '2ª'),
        ('3ª', '3ª'),
    ]
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio", blank=True, null=True)
    serie = models.CharField(max_length=20, verbose_name="Série", choices=serie_choices)
    turma = models.CharField(max_length=50, verbose_name="Turma") # Ex: "A TDS"
    professor = models.ManyToManyField(User, verbose_name="Professores Responsáveis", related_name="turmas")

    def __str__(self):
        return f"{self.get_serie_display()} - {self.turma}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        unique_together = ('serie', 'turma', 'colegio')


# --- MODELO 2: ALUNO ---
class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    # MANTIDO COMO 'matricula' (mas você usará para guardar a Série)
    matricula = models.CharField(max_length=20, verbose_name="Série")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.turma}"


# --- MODELO 3: FO ---
class FO(models.Model):
    NATUREZA_CHOICES = [
        ('Positivo', 'Positivo'),
        ('Negativo', 'Negativo'),
    ]
    
    TIPO_CHOICES = [
        ('Disciplinar', 'Disciplinar'),
        ('Pedagogico', 'Pedagógico'),
    ]

    TITULO_CHOICES = [
        ('Participação em aula', 'Participação em aula'),
        ('Comportamento exemplar', 'Comportamento exemplar'),
        ('Atraso', 'Atraso'),
        ('Falta de material', 'Falta de material'),
        ('Distração', 'Distração'),
        ('Outro', 'Outro'),
    ]

    TITULO_POSITIVO_DISCIPLINAR_CHOICES = [
        ('Cumpriu ativamente com todas as atribuições, quando Chefe de Turma e ou Subchefe de Turma', 'Cumpriu ativamente com todas as atribuições, quando Chefe de Turma e ou Subchefe de Turma'),
        ('Apresentou-se como voluntário para participar de atividade extra curricular representando o colégio', 'Apresentou-se como voluntário para participar de atividade extra curricular representando o colégio'),
        ('Colaborou ativamente para a disciplina e o bom comportamento no ambiente escolar', 'Colaborou ativamente para a disciplina e o bom comportamento no ambiente escolar'),
        ('Demonstrou honestidade ao devolver objeto ou dinheiro encontrado que não lhe pertencia', 'Demonstrou honestidade ao devolver objeto ou dinheiro encontrado que não lhe pertencia'),
        ('Demonstrou gentileza para com um colega com alguma necessidade ou ainda para com um professor, monitor ou agente', 'Demonstrou gentileza para com um colega com alguma necessidade ou ainda para com um professor, monitor ou agente'),
        ('Contribuiu espontaneamente para a limpeza, arrumação e manutenção das dependências escolares', 'Contribuiu espontaneamente para a limpeza, arrumação e manutenção das dependências escolares'),
        ('Apresentou-se como voluntário para participar de atividades de assistência social', 'Apresentou-se como voluntário para participar de atividades de assistência social'),
        ('Compareceu à formatura inicial com o uniforme impecavelmente bem passado e excelente apresentação individual', 'Compareceu à formatura inicial com o uniforme impecavelmente bem passado e excelente apresentação individual'),
        ('Destacou-se dos demais pela vibração no canto do Hino Nacional ou outro hino previsto para o dia, pela vibração na execução dos movimentos e ou auxiliou espontaneamente o Chefe de Turma e/ou o monitor para colocar a turma em forma', 'Destacou-se dos demais pela vibração no canto do Hino Nacional ou outro hino previsto para o dia, pela vibração na execução dos movimentos e ou auxiliou espontaneamente o Chefe de Turma e/ou o monitor para colocar a turma em forma'),
        ('Obtive em todos os trimestres média igual ou superior a 8,0 (oito vírgula zero), em todos os Componentes Curriculares, ou, ainda, que se destacarem positivamente em seu comportamento disciplinar (estudantes que durante o ano letivo não tenham cometido nenhum fato observado negativo)', 'Obtive em todos os trimestres média igual ou superior a 8,0 (oito vírgula zero), em todos os Componentes Curriculares, ou, ainda, que se destacarem positivamente em seu comportamento disciplinar (estudantes que durante o ano letivo não tenham cometido nenhum fato observado negativo)'),
        ('Outro', 'Outro'),
    ]

    TITULO_POSITIVO_PEDAGOGICO_CHOICES = [
        ('Participou ativamente durante a aula', 'Participou ativamente durante a aula'),
        ('Colaborou com um colega que estava com dificuldade de aprendizado', 'Colaborou com um colega que estava com dificuldade de aprendizado'),
        ('Outro', 'Outro'),
    ]

    TITULO_NEGATIVO_DISCIPLINAR_CHOICES = [
        ('Deixou de comparecer ou chegar atrasado às atividades programadas ou delas ausentar-se sem autorização.', 'Deixou de comparecer ou chegar atrasado às atividades programadas ou delas ausentar-se sem autorização'),
        ('Deixou de cumprir a escala de Chefe de Turma e/ou SubChefe de Turma, conforme organização da instituição escolar.', 'Deixou de cumprir a escala de Chefe de Turma e/ou SubChefe de Turma, conforme organização da instituição escolar.'),
        ('Comportou-se de forma inadequada durante atividades, instruções ou formaturas', 'Comportou-se de forma inadequada durante atividades, instruções ou formaturas'),
        ('Simulou doença para esquivar-se ao atendimento de obrigações e atividades escolares', 'Simulou doença para esquivar-se ao atendimento de obrigações e atividades escolares'),
        ('Deixou de seguir orientação prevista no manual do CCM, que prevê as manifestações formais de respeito a professores, funcionários e militares, bem como a símbolos nacionais e autoridades', 'Deixou de seguir orientação prevista no manual do CCM, que prevê as manifestações formais de respeito a professores, funcionários e militares, bem como a símbolos nacionais e autoridades'),
        ('Deixou de zelar pelo nome do colégio e da rede pública de ensino do Estado do Paraná, envolvendo-se em brigas, tu multos, algazarras e brincadeiras agressivas quando uniformizado, em público e/ou fazendo uso do transporte escolar ou coletivo', 'Deixou de zelar pelo nome do colégio e da rede pública de ensino do Estado do Paraná, envolvendo-se em brigas, tu multos, algazarras e brincadeiras agressivas quando uniformizado, em público e/ou fazendo uso do transporte escolar ou coletivo'),
        ('Deixou de seguir orientações e determinações do Chefe e do Subchefe de Turma, quando no exercício de suas funções', 'Deixou de seguir orientações e determinações do Chefe e do Subchefe de Turma, quando no exercício de suas funções'),
        ('Utilizou bonés e capuz dentro de sala de aula', 'Utilizou bonés e capuz dentro de sala de aula'),
        ('Utilizou piercing, alargadores nas dependências da instituição escolar.', 'Utilizou piercing, alargadores nas dependências da instituição escolar.'),
        ('Utilizou sem devida autorização da equipe diretiva,  telefones celulares e/ou aparelhos eletrônicos na Instituição de Ensino', 'Utilizou sem devida autorização da equipe diretiva,  telefones celulares e/ou aparelhos eletrônicos na Instituição de Ensino'),
        ('Faltou com a verdade e ou comportar-se de maneira inadequada, desrespeitando ou desafiando pessoas, descumprindo normas vigentes ou normas de boa educação', 'Faltou com a verdade e ou comportar-se de maneira inadequada, desrespeitando ou desafiando pessoas, descumprindo normas vigentes ou normas de boa educação'),
        ('Teve em seu poder, introduzir, ler ou distribuir, dentro do colégio, cartazes, jornais ou publicações que atentem contra a moral', 'Teve em seu poder, introduzir, ler ou distribuir, dentro do colégio, cartazes, jornais ou publicações que atentem contra a moral'),
        ('Retirou ou tentou retirar de qualquer dependência do colégio material, ou mesmo deles servir-se, sem ordem do responsável ou do proprietário', 'Retirou ou tentou retirar de qualquer dependência do colégio material, ou mesmo deles servir-se, sem ordem do responsável ou do proprietário'),
        ('Entrou no colégio ou dele saiu não estando para isso autorizado, bem como entrar ou sair por locais e vias não permitidos', 'Entrou no colégio ou dele saiu não estando para isso autorizado, bem como entrou ou saiu por locais e vias não permitidos'),
        ('Praticou gestos que intimidem e agridem pessoas tanto verbal quanto fisicamente (bullying)', 'Praticou gestos que intimidem e agridem pessoas tanto verbal quanto fisicamente (bullying)'),
        ('Utilizou meios digitais para difamar, atacar ou incentivar condutas inadequadas no ambiente escolar, bem como envolver-se em atos inconvenientes e fazendo apologia a ilegalidades, usando dos mesmos meios envolvendo o nome do CCM (cyberbullying)', 'Utilizou meios digitais para difamar, atacar ou incentivar condutas inadequadas no ambiente escolar, bem como envolver-se em atos inconvenientes e fazendo apologia a ilegalidades, usando dos mesmos meios envolvendo o nome do CCM (cyberbullying)'),
        ('Portou na instituição de ensino objetos alheios à prática educativa como bebidas alcoólicas/congêneres', 'Portou na instituição de ensino objetos alheios à prática educativa como bebidas alcoólicas/congêneres'),
        ('Recusou-se a usar o fardamento ou qualquer uniforme  pré-estabelecido como padrão CCM', 'Recusou-se a usar o fardamento ou qualquer uniforme  pré-estabelecido como padrão CCM'),
        ('Portou simulacros de armas de fogo e/ou armas brancas', 'Portou simulacros de armas de fogo e/ou armas brancas'),
        ('Portou objetos que ameacem a segurança individual e/ou da coletividade ou envolveu-se em rixa, inclusive luta corporal, com outro estudante ou profissionais do colégio', 'Portou objetos que ameacem a segurança individual e/ou da coletividade ou envolveu-se em rixa, inclusive luta corporal, com outro estudante ou profissionais do colégio'),
        ('Causou danos físicos e/ou materiais leves ou graves de qualquer natureza', 'Causou danos físicos e/ou materiais leves ou graves de qualquer natureza'),
        ('Portou, usou e/ou distribuiu drogas lícitas nas dependências do colégio', 'Portou, usou e/ou distribuiu drogas lícitas nas dependências do colégio'),
        ('Portou, usou e/ou distribuiu drogas ilícitas nas dependências do colégio', 'Portou, usou e/ou distribuiu drogas ilícitas nas dependências do colégio'),
        ('Outro', 'Outro'),
    ]

    TITULO_NEGATIVO_PEDAGOGICO_CHOICES = [
        ('Deixou material ou dependência sob sua responsabilidade, desarrumada, com má apresentação ou para tal contribuir', 'Deixou material ou dependência sob sua responsabilidade, desarrumada, com má apresentação ou para tal contribuir.'),
        ('Deixou de apresentar materiais, documentos ou trabalhos sob sua responsabilidade no prazo devido', 'Deixou de apresentar materiais, documentos ou trabalhos sob sua responsabilidade no prazo devido'),
        ('Utilizou-se de processos fraudulentos na realização de provas e trabalhos escolares, bem como a adulteração de documentação', 'Utilizou-se de processos fraudulentos na realização de provas e trabalhos escolares, bem como a adulteração de documentação'),
        ('Outro', 'Outro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio", blank=True, null=True)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=100, verbose_name="O que aconteceu?", choices=TITULO_CHOICES)
    descricao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")
    
    # Novos campos para sistema de chamado
    STATUS_CHOICES = [
        ('Em aberto', 'Em aberto'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Em aberto', verbose_name="Status")
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='fo_responsavel', verbose_name="Responsável")
    relatorio = models.TextField(blank=True, null=True, verbose_name="Relatório")
    evidencias = models.TextField(blank=True, null=True, verbose_name="Evidências (links ou descrições)")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Fato Observado"
        verbose_name_plural = "Fatos Observados"
        ordering = ['-data_registro']

    def __str__(self):
        return f"{self.aluno.nome} - {self.titulo}"
    
class FOHistory(models.Model):
    fo = models.ForeignKey(FO, on_delete=models.CASCADE, related_name='historico')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    campo_alterado = models.CharField(max_length=50)  # Ex: 'status', 'relatorio', 'evidencias'
    valor_anterior = models.TextField(blank=True, null=True)
    valor_novo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)  # Descrição da alteração

    class Meta:
        verbose_name = "Histórico de F.O."
        verbose_name_plural = "Históricos de F.O."
        ordering = ['-data_alteracao']

    def __str__(self):
        return f"{self.fo} - {self.campo_alterado} em {self.data_alteracao}"

class Anexo(models.Model):
    fo = models.ForeignKey(FO, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexos/')
    nome = models.CharField(max_length=100, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome or self.arquivo.name

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"

class Colegio(models.Model):
    colegio = models.CharField(max_length=100, verbose_name="Nome do Colégio", blank=True, default="")
    def __str__(self):
        return self.colegio

    class Meta:
        verbose_name = "Colégio"
        verbose_name_plural = "Colégios"
