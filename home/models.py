from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# --- MODELO 1: TURMA ---
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
    turma = models.CharField(max_length=50, verbose_name="Turma")
    professor = models.ManyToManyField(User, verbose_name="Professores Responsáveis", related_name="turmas")

    def __str__(self):
        nome_colegio = self.colegio.colegio if self.colegio else "Sem Colégio"
        return f"{nome_colegio} - {self.get_serie_display()} {self.turma}"

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        unique_together = ('serie', 'turma', 'colegio')


# --- MODELO 2: ALUNO ---
class Aluno(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
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
    
    @property
    def score(self):
        nota_atual = 5.0

        for fo in self.fo_set.filter(status='Concluído'):
            nota_atual += fo.pontos
            
        return nota_atual
    
    @property
    def score_cor(self):
        s = self.score
        if s >= 8: return "#28a745" # Verde
        if s >= 5: return "#007bff" # Azul
        if s >= 3: return "#ffc107" # Amarelo
        return "#dc3545" # Vermelho
    
    def clean(self):
        if self.turma and self.colegio:
            if self.turma.colegio != self.colegio:
                raise ValidationError("A turma selecionada não pertence a este colégio.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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
    
    TODOS_TITULOS = (
        TITULO_POSITIVO_DISCIPLINAR_CHOICES +
        TITULO_POSITIVO_PEDAGOGICO_CHOICES +
        TITULO_NEGATIVO_DISCIPLINAR_CHOICES +
        TITULO_NEGATIVO_PEDAGOGICO_CHOICES
    )

    INTENSIDADE_CHOICES = [
        ('bom', 'Bom (+0.25)'),
        ('muito_bom', 'Muito Bom (+0.50)'),
        ('otimo', 'Ótimo (+1.00)'),
        ('excelente', 'Excelente (+2.00)'),
        ('leve', 'Leve (-0.25)'),
        ('media', 'Média (-0.50)'),
        ('grave', 'Grave (-1.00)'),
        ('gravissima', 'Gravíssima (-2.00)'),
        ('neutro', 'Neutro/Outro (0.00)'), 
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    colegio = models.ForeignKey('Colegio', on_delete=models.CASCADE, verbose_name="Colégio", blank=True, null=True)
    natureza = models.CharField(max_length=10, choices=NATUREZA_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    titulo = models.CharField(max_length=300, verbose_name="O que aconteceu?", choices=TODOS_TITULOS)
    descricao = models.TextField(blank=True, null=True, verbose_name="Observação")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")
    serie_original = models.CharField(max_length=50, blank=True, null=True, editable=False, verbose_name="Série na época")
    turma_original = models.CharField(max_length=50, blank=True, null=True, editable=False, verbose_name="Turma na época")
    colegio_original = models.CharField(max_length=100, blank=True, null=True, editable=False,verbose_name="Colégio na época")
    intensidade = models.CharField(max_length=20, choices=INTENSIDADE_CHOICES, default='leve')

    @property
    def pontos(self):
        valores = {
            'bom': 0.25, 'muito_bom': 0.50, 'otimo': 1.00, 'excelente': 2.00,
            'leve': -0.25, 'media': -0.50, 'grave': -1.00, 'gravissima': -2.00,
            'neutro': 0.00
        }
        return valores.get(self.intensidade, 0)

    @property
    def score_cor(self):
        s = self.score 
        p = self.pontos
        if p > 0: return "#28a745"
        if p < 0: return "#dc3545"
        return "#6c757d" 

    STATUS_CHOICES = [
        ('Em aberto', 'Em aberto'),
        ('Em andamento', 'Em andamento'),
        ('Concluído', 'Concluído'),
        ('Anulado', 'Anulado') 
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
    

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.aluno.turma:
                self.serie_original = self.aluno.turma.serie
                self.turma_original = self.aluno.turma.turma
            else:
                self.serie_original = ""
                self.turma_original = ""
            if self.aluno.colegio:
                self.colegio_original = str(self.aluno.colegio)
            else:
                self.colegio_original = ""
            if not self.colegio and self.aluno.colegio:
                self.colegio = self.aluno.colegio
        
        mapa_de_pesos = {
            # --- POSITIVOS ---
            'Cumpriu ativamente com todas as atribuições, quando Chefe de Turma e ou Subchefe de Turma': 'bom',
            'Apresentou-se como voluntário para participar de atividade extra curricular representando o colégio': 'bom',
            'Colaborou ativamente para a disciplina e o bom comportamento no ambiente escolar': 'bom',
            'Participou ativamente durante a aula': 'bom',
            'Colaborou com um colega que estava com dificuldade de aprendizado': 'bom',
            'Demonstrou honestidade ao devolver objeto ou dinheiro encontrado que não lhe pertencia': 'bom',

            'Demonstrou gentileza para com um colega com alguma necessidade ou ainda para com um professor, monitor ou agente': 'muito_bom',
            'Contribuiu espontaneamente para a limpeza, arrumação e manutenção das dependências escolares': 'muito_bom',
            'Apresentou-se como voluntário para participar de atividades de assistência social': 'muito_bom',
            'Compareceu à formatura inicial com o uniforme impecavelmente bem passado e excelente apresentação individual': 'muito_bom',

            'Destacou-se dos demais pela vibração no canto do Hino Nacional ou outro hino previsto para o dia, pela vibração na execução dos movimentos e ou auxiliou espontaneamente o Chefe de Turma e/ou o monitor para colocar a turma em forma': 'otimo',

            'Obtive em todos os trimestres média igual ou superior a 8,0 (oito vírgula zero), em todos os Componentes Curriculares, ou, ainda, que se destacarem positivamente em seu comportamento disciplinar (estudantes que durante o ano letivo não tenham cometido nenhum fato observado negativo)': 'excelente',

            # --- NEGATIVOS ---
            'Deixou de comparecer ou chegar atrasado às atividades programadas ou delas ausentar-se sem autorização.': 'leve',
            'Deixou de cumprir a escala de Chefe de Turma e/ou SubChefe de Turma, conforme organização da instituição escolar.': 'leve',
            'Comportou-se de forma inadequada durante atividades, instruções ou formaturas': 'leve',
            'Simulou doença para esquivar-se ao atendimento de obrigações e atividades escolares': 'leve',

            'Deixou material ou dependência sob sua responsabilidade, desarrumada, com má apresentação ou para tal contribuir': 'media',
            'Deixou de apresentar materiais, documentos ou trabalhos sob sua responsabilidade no prazo devido': 'media',
            'Deixou de seguir orientação prevista no manual do CCM, que prevê as manifestações formais de respeito a professores, funcionários e militares, bem como a símbolos nacionais e autoridades': 'media',
            'Deixou de zelar pelo nome do colégio e da rede pública de ensino do Estado do Paraná, envolvendo-se em brigas, tu multos, algazarras e brincadeiras agressivas quando uniformizado, em público e/ou fazendo uso do transporte escolar ou coletivo': 'media',
            'Deixou de seguir orientações e determinações do Chefe e do Subchefe de Turma, quando no exercício de suas funções': 'media',
            'Utilizou bonés e capuz dentro de sala de aula': 'media',
            'Utilizou piercing, alargadores nas dependências da instituição escolar.': 'media',
            'Utilizou sem devida autorização da equipe diretiva,  telefones celulares e/ou aparelhos eletrônicos na Instituição de Ensino': 'media',

            'Faltou com a verdade e ou comportar-se de maneira inadequada, desrespeitando ou desafiando pessoas, descumprindo normas vigentes ou normas de boa educação': 'grave',
            'Teve em seu poder, introduzir, ler ou distribuir, dentro do colégio, cartazes, jornais ou publicações que atentem contra a moral': 'grave',
            'Retirou ou tentou retirar de qualquer dependência do colégio material, ou mesmo deles servir-se, sem ordem do responsável ou do proprietário': 'grave',
            'Entrou no colégio ou dele saiu não estando para isso autorizado, bem como entrar ou sair por locais e vias não permitidos': 'grave',
            'Utilizou-se de processos fraudulentos na realização de provas e trabalhos escolares, bem como a adulteração de documentação': 'grave',
            'Praticou gestos que intimidem e agridem pessoas tanto verbal quanto fisicamente (bullying)': 'grave',
            'Utilizou meios digitais para difamar, atacar ou incentivar condutas inadequadas no ambiente escolar, bem como envolver-se em atos inconvenientes e fazendo apologia a ilegalidades, usando dos mesmos meios envolvendo o nome do CCM (cyberbullying)': 'grave',
            'Portou na instituição de ensino objetos alheios à prática educativa como bebidas alcoólicas/congêneres': 'grave',
            'Recusou-se a usar o fardamento ou qualquer uniforme  pré-estabelecido como padrão CCM': 'grave',

            'Portou simulacros de armas de fogo e/ou armas brancas': 'gravissima',
            'Portou objetos que ameacem a segurança individual e/ou da coletividade ou envolveu-se em rixa, inclusive luta corporal, com outro estudante ou profissionais do colégio': 'gravissima',
            'Causou danos físicos e/ou materiais leves ou graves de qualquer natureza': 'gravissima',
            'Portou, usou e/ou distribuiu drogas lícitas nas dependências do colégio': 'gravissima',
            'Portou, usou e/ou distribuiu drogas ilícitas nas dependências do colégio': 'gravissima',
        }
        if self.titulo != 'Outro' and self.titulo in mapa_de_pesos:
            self.intensidade = mapa_de_pesos[self.titulo]
        elif self.titulo == 'Outro' and not self.pk:
             pass

        super().save(*args, **kwargs)
    
class FOHistory(models.Model):
    fo = models.ForeignKey(FO, on_delete=models.CASCADE, related_name='historico')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    campo_alterado = models.CharField(max_length=50) 
    valor_anterior = models.TextField(blank=True, null=True)
    valor_novo = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Histórico de F.O."
        verbose_name_plural = "Históricos de F.O."
        ordering = ['-data_alteracao']

    def __str__(self):
        return f"{self.fo} - {self.campo_alterado} em {self.data_alteracao}"

class Anexo(models.Model):
    fo = models.ForeignKey(FO, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='anexo/')
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