# Patrones de Diseño Implementados

**Total: 30 patrones identificados** — 18 GoF (Gang of Four) + 12 arquitectónicos/de framework.

---

## Categorías de Patrones

- **Creacionales** (5): Abstract Base Class, Singleton, Factory Method, Dependency Injection, Alias
- **Estructurales** (11): Repository, Adapter, Facade, Proxy, Decorator, Pagination, Registry, DTO, Field Encapsulation, Composite Form, Value Object
- **Comportamiento** (8): Template Method, Strategy, Observer, Command, Chain of Responsibility, Role, Specification, Pagination
- **Arquitectónicos** (6): MVT/MVC, Front Controller, Configuration Module, Service Locator, Eager Loading, Template Tag

---

# PATRONES CREACIONALES

## 1. Singleton

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Garantiza que una clase tenga una sola instancia y proporciona un punto de acceso global |
| **Dónde** | `core/services.py:33-38`, `website/views.py:10`, `productos/views.py:15`, todas las `admin.py` |
| **Cómo** | Instancia única creada a nivel de módulo y reutilizada en toda la aplicación |
| **Por qué** | Evita crear múltiples conexiones/instancias para el mismo modelo, ahorra memoria |

**Código clave:**
```python
# core/services.py
class CrudService(BaseService):
    """Singleton lógico: se instancia una vez por modelo"""

# website/views.py
_record_service = CrudService(Record)        # Instancia única para Record
_producto_service = CrudService(Producto)     # Instancia única para Producto

# admin.py en cada app
admin.site.register(Record)  # admin.site es singleton de Django
```

**Diagrama:**
```
  ┌─────────────────────────────────────────┐
  │               Aplicación                │
  │                                         │
  │  _record_service ─── CrudService(Record) │
  │  _producto_service ─ CrudService(Prod)   │
  │  admin.site ──────── AdminSite          │
  └─────────────────────────────────────────┘
         ↑ instancia única cada uno
```

---

## 2. Abstract Base Class

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Clase que no se instancia directamente, define una interfaz/base para subclases |
| **Dónde** | `core/models.py:3-11`, `core/services.py:3-8`, `core/repository.py:3-8` |
| **Cómo** | `Meta: abstract = True` en Django models; `ABC` + `@abstractmethod` en services/repository |
| **Por qué** | Evita duplicación de campos y métodos comunes (DRY), define contratos |

**Código clave:**
```python
# core/models.py - Abstract Base Class de Django
class BaseModel(models.Model):
    _created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    _updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        abstract = True  # No crea tabla, solo sirve para heredar

    def get_metadata(self):
        return f"Creado: {self._created_at}, Actualizado: {self._updated_at}"

# core/services.py - Abstract Base Class de Python
class BaseService(ABC):
    @abstractmethod
    def get_all(self) -> QuerySet: ...
    @abstractmethod
    def get_by_id(self, pk: Any) -> Optional[Model]: ...
    @abstractmethod
    def create(self, data: dict) -> Model: ...
    @abstractmethod
    def update(self, instance: Model, data: dict) -> Model: ...
    @abstractmethod
    def delete(self, instance: Model) -> None: ...
```

**Modelos que heredan de BaseModel:**
```
BaseModel (abstracta)
  ├── Record (website/models.py)
  ├── Producto (productos/models.py)
  ├── Categoria (catalogo/models.py)
  └── Catalogo (catalogo/models.py)
```

---

## 3. Simple Factory / Factory Method

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Define una interfaz para crear objetos, pero permite a las subclases decidir qué clase instanciar |
| **Dónde** | Todos los `forms.py` (`form.save()`), `core/validators.py:21-24` |
| **Cómo** | `form.save()` crea y retorna una nueva instancia del modelo |
| **Por qué** | Centraliza la lógica de creación, permite personalizar el proceso |

**Código clave:**
```python
# usuarios/forms.py
def save(self, commit=True):
    user = super().save(commit=False)          # Factory: crea User sin commit
    user.set_password(self.cleaned_data["password"])
    if commit:
        user.save()
        UserProfile.objects.get_or_create(     # Factory: crea perfil asociado
            user=user,
            defaults={"_rol": UserProfile.ROL_CLIENTE}
        )
    return user
```

---

## 4. Dependency Injection

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Inyecta dependencias a un objeto en lugar de que el objeto las cree |
| **Dónde** | `core/services.py:10` (`__init__(self, model_class)`) |
| **Cómo** | `CrudService` recibe `model_class` por constructor |
| **Por qué** | Hace que `CrudService` sea reutilizable con cualquier modelo |

**Código clave:**
```python
class CrudService(BaseService):
    def __init__(self, model_class: type[Model]):  # Inyección por constructor
        self._model_class = model_class

# Uso: el mismo servicio sirve para cualquier modelo
_record_service = CrudService(Record)
_producto_service = CrudService(Producto)
```

---

## 5. Alias Pattern

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Proporciona un nombre alternativo para una clase |
| **Dónde** | `website/forms.py` |
| **Cómo** | `AddRecordForm = RecordForm` |
| **Por qué** | Mejora legibilidad semántica |

---

# PATRONES ESTRUCTURALES

## 6. Repository / Data Access Object (DAO)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Abstrae la capa de acceso a datos separando la lógica de negocio de la persistencia |
| **Dónde** | `core/repository.py:3-29` |
| **Cómo** | `BaseRepository` define el contrato; `DjangoRepository` implementa usando ORM |
| **Por qué** | Permite cambiar el motor de BD sin afectar la lógica de negocio; facilita testing |

**Código clave:**
```python
class BaseRepository(ABC):
    @abstractmethod
    def find_all(self) -> QuerySet: ...
    @abstractmethod
    def find_by_id(self, pk: Any) -> Optional[Model]: ...
    @abstractmethod
    def save(self, instance: Model) -> Model: ...
    @abstractmethod
    def remove(self, instance: Model) -> None: ...

class DjangoRepository(BaseRepository):
    def __init__(self, model_class: type[Model]):
        self._model_class = model_class
    
    def find_all(self) -> QuerySet:
        return self._model_class.objects.all()
    
    def find_by_id(self, pk: Any) -> Optional[Model]:
        return self._model_class.objects.filter(id=pk).first()
    
    def save(self, instance: Model) -> Model:
        instance.save()
        return instance
    
    def remove(self, instance: Model) -> None:
        instance.delete()
```

---

## 7. Adapter

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Convierte la interfaz de una clase en otra interfaz que el cliente espera |
| **Dónde** | `core/repository.py` (`DjangoRepository` adapta el ORM), `core/services.py` (`CrudService` adapta el ORM) |
| **Cómo** | Adapta `Model.objects.all()` → `find_all()`, `Model.save()` → `save()`, etc. |
| **Por qué** | Desacopla el código de negocio del ORM específico |

**Ejemplo:**
```
  Cliente (View)       BaseRepository        DjangoRepository      Django ORM
       │                     │                      │                 │
       │── find_all() ──────→│                      │                 │
       │                     │── find_all() ───────→│                 │
       │                     │                      │── .all() ──────→│
       │                     │                      │←── QuerySet ───│
       │←── QuerySet ───────│←── QuerySet ────────│                 │
```

---

## 8. Facade

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Proporciona una interfaz simplificada a un conjunto de interfaces complejas |
| **Dónde** | `core/services.py` (`CrudService`), `core/security.py` |
| **Cómo** | `CrudService.get_all()` oculta `Model.objects.all().order_by("id")` |
| **Por qué** | Simplifica el código de las vistas; centraliza la lógica de consultas |

**Código clave:**
```python
# Sin Facade (vistas tendrían que escribir esto cada vez):
records = Record.objects.all().order_by("id")
record = Record.objects.filter(id=pk).first()
Record.objects.create(**data)

# Con Facade (CrudService):
_record_service.get_all()
_record_service.get_by_id(pk)
_record_service.create(data)
```

---

## 9. Proxy / Protection Proxy

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Controla el acceso a un objeto, agregando una capa de seguridad |
| **Dónde** | `website/views.py` (`has_admin_role()`), `get_object_or_404()` |
| **Cómo** | `has_admin_role()` verifica permisos antes de ejecutar la acción |
| **Por qué** | Previene accesos no autorizados a operaciones sensibles |

**Código clave:**
```python
@login_required
def delete_record(request, pk):
    if not has_admin_role(request.user):          # ← Protection Proxy
        messages.error(request, "No tienes permisos")
        return redirect("home")
    record = get_object_or_404(Record, id=pk)     # ← Protection Proxy (404 si no existe)
    _record_service.delete(record)
```

---

## 10. Decorator

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Agrega responsabilidades a un objeto dinámicamente sin modificar su clase |
| **Dónde** | Todas las `views.py` (`@login_required`), `signals.py` (`@receiver`), `nav_extras.py` (`@register.simple_tag`) |
| **Cómo** | `@login_required` envuelve la vista; se ejecuta antes de la vista original |
| **Por qué** | Sepala la preocupación de autenticación de la lógica de negocio |

**Código clave:**
```python
# Sin decorator (código repetitivo):
def delete_record(request, pk):
    if not request.user.is_authenticated:
        return redirect("login")
    # ... lógica ...

# Con decorator (limpio, reutilizable):
@login_required
def delete_record(request, pk):
    # ... solo lógica de negocio ...
```

**Vistas protegidas con `@login_required`:**
- `website/views.py`: `logout_user`, `register_user`, `customer_record`, `delete_record`, `update_record`, `admin_dashboard`, `search_records`
- `productos/views.py`: `listado`, `crear`, `detalle`, `editar`, `eliminar`
- `catalogo/views.py`: `listado_categorias`, `listado_catalogos`
- `usuarios/views.py`: `perfil`, `editar_perfil`

---

## 11. Pagination

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Divide un conjunto grande de datos en páginas más pequeñas |
| **Dónde** | `website/views.py`, `productos/views.py`, `catalogo/views.py` (todos usan `Paginator`) |
| **Cómo** | `Paginator(queryset, 5)` — 5 registros por página |
| **Por qué** | Mejora la experiencia de usuario y el rendimiento |

**Código clave:**
```python
paginator = Paginator(records_queryset, 5)            # 5 registros por página
page_number = request.GET.get("page")                  # Lee ?page=N de la URL
records_page = paginator.get_page(page_number)          # Obtiene página segura
```

---

## 12. Registry / Mapper

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Almacena y proporciona acceso a objetos mediante una clave |
| **Dónde** | `core/validators.py:3-10` |
| **Cómo** | Diccionario `_patterns` mapea nombres de campo a regex compilados |
| **Por qué** | Centraliza todas las validaciones; fácil de extender |

**Código clave:**
```python
class RegexValidator:
    _patterns = {
        "username": re.compile(r"^[a-zA-Z0-9@\.\+\-_]+$"),
        "email":    re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
        "phone":    re.compile(r"^\+?\d{7,15}$"),
        "password": re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&_]{8,}$"),
        "zip_code": re.compile(r"^\d{4,10}$"),
        "name":     re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"),
    }

    @classmethod
    def validate(cls, field_type: str, value: str) -> bool:
        pattern = cls._patterns.get(field_type)
        return bool(pattern.match(value)) if pattern else True
```

**Validaciones disponibles:**
| Tipo | Regex | Ejemplo válido |
|------|-------|----------------|
| username | `^[a-zA-Z0-9@\.\+\-_]+$` | `jose_perez-23` |
| email | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | `user@mail.com` |
| phone | `^\+?\d{7,15}$` | `+573001234567` |
| password | `^(?=.*[A-Za-z])(?=.*\d)[...]{8,}$` | `Admin123` |
| name | `^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$` | `José Muñoz` |

---

## 13. Data Transfer Object (DTO)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Objeto que transporta datos entre procesos sin comportamiento |
| **Dónde** | `website/export.py` |
| **Cómo** | Convierte modelos a filas CSV |
| **Por qué** | Sepala los datos de presentación de los datos internos |

---

## 14. Field Encapsulation

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Oculta atributos internos usando nombres protegidos |
| **Dónde** | `core/models.py` (`_created_at`, `_updated_at`), `usuarios/models.py` (`_rol`) |
| **Cómo** | Prefijo `_` (convención Python protected) + `db_column` para nombre limpio en BD |
| **Por qué** | Protege campos sensibles de modificación directa |

```python
_rol = models.CharField(max_length=20, choices=ROL_CHOICES, default=ROL_CLIENTE, db_column="rol")
# En BD: columna "rol"
# En Python: _rol (protegido, acceso vía métodos)
```

---

## 15. Composite Form

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Formulario que maneja múltiples modelos relacionados |
| **Dónde** | `usuarios/forms.py` (`UserRegistrationForm`) |
| **Cómo** | Crea `User` + `UserProfile` en un solo formulario |
| **Por qué** | Transaccional: ambas entidades se crean juntas |

---

## 16. Value Object

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Objeto inmutable que representa un valor descriptivo |
| **Dónde** | `usuarios/models.py:2-5` (constantes `ROL_*`) |
| **Cómo** | Constantes de clase inmutables |

```python
class UserProfile(models.Model):
    ROL_CLIENTE  = "cliente"
    ROL_VENDEDOR = "vendedor"
    ROL_GESTOR   = "gestor"
    ROL_ADMIN    = "admin"
```

---

# PATRONES DE COMPORTAMIENTO

## 17. Template Method

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Define el esqueleto de un algoritmo en un método, difiriendo pasos a las subclases |
| **Dónde** | `core/models.py` (`BaseModel`), todos los `admin.py` (`ModelAdmin`), `usuarios/forms.py` (`save()`) |
| **Cómo** | `BaseModel.get_metadata()` provee comportamiento base; subclases heredan sin modificar |
| **Por qué** | Evita duplicación de código (DRY) en campos timestamp |

**Jerarquía de Template Method:**
```
BaseModel (define _created_at, _updated_at, get_metadata)
  ├── Record          → hereda sin cambios
  ├── Producto        → hereda sin cambios  
  ├── Categoria       → hereda sin cambios
  └── Catalogo        → hereda sin cambios
```

---

## 18. Strategy

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Define una familia de algoritmos, los encapsula y los hace intercambiables |
| **Dónde** | `core/validators.py`, `core/services.py` (`CrudService` implementa `BaseService`), `website/export.py` (CSV export) |
| **Cómo** | Cada regex es una estrategia de validación; `CrudService` es una estrategia CRUD |
| **Por qué** | Permite cambiar algoritmos sin modificar el cliente |

**Diagrama Strategy:**
```
  Cliente (View)
       │
       │ validate("email", valor)
       ▼
  RegexValidator
       │
       ├── "email"    → re.compile(r"^[a-zA-Z0-9._%+-]+@...")
       ├── "phone"    → re.compile(r"^\+?\d{7,15}$")
       ├── "password" → re.compile(r"^(?=.*[A-Za-z])(?=.*\d)...")
       ├── "username" → re.compile(r"^[a-zA-Z0-9@\.\+\-_]+$")
       └── "zip_code" → re.compile(r"^\d{4,10}$")
```

---

## 19. Observer (Signals)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Define una dependencia uno-a-muchos; cuando un objeto cambia su estado, notifica a los dependientes |
| **Dónde** | `usuarios/signals.py` (post_save de User), `settings.py` (logging) |
| **Cómo** | Señal `post_save` de User → `create_user_profile()` crea perfil automáticamente |
| **Por qué** | Desacopla la creación de User de la creación de UserProfile |

**Código clave:**
```python
# usuarios/signals.py
@receiver(post_save, sender=User)           # ← Observer: se registra para escuchar
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={"_rol": UserProfile.ROL_CLIENTE}
        )

# usuarios/apps.py
class UsuariosConfig(AppConfig):
    name = 'usuarios'
    def ready(self):
        import usuarios.signals  # Registra los observers al iniciar
```

**Flujo Observer:**
```
  User.save()                       # Sujeto: emite post_save signal
       │
       ▼
  Signal Dispatcher                 # Dispatcher: notifica a todos los listeners
       │
       ▼
  create_user_profile()             # Observer 1: crea UserProfile automáticamente
  Logging handlers                   # Observer 2: escribe en security.log
```

---

## 20. Command

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Encapsula una solicitud como un objeto |
| **Dónde** | Migraciones de Django (`0001_initial.py`), vistas (cada URL mapea a una función) |
| **Cómo** | Cada migración tiene operaciones que se aplican/deshacen; cada URL es un comando |
| **Por qué** | Permite deshacer operaciones (rollback de migraciones) |

---

## 21. Chain of Responsibility

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Pasa una solicitud a través de una cadena de manejadores |
| **Dónde** | `settings.py` (MIDDLEWARE, AUTH_PASSWORD_VALIDATORS) |
| **Cómo** | Cada middleware procesa el request/response y lo pasa al siguiente |
| **Por qué** | Sepala preocupaciones (seguridad, sesión, CSRF, etc.) en módulos independientes |

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # ← Seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # ← Sesión
    'django.middleware.common.CommonMiddleware',          # ← Común
    'django.middleware.csrf.CsrfViewMiddleware',          # ← CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← Auth
    'django.contrib.messages.middleware.MessageMiddleware',  # ← Mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # ← Clickjack
]
```

---

## 22. Role Pattern

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Asigna roles a un objeto, cambiando su comportamiento según el rol |
| **Dónde** | `usuarios/models.py` (`UserProfile._rol`) |
| **Cómo** | `_rol` determina permisos: `es_admin()`, `es_vendedor()`, etc. |
| **Por qué** | Implementa RBAC (Role-Based Access Control) |

**Roles del sistema:**
```
UserProfile._rol
  ├── "cliente"    → Solo lectura básica
  ├── "vendedor"   → CRUD clientes + productos
  ├── "gestor"     → CRUD completo + catálogo
  └── "admin"      → Todo acceso + dashboard + admin Django
```

---

## 23. Specification (Q Objects)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Combina reglas de negocio usando operadores lógicos |
| **Dónde** | `website/views.py` (búsqueda con `Q`) |
| **Cómo** | `Q(first_name__icontains=q) | Q(last_name__icontains=q)` |
| **Por qué** | Búsqueda flexible combinando múltiples criterios |

```python
results = Record.objects.filter(
    Q(first_name__icontains=query) |
    Q(last_name__icontains=query) |
    Q(email__icontains=query) |
    Q(phone__icontains=query)
)
```

---

# PATRONES ARQUITECTÓNICOS

## 24. MVT (Model-View-Template)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Variante de MVC de Django: Model (datos), View (lógica), Template (presentación) |
| **Dónde** | Todo el proyecto |
| **Cómo** | `models.py` → `views.py` → `templates/*.html` |
| **Por qué** | Es la arquitectura nativa de Django |

```
  Navegador
      │
      ▼
  urls.py ───→ views.py ───→ models.py
      │            │              │
      │            ▼              │
      │      templates/*.html     │
      │            │              │
      ◄────────────┴──────────────┘
```

---

## 25. Front Controller / Dispatcher

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Mecanismo central de enrutamiento que dirige todas las peticiones |
| **Dónde** | `dcrm/urls.py`, todas las `urls.py` de cada app |
| **Cómo** | `ROOT_URLCONF` → `include()` → `path()` → view function |
| **Por qué** | Centraliza el enrutamiento, facilita la navegación |

---

## 26. Configuration Module

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Centraliza toda la configuración de la aplicación |
| **Dónde** | `dcrm/settings.py` |
| **Cómo** | Variables de configuración para BD, seguridad, apps, middleware, etc. |
| **Por qué** | Un solo punto de configuración, fácil de modificar |

---

## 27. Service Locator

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Punto central donde se obtienen servicios |
| **Dónde** | `website/views.py`, `productos/views.py` |
| **Cómo** | Variables globales de módulo (`_record_service`, `_producto_service`) |
| **Por qué** | Las vistas acceden a servicios sin acoplarse a su creación |

---

## 28. Eager Loading

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Carga datos relacionados en una sola consulta SQL (JOIN) |
| **Dónde** | `catalogo/views.py` |
| **Cómo** | `Catalogo.objects.select_related("categoria", "producto")` |
| **Por qué** | Reduce el número de consultas a la BD (problema N+1) |

---

## 29. Template Tag / Helper

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Extiende el motor de templates con funcionalidad personalizada |
| **Dónde** | `website/templatetags/nav_extras.py` |
| **Cómo** | `{% active_link 'home' %}` → resalta el link activo |
| **Por qué** | Mantiene la lógica de presentación fuera de las vistas |

```python
@register.simple_tag(takes_context=True)
def active_link(context, url_name):
    request = context.get("request")
    if request and request.resolver_match and request.resolver_match.url_name == url_name:
        return "active"
    return ""
```

---

## 30. Logging (Observer Variant)

| Aspecto | Descripción |
|---------|-------------|
| **Qué es** | Sistema de registro de eventos que notifica a manejadores configurados |
| **Dónde** | `core/security.py`, `dcrm/settings.py` |
| **Cómo** | `logging.getLogger("django.security")` escribe a `security.log` |
| **Por qué** | Auditoría y detección de intentos de ataque |

---

# RESUMEN: Mapa de Patrones por Archivo

```
dcrm/
├── core/
│   ├── models.py       → Abstract Base Class, Template Method, Field Encapsulation
│   ├── services.py     → Abstract Base Class, Strategy, Facade, Adapter, DI
│   ├── repository.py   → Repository, Adapter, Abstract Base Class
│   ├── validators.py   → Strategy, Registry, Simple Factory, Singleton
│   └── security.py     → Facade, Proxy, Logging (Observer)
├── usuarios/
│   ├── models.py       → Role, Value Object, Field Encapsulation
│   ├── forms.py        → ModelForm, Factory Method, Composite Form, Template Method
│   ├── signals.py      → Observer, Decorator
│   └── apps.py         → Observer Registration
├── website/
│   ├── views.py        → Singleton, Decorator, Protection Proxy, Facade, Specification
│   ├── forms.py        → ModelForm, Factory Method, Template Method, Alias
│   ├── models.py       → Abstract Base Class (herencia), Domain Model
│   ├── export.py       → Decorator, DTO, Strategy
│   ├── urls.py         → Front Controller, Error Handler
│   └── templatetags/   → Singleton, Decorator, Template Tag
├── productos/
│   ├── views.py        → Singleton, Decorator, Facade, Pagination, Proxy
│   ├── forms.py        → ModelForm
│   └── models.py       → Abstract Base Class (herencia)
├── catalogo/
│   ├── models.py       → Abstract Base Class, Foreign Key Association
│   └── views.py        → Decorator, Pagination, Eager Loading
└── dcrm/
    ├── settings.py      → Configuration Module, Chain of Responsibility, Strategy, Logging
    ├── urls.py          → Front Controller, Facade, Composite Dispatcher
    ├── asgi.py          → Factory Method
    └── wsgi.py          → Factory Method
```

---

# Principios SOLID Aplicados

| Principio | Dónde se aplica |
|-----------|----------------|
| **S**ingle Responsibility | Cada app tiene un propósito único (usuarios, productos, etc.) |
| **O**pen/Closed | `BaseModel` abierto a extensión, cerrado a modificación |
| **L**iskov Substitution | `Record`, `Producto`, etc. pueden sustituir a `BaseModel` |
| **I**nterface Segregation | Cada servicio expone solo los métodos que necesita |
| **D**ependency Inversion | `CrudService` depende de abstracciones (`BaseService`, inyección) |

---

# Principio DRY

| Antes (duplicado) | Después (DRY con patrones) |
|-------------------|---------------------------|
| `Record.objects.all().order_by("id")` en cada vista | `_record_service.get_all()` |
| `_created_at` + `_updated_at` en cada modelo | `BaseModel` abstracto |
| `if not request.user.is_authenticated` en cada vista | `@login_required` decorator |
| HTML repetido en cada página | `{% extends 'base.html' %}` |
| Formularios escritos a mano | `ModelForm` genera automáticamente |
