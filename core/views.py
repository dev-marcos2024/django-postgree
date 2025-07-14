from django.shortcuts import render, redirect
from core.forms import  ContatoForm, ProdutoMoselForm
from django.contrib import  messages
from core.models import Produto

def index(request):
    context = {
        'produtos': Produto.objects.all(),
    }
    return render(request, 'index.html', context)

def contato(request):
    form = ContatoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.send_email()
            messages.success(request, 'Contato enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar o contato!')

    context = {
        'form': form,
    }
    return render(request, 'contato.html', context)

def produto(request):
    print(request.user.is_authenticated)
    print(dir(request.user))
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProdutoMoselForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoMoselForm()
            else:
                messages.error(request, 'Erro ao Salvar o produto!')
        else:
            form = ProdutoMoselForm()

        context = {
            'form': form,
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')
