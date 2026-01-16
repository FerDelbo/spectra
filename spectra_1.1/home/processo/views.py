import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from home.models import FO, FOHistory, Anexo
from django.contrib import messages
from django.db.models import Q

# Função Auxiliar para Compressão de Imagem
def compress_image(image):
    im = Image.open(image)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    
    im_io = BytesIO()
    # Salva com qualidade reduzida para economizar espaço
    im.save(im_io, 'JPEG', quality=60, optimize=True)
    new_image = ContentFile(im_io.getvalue(), name=image.name)
    return new_image

def get_user_type(user):
    try:
        profile = user.userprofile
        return profile.user_type.nome if profile.user_type else None
    except:
        return None

@login_required
def processo_detalhes(request, fo_id):
    fo = get_object_or_404(FO, id=fo_id)
    user_type = get_user_type(request.user)
    
    # 1. Verificação de Acesso
    can_view = False
    if user_type == 'Professor' and fo.usuario == request.user:
        can_view = True
    elif user_type == 'Monitor' and fo.tipo == 'Disciplinar':
        can_view = True
    elif user_type == 'Pedagogo':
        can_view = True
    
    if not can_view:
        messages.error(request, 'Acesso negado.')
        return redirect('processo')

    # 2. Lógica de Reabertura
    if request.method == 'POST' and 'reabrir_caso' in request.POST:
        if user_type == 'Pedagogo' or (user_type == 'Monitor' and fo.tipo == 'Disciplinar'):
            FOHistory.objects.create(
                fo=fo,
                usuario=request.user,
                campo_alterado='status',
                valor_anterior=fo.status,
                valor_novo='Em andamento',
                descricao='Caso reaberto para revisão.'
            )
            fo.status = 'Em andamento'
            fo.save()
            # MENSAGEM COM TAG 'reaberto' PARA APARECER NESTA PÁGINA
            messages.success(request, 'Processo reaberto!', extra_tags='reaberto')
            return redirect('processo_detalhes', fo_id=fo.id)

    # 3. Lógica de permissão de edição
    can_treat = False
    if fo.status != 'Concluído':
        if user_type == 'Pedagogo' or (user_type == 'Monitor' and fo.tipo == 'Disciplinar'):
            can_treat = True

    # 4. Processamento de POST (Salvar ou Excluir Anexo)
    if request.method == 'POST' and can_treat:
        
        # --- SUB-LÓGICA: EXCLUIR ANEXO ---
        if 'excluir_anexo' in request.POST:
            anexo_id = request.POST.get('anexo_id')
            anexo = get_object_or_404(Anexo, id=anexo_id, fo=fo)
            nome_arq = anexo.nome
            anexo.delete()
            
            FOHistory.objects.create(
                fo=fo, usuario=request.user, campo_alterado='anexos',
                valor_anterior=nome_arq, valor_novo='Removido',
                descricao=f'O anexo "{nome_arq}" foi excluído.'
            )
            # Tag 'reaberto' usada aqui para que o feedback apareça na página de detalhes
            messages.success(request, 'Anexo removido.', extra_tags='reaberto')
            return redirect('processo_detalhes', fo_id=fo.id)

        # --- LÓGICA: SALVAR ALTERAÇÕES ---
        if 'reabrir_caso' not in request.POST:
            new_status = request.POST.get('status')
            new_relatorio = request.POST.get('relatorio', '').strip()
            new_evidencias = request.POST.get('evidencias', '').strip()
            
            has_changes = False

            # Status
            if fo.status != new_status:
                FOHistory.objects.create(
                    fo=fo, usuario=request.user, campo_alterado='status',
                    valor_anterior=fo.status, valor_novo=new_status,
                    descricao=f'Status alterado para {new_status}.'
                )
                fo.status = new_status
                has_changes = True

            # Relatório
            old_relatorio = (fo.relatorio or '').strip()
            if old_relatorio != new_relatorio:
                FOHistory.objects.create(
                    fo=fo, usuario=request.user, campo_alterado='relatorio',
                    valor_anterior=old_relatorio, valor_novo=new_relatorio,
                    descricao='O relatório técnico foi atualizado.'
                )
                fo.relatorio = new_relatorio
                has_changes = True

            # Evidências (Texto/Links)
            old_evidencias = (fo.evidencias or '').strip()
            if old_evidencias != new_evidencias:
                FOHistory.objects.create(
                    fo=fo, usuario=request.user, campo_alterado='evidencias',
                    valor_anterior=old_evidencias, valor_novo=new_evidencias,
                    descricao='Novas evidências ou links foram anexados.'
                )
                fo.evidencias = new_evidencias
                has_changes = True

            # Anexos (Arquivos) com Validação e Compressão
            if 'anexos' in request.FILES:
                anexos_enviados = request.FILES.getlist('anexos')
                arquivos_salvos = 0
                
                for f in anexos_enviados:
                    if f.size > 5 * 1024 * 1024:
                        messages.error(request, f"Arquivo {f.name} ignorado: excede 5MB.")
                        continue
                    
                    ext = os.path.splitext(f.name)[1].lower()
                    if ext not in ['.jpg', '.jpeg', '.png', '.pdf']:
                        messages.error(request, f"Arquivo {f.name} ignorado: formato inválido.")
                        continue

                    if ext in ['.jpg', '.jpeg', '.png']:
                        try:
                            f = compress_image(f)
                        except:
                            pass 

                    Anexo.objects.create(fo=fo, arquivo=f, nome=f.name)
                    arquivos_salvos += 1

                if arquivos_salvos > 0:
                    FOHistory.objects.create(
                        fo=fo, usuario=request.user, campo_alterado='anexos',
                        valor_anterior='', valor_novo=f'{arquivos_salvos} arquivo(s)',
                        descricao=f'Foram adicionados {arquivos_salvos} novos anexos.'
                    )
                    has_changes = True

            if has_changes:
                fo.responsavel = request.user
                fo.save()
                # MENSAGEM COM TAG 'atualizado' PARA APARECER NA PÁGINA DA LISTA (PROCESSO)
                messages.success(request, 'F.O. atualizada com sucesso!', extra_tags='atualizado')
                return redirect('processo')
            else:
                messages.info(request, 'Nenhuma alteração detectada.', extra_tags='reaberto')
                return redirect('processo_detalhes', fo_id=fo.id)

    # Organização de Anexos por Tipo para o Template
    anexos_fotos = fo.anexos.filter(arquivo__icontains='.jpg') | \
                   fo.anexos.filter(arquivo__icontains='.jpeg') | \
                   fo.anexos.filter(arquivo__icontains='.png')
    
    anexos_docs = fo.anexos.exclude(id__in=anexos_fotos)

    return render(request, 'processo_detalhes.html', {
        'fo': fo, 
        'can_treat': can_treat, 
        'user_type': user_type,
        'anexos_fotos': anexos_fotos,
        'anexos_docs': anexos_docs
    })
@login_required
def processo(request):
    user_type = get_user_type(request.user)
    # Pega todos os FOs
    fos = FO.objects.all().order_by('-data_registro')

    # 1. Pesquisa
    search_query = request.GET.get('search')
    if search_query:
        fos = fos.filter(
            Q(aluno__nome__icontains=search_query) |
            Q(aluno__turma__turma__icontains=search_query) |
            Q(tipo__icontains=search_query)
        )

    # 2. Filtros Status
    status_filter = request.GET.getlist('status')
    if status_filter:
        fos = fos.filter(status__in=status_filter)

    # 3. Filtros Natureza
    natureza_filter = request.GET.getlist('natureza')
    if natureza_filter:
        fos = fos.filter(natureza__in=natureza_filter)

    # 4. Injeção para o template manter os checkboxes marcados
    # Sem isso, o HTML {% if 'X' in request.GET.status_list %} não funciona
    request.GET._mutable = True
    request.GET['status_list'] = status_filter
    request.GET['natureza_list'] = natureza_filter
    request.GET._mutable = False

    return render(request, 'processo.html', {'fos': fos, 'user_type': user_type})