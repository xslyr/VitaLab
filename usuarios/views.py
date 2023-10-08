from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User

# Create your views here.

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter ao menos 6 caracteres')
            return redirect('/usuarios/cadastro')

        try:
            # Username deve ser único!
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS,'Cadastro realizado com sucesso!')
        except:
            messages.add_message(request, constants.ERROR, f'Já existe um usuário com o username {username} já cadastrado. Utilize algum outro para cadastrar um novo usuário.')
            return redirect('/usuarios/cadastro')

        return redirect('/usuarios/cadastro')

def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        if user:
            login(request, user)
            # Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
            return redirect('/exames/gerenciar_exames')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/usuarios/login')