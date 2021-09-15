from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def root(request):
    return redirect('/main')

def main(request):
    return render(request, 'wishes_app/main.html')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    
    elif request.method == 'POST':
        errors = User.objects.validador_campos(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            #Si se produce un error pero no queremos perder los datos....
            request.session['level_mensaje'] = 'alert-danger'
            return redirect('/') 
        else:
            request.session['registro_name'] = ""
            request.session['registro_username'] = ""
            request.session['registro_datehired'] = ""
           
            name = request.POST['name']
            username = request.POST['username']
            datehired = request.POST['datehired']

            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            obj = User.objects.create(name=name, username=username,password=password_hash,datehired=datehired)
            obj.save()
            messages.success(request, "Usuario registrado con éxito!!!!")
            request.session['level_mensaje'] = 'alert-success'
            
        return redirect('/')


def login(request):
    if request.method == 'GET':
        return redirect("/")
    
    else:
        if request.method == 'POST':
            user = User.objects.filter(username=request.POST['username_login'])
            #Buscamos el correo ingresado en la BD             
            if user : #Si el usuario existe
                usuario_registrado = user[0]
                if bcrypt.checkpw(request.POST['password_login'].encode(), usuario_registrado.password.encode()):
                    usuario = { # session
                        'id':usuario_registrado.id,
                        'name':usuario_registrado.name,
                        'username':usuario_registrado.username,
                        'datehired':str(usuario_registrado.datehired),
                    }

                    request.session['usuario'] = usuario
                    return redirect('/dashboard')
                else:
                    messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                    return redirect('/')
            else:
                messages.error(request,"Datos mal ingresados o el usuario no existe!!!")
                return redirect('/')

def dashboard(request):
    if 'usuario' not in request.session:
        return redirect('/')
    context = {
    'items' : Item.objects.all().filter(wisher__id=request.session['usuario']['id']),
    'no_wishes': Item.objects.all().exclude(wisher__id=request.session['usuario']['id'])
    }
    return render(request, 'wishes_app/dashboard.html', context)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        return redirect('/')


def wish_items(request, item_id):
    context = {
        'i_view': Item.objects.get(id=item_id),
        'i_wishers': User.objects.all().filter(wisher_user__id=item_id)

    }
    return render(request, 'wishes_app/wish_items.html', context)

def erase_wish(request, item_id):
    wish_del = Item.objects.get(id=item_id)
    if wish_del.creator.id == request.session['usuario']['id']:
        wish_del.delete()
    return redirect('/dashboard')

def assign(request, item_id):
        wish_assign = Item.objects.get(id=item_id)
        wisher = User.objects.get(id=request.session['usuario']['id'])
        if 'usuario' not in request.session:
            return redirect("/")
        wish_assign.wisher.add(wisher)
        return redirect('/dashboard')

def remove_wish(request, item_id):
        wish_assign = Item.objects.get(id=item_id)
        wisher = User.objects.get(id=request.session['usuario']['id'])
        if 'usuario' not in request.session:
            return redirect("/")
        wish_assign.wisher.remove(wisher)
        return redirect('/dashboard')

def create(request):
    if 'usuario' not in request.session:
        messages.error(request,"Debe loguearse...")
        return redirect('/')
    return render(request, 'wishes_app/create_item.html')


def create_item(request):
    if 'usuario' not in request.session:
        return redirect("/")
    else:
        if request.method == "GET":
            return redirect("/")
        else:
            if request.method == "POST":
                errors = Item.objects.validador_item(request.POST)
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect('/wish_items/create')
                else:
                    desc = request.POST['item_create']
                    creador_id = User.objects.get(id=request.session['usuario']['id'])
                    obj = Item.objects.create(description=desc, creator=creador_id)
                    obj.save()

                    item_wish = Item.objects.get(id=obj.id)
                    wisher = User.objects.get(id=request.session['usuario']['id'])
                    item_wish.wisher.add(wisher)
            return redirect("/dashboard")
