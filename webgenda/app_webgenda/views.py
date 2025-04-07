from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'webgenda/home.html')

def login_view(request):
    if request.method == "POST":
        usrname = request.POST["username"]
        pssword = request.POST["password"]
    
        #Código de autenticação do usuário
        user = authenticate(request, username = usrname, password = pssword)
        if user is not None:
            #Logar usuário
            login(request, user)
            return redirect(reverse("home/"))
        else:
            #Credenciais inválidas
            messages.error(request, "Nome de usuário ou senha inválida.")
            return redirect(reverse(""))
    else:
        # Processamento do GET
        return render(request, "webgenda/login.html")