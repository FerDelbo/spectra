from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FO

@login_required
def meus_fos_view(request):
    meus_fos = FO.objects.filter(usuario=request.user)
    return render(request, 'meus_fos.html', {'meus_fos': meus_fos})

@login_required
def historico_aluno(request, aluno_id):
    # Por enquanto, não usamos o aluno_id nem o banco, apenas renderizamos o HTML estático
    # No futuro, você usará: aluno = get_object_or_404(Aluno, id=aluno_id)
    return render(request, 'historico.html')