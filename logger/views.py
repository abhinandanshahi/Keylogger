from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from pynput import keyboard, mouse
import time
import subprocess
from datetime import datetime
start_time = time.time()

process = None
caps_lock_on = False
shift_pressed = False
ctrl_pressed = False
last_key = None

current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
file_name = "keylogger_{}.txt".format(current_time)

def on_press(key):
    elapsed_time = float((time.time() - start_time))
    global caps_lock_on, shift_pressed, ctrl_pressed, last_key

    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
        return

    try:
        if key.char.isprintable():
            if caps_lock_on or (shift_pressed and not ctrl_pressed):
                output = key.char.upper()
            else:
                output = key.char
        else:
            output = '<{}>'.format(key)

        if ctrl_pressed and key.char:
            output = 'ctrl+' + chr(key.vk) if key.vk in range(0, 256) else 'ctrl+' + key.name
            ctrl_pressed = False # set ctrl_pressed to False after printing the control key combination
            with open(file_name, "a") as f:
                elapsed_time = time.time() - start_time
                f.write("[{:.2f}] {}\n".format(elapsed_time, output))
                
            last_key = None
        else:
            with open(file_name, "a") as f:
                elapsed_time = time.time() - start_time
                f.write("[{:.2f}] {}\n".format(elapsed_time, output))
            last_key = key

    except AttributeError:
        output = '<{}>'.format(key)

        if key == keyboard.Key.caps_lock:
            caps_lock_on = not caps_lock_on
        elif key == keyboard.Key.shift:
            shift_pressed = True

        with open(file_name, "a") as f:
            elapsed_time = time.time() - start_time
            f.write("[{:.2f}] {}\n".format(elapsed_time, output))



def on_release(key):
    global shift_pressed, ctrl_pressed, last_key
    

    if key == keyboard.Key.shift:
        shift_pressed = False
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
        if last_key is not None and last_key.char is not None:
            with open(file_name, "a") as f:
                elapsed_time = time.time() - start_time
                f.write("[{:.2f}] control+{}\n".format(elapsed_time, last_key.char))
            last_key = None
start_time = time.time()           
def on_move(x, y):
    elapsed_time = float((time.time() - start_time))
    with open(file_name, "a") as f:
        f.write("[{:.2f}] Mouse moved to ({}, {})\n".format(elapsed_time, x, y))

def on_click(x, y, button, pressed):
    elapsed_time = time.time() - start_time
    with open(file_name, "a") as f:
        if pressed:
            f.write(f"[{elapsed_time:.2f}] Mouse pressed {button.name} at ({x}, {y})\n")
        else:
            f.write(f"[{elapsed_time:.2f}] Mouse released {button.name} at ({x}, {y})\n")


current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
file_name = "keylogger_{}.txt".format(current_time)



def start(request):
    global process, start_time

    task_description = request.POST.get('task_description')
    if not task_description:
        return HttpResponseBadRequest('Task description is required')

    start_time = time.time()
    start_time_formatted = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    file_name = "task.txt"
    elapsed_time = time.time() - start_time

    with open(file_name, 'a') as f:
        f.write(f'{task_description }')
        f.write(f'({elapsed_time:.2f}s)')  
         

    with keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
        with mouse.Listener(on_click=on_click) as mouse_listener:
            with mouse.Listener(on_move=on_move) as move_listener:
                filename = f"output_{start_time_formatted}.mp4"
                command = ['ffmpeg', '-y', '-f', 'gdigrab', '-framerate', '30', '-i', 'desktop', '-vf', 'scale=1366:768', '-c:v', 'libx264', '-preset', 'ultrafast', filename]
                process = subprocess.Popen(command)
                keyboard_listener.join()
                mouse_listener.join()
                move_listener.join()

    end_time = time.time()
    end_time_formatted = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    elapsed_time = end_time - start_time
    with open(file_name, 'a') as f:
        f.write(f'(End time: {end_time_formatted}) [Elapsed time: {elapsed_time:.2f}s]\n')

    return HttpResponse(f'Started task "{task_description}" at {start_time_formatted}. Ended at {end_time_formatted}. Elapsed time: {elapsed_time:.2f}s')

import datetime

def stop(request):
    global process, start_time

    if process:
        process.kill()
        process = None

    end_time = datetime.datetime.now()
    end_time_formatted = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    file_name = "task.txt"
    elapsed_time = time.time() - start_time
    with open(file_name, 'a') as f:
        f.write(f' ({elapsed_time:.2f}s)\n')
    return HttpResponse(f'Stopped task. End time: {end_time} | Elapsed time: {elapsed_time:.2f}s')


def home(request):
    return render(request, 'home.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# views.py
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') # replace 'home' with the name of your home page URL
            else:
                error_message = 'Invalid username or password'
        else:
            error_message = 'Invalid username or password'
    else:
        form = AuthenticationForm()
        error_message = ''
    context = {'form': form, 'error_message': error_message, 'signup': True}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # replace 'home' with the name of your home page URL
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'signup.html', context)
