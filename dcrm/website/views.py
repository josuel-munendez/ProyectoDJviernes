from django.shortcuts import redirect, render#permite cambiar la plantilla  html con datos  y devolver respuesta

# Esta es la función que se ejecuta cuando entras a la página
# login para incio de sesion  segun el rol
#logout para cerrar sesion 
from django.contrib.auth import authenticate, login, logout# type: ignore # Importamos las funciones de autenticación, inicio de sesión y cierre de sesión de Django.
from django.contrib import messages # type: ignore #
def home(request):# type: ignore
    #si el metodo  de la solicitud  es post, significa que se esta  enviado un formulario
    # post esta enviando informacion 
    if request.method =='POST': # pyright: ignore[reportUnknownMemberType]
        # si  el metodo  de la solicitud  post  significa que se esta en viando el formulario
        # aqui podemos manehjar  la logica del formulario  como la autentificacion del usuario
        username = request.POST['username'] # pyright: ignore[reportUnknownVariableType, reportUnusedVariable, reportUnknownMemberType] #  ontiene este valor des de  formulario
        password = request.POST['password'] # type: ignore
        user = authenticate(request, username=username, password= password) # type: ignore
        if user is not None: # valor o nulo 
            login(request, user) # pyright: ignore[reportUnknownArgumentType] # indicando la sesion 
            #muestra el mensaje de exito 
            messages.success(request,"ingresado exitosamente") # pyright: ignore[reportUnknownArgumentType]
            return redirect('home')
        else:
            # si las credenciales no fueron existosas 
            messages.error(request," las credenciales son invalidas !!📢") # pyright: ignore[reportUnknownArgumentType]
            return render(request, 'home.html', {})  # type: ignore
    else:
        # si el metodo  de la solicitud no es POST, simplemente renderiza la plantilla 'home.html
        return render(request, 'home.html', {})# type: ignore # El tercer argumento es un diccionario para pasar datos a la plantilla, pero aquí lo dejamos vacío por ahora.
# funcion para logiar
def login_user(request): # type: ignore
    pass

# funcion para poder salir  cerrar sesion 
def logout_user(request): # type: ignore
    logout(request)# cierre de la sesion del usuario 
    #muestra un mensaje de exito al usuario
    messages.success(request,"cerraste la session correctamente")
    return redirect('home')# direccionar al usuario a la pafina de inicio


def register_user(request):# type: ignore
    return render(request, 'register.html',{})# type: ignore