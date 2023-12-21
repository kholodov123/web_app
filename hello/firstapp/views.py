from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from  django.http import *
from .models import Event, Users
import pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime as d
import requests
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
import datetime
from django.conf import settings
from django.db import connection
from django.forms import FilePathField
from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from sqlalchemy import create_engine

import pandas as pd
import requests
from firstapp.models import Event, Users

from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:111@127.0.0.1:5432/web_app')

def index(request):
    Events = Event.objects.all()
    cards = GetCards(Events)
    return render(request, "index.html", context={"cards": cards})

def GetCards(Events):
    cards = []
    for Event in Events:
        card = '''<div class="card" id="{0}" data="event" date="{3}">
        <div class="card-header">
          {0}
        </div>
        <div class="card-body" style="display: flex; align-items: center;">
          <img class="w-25 p-3" src="{1}">
          <div class="p-3" style="color: rgb(106, 31, 123)">
            <h2 class="card-title">{2}</h2>
            <p class="card-text">{3}</p>
          </div>
        </div>
      </div>'''.format(Event.type, f"/{Event.image}"[6:], Event.title, Event.data)
        cards.append(card)
    return cards

def registration(request):
    return render(request, "registration.html", context={"open" : ""})

def registration_jury(request):
    events = get_evets(Event.objects.all())
    return render(request, "registration_jury.html", context = {"events": events})

def get_evets(events):
    cards = []
    for e in events:
        op = f'<option value="{e.title}">{e.title}</option>'
        cards.append(op)
    return cards

def reg_form(request):
    if request.method == 'POST':
        id_number = request.POST.get('ID')
        password = request.POST.get('Password')
        user = authenticate(request, username = f"{id_number}", password = password)
        print(user)
        try:
            login(request, user)
            type = Users.objects.get(number = id_number).type
            if type == "User": return redirect('prof')
            elif type == "juri": return redirect('prof')
            elif type == "Organizator": return redirect('org')
            else: return redirect('home/')

        except Exception as e:
            print("Error:", e)
            return redirect("reg_f")
    else:
        return render(request, '/')

def registration_fail(request):
    return render(request, "registration.html", context={"open" : "open"})

def registration_form(request):
    if request.method == 'POST':
        id = str(request.POST.get('ID'))
        fio = request.POST.get('FIO')
        gen = request.POST.get('GEN')
        type = request.POST.get('TYPE')
        mail = request.POST.get('MAIL')
        tel = request.POST.get('TEL')
        dir = request.POST.get('DIR')
        event = request.POST.get('EVENT')
        pas = request.POST.get('PASS')
        img = request.FILES.get('IMG')
        if img != None:
            img = img
        else:
            img = "hello/static/photos/def.webp"
        Users.objects.create(
            number = id,
            full_name = fio,
            gender = gen,
            type = type,
            email = mail,
            phone = tel,
            direction = dir,
            event = event,
            image = img
        )
        User.objects.create(
            username = id,
            password = make_password(pas),
            first_name = fio,
            email = mail
        )
        return redirect("home")
    else:
        return render(request, '/')
    
def lk(request):
    user = request.user
    h = int(str(d.datetime.now().time())[:2])
    if 11 > h > 9: text = "Доброе утро"
    elif 18 > h > 11: text = "Добрый день"
    elif 24 > h > 18: text = "Добрый вечер"
    else: text = "Здравствуйте"
    name = f"{user.first_name} {user.last_name}"
    image = Users.image
    data = {"Text":text, "Name":name, "Image": f"/{str(image)[6:]}"}
    return render(request, "organizator.html", context=data)

def my_events(request):
    user = request.user
    events = Event.objects.filter(org = user)
    print("События", events)
    event_list = GetCards(events)
    title = "Мои события"
    display = "flex"
    data = {"Title": title,"Display": display, "cards": event_list, "VH":"75%"}
    return render(request, "my_info.html", context=data)

def my_people(request):
    users = Users.objects.filter(type = "Пользователь")
    user_list = get_user_card(users)
    title = "Мои участники"
    display = "none"
    events = get_evets(Event.objects.all())
    data = {"Title": title,"Display": display, "cards": user_list, "VH":"78%", "LINK":"reg_p", "events": events}
    return render(request, "my_people.html", context=data)

def my_jury(request):
    users = Users.objects.filter(type = "Жюри")
    user_list = get_user_card(users)
    title = "Мои жюри"
    display = "none"
    events = get_evets(Event.objects.all())
    data = {"Title": title,"Display": display, "cards": user_list, "VH":"78%", "LINK":"reg_p", "events": events}
    return render(request, "my_people.html", context=data)

def get_user_card (users):
    cards = []
    for user in users:
        card = '''<div class="card" data "people" id "{5}">
        <div class="card-header">
            Мероприятие: {5} - {8}
        </div>
        <div class="card-body" style="display: flex; align-items: center;">
            <img class="w-25 p-3" src="{1}">
            <div class="p-3" style="color: rgb(106, 31, 123); display: flex; flex-wrap: wrap;">
                <h2 class="card-title w-100">{2}</h2>
                <p class="card-text w-50">ID: {0}</p>
                <p class="card-text w-50">{3}</p>
                <p class="card-text w-50">{4}</p>
                <p class="card-text w-50">{6}</p>
            </div>
        </div>
    </div>'''.format(user.number, f"/{str(user.image)[6:]}", user.Full_name, user.email, user.gender, user.event, user.phone, user.email, user.direction)
        cards.append(card)
    return cards

def add_e(request):
    return render(request, "add_event.html")

def sub_e_form(request):
    if request.method == 'POST':
        title = str(request.POST.get('TITLE'))
        date = str(request.POST.get('DATE'))
        dir = str(request.POST.get("DIR"))
        img = request.FILES.get('IMG')
        if img != None:
            img = img
        else:
            img = "hello/static/photos/def.webp"

        Event.objects.create(
            title = title,
            data = date,
            type = dir,
            image = img,
            org = f"{request.user}"
        )
        return redirect("home")
    else:
        return render(request, '/')
    
def import_db(request):
    return render(request, "import_event.html")

def submit_form(request):
    if request.method == 'POST':
        # Получите данные из формы
        db = request.POST.get('DataBase')
        table = request.FILES.get('Table')
        items = read_tables(table)
        if db == "Event": add_event(items)
        elif db == "Users": add_users(items)
        print(db, table)
        return redirect('home/')
    else:
        return render(request, '/')

def read_tables(file_path): 
    try:
        #file_path = r'C:/Users/Student21/Desktop/1111/hello/static/xlsx/Events.xlsx'
        df = pd.read_excel(file_path)
        tables = df.values.tolist()
        return tables
        
    except Exception as e:
        print(f"Произошла ошибка: {e}") 
        return f"Произошла ошибка: {e}"
    
def add_event(events):
    for event in events:
        try:
                org_1 = f"{event[4]}" 
        except:
                org_1 = "All"
        try:
          Event.objects.create(
              type = f"{event[0]}",
              title = f"{event[1]}",
              image = f"{download_and_save_image(event[2])}",
              data = f"{event[3]}",
              org = org_1
          )
        except Exception as e:
          print(f"Произошла ошибка: {e}")

def add_users(users):
    for user in users:
        try:
            User.objects.create(
                username = f"{user[0]}",
                password = f"{make_password(user[1])}", 
                first_name = f"{user[2]}", 
                last_name = f"{user[3]}",
            )

            Users.objects.create(
                number = F"{user[0]}",
                type = f"{user[4]}",
                image = f"{download_and_save_image(user[5])}",
                gender = F"{user[6]}",
                email = f"{user[7]}", phone = f"{user[8]}",
                direction = f"{user[9]}",
                event = f"{user[10]}",
            )
        except Exception as e:
            print(e)

def download_and_save_image(url):
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        # Получение имени файла из URL
        file_name = os.path.basename(url)

        # Сохранение изображения в директории static/photos/
        file_path = os.path.join(settings.BASE_DIR, 'static', 'photos', file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(file_path)
        return os.path.join('hello','static', 'photos', file_name)
    
def profile(request):
    return render(request, "profile.html")    

    
