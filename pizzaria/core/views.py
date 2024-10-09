
# core/views.py
from .models import Cliente, Mesa, Reserva
from .forms import ClienteForm, ReservaForm 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    return render(request, 'core/menu.html')

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/lista_clientes.html', {'clientes': clientes})

def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'core/criar_cliente.html', {'form': form})

def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/lista_reservas.html', {'reservas': reservas})

def criar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'core/criar_reserva.html', {'form': form})

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    mesas = Mesa.objects.all()  # Obtém todas as mesas

    if request.method == 'POST':
        reserva.data_reserva = request.POST['data_reserva']
        reserva.hora_reserva = request.POST['hora_reserva']
        reserva.num_pessoas = request.POST['num_pessoas']
        reserva.mesa_id = request.POST['mesa']  # Supondo que você tenha uma relação de ForeignKey

        reserva.save()
        return redirect('listar_reservas')  # Redireciona para a lista de reservas

    return render(request, 'core/editar_reserva.html', {'reserva': reserva, 'mesas': mesas})

def deletar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        reserva.delete()
        return redirect('listar_reservas')  # Redireciona para a lista de reservas

    return render(request, 'core/deletar_reserva.html', {'reserva': reserva})
# core/views.py

@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/listar_usuarios.html', {'usuarios': usuarios})

@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UserCreationForm()
    return render(request, 'core/criar_usuario.html', {'form': form})

@login_required
def atualizar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, 'core/atualizar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def deletar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'core/deletar_usuario.html', {'usuario': usuario})


from .models import Mesa
from .forms import MesaForm  # Assumindo que você criará um formulário de Mesa

# View para listar mesas
def listar_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'core/listar_mesas.html', {'mesas': mesas})

# View para criar mesa
def criar_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm()
    return render(request, 'core/criar_mesa.html', {'form': form})

# View para atualizar mesa
def atualizar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        form = MesaForm(request.POST, instance=mesa)
        if form.is_valid():
            form.save()
            return redirect('listar_mesas')
    else:
        form = MesaForm(instance=mesa)
    return render(request, 'core/criar_mesa.html', {'form': form, 'mesa': mesa})

# View para deletar mesa
def deletar_mesa(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.delete()
        return redirect('listar_mesas')
    return render(request, 'core/deletar_mesa.html', {'mesa': mesa})

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Reserva, Cliente, Mesa
from django.contrib.auth.models import User
from datetime import datetime

# Função genérica para gerar PDF
def gerar_pdf(html_string, nome_arquivo):
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename={nome_arquivo}.pdf'
    return response

# Gerar PDF de Reservas
def gerar_relatorio_reservas(request):
    reservas = Reserva.objects.all()
    html_string = render_to_string('core/relatorio_reservas.html', {'reservas': reservas})
    
    return gerar_pdf(html_string, 'relatorio_reservas')

# Gerar PDF de Clientes
def gerar_relatorio_clientes(request):
    clientes = Cliente.objects.all()
    html_string = render_to_string('core/relatorio_clientes.html', {'clientes': clientes})
    return gerar_pdf(html_string, 'relatorio_clientes')

# Gerar PDF de Usuários
def gerar_relatorio_usuarios(request):
    usuarios = User.objects.all()
    html_string = render_to_string('core/relatorio_usuarios.html', {'usuarios': usuarios})
    return gerar_pdf(html_string, 'relatorio_usuarios')

# Gerar PDF de Mesas
def gerar_relatorio_mesas(request):
    mesas = Mesa.objects.all()
    html_string = render_to_string('core/relatorio_mesas.html', {'mesas': mesas})
    return gerar_pdf(html_string, 'relatorio_mesas')

