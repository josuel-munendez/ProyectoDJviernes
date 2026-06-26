# Patrones Clave para Sustentación

Basado en los materiales de formación y el código del proyecto.  
Documentación completa de 30 patrones en `docs/patrones_diseno.md` (apéndice).

---

# PARTE 1: PATRONES DE DISEÑO (GoF)

## 1. Singleton

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón creacional que garantiza que una clase tenga **una única instancia** en toda la aplicación |
| **¿Dónde está?** | `dcrm/core/services.py` y las variables `_record_service`, `_producto_service` en las vistas |
| **¿Qué hace?** | Cada servicio CRUD se crea una sola vez y se reutiliza en toda la app |
| **¿Por qué?** | Evita crear mil instancias innecesarias, ahorra memoria y centraliza la lógica |
| **Código clave** | `_record_service = CrudService(Record)` en `website/views.py:10` |
| **La profe lo enseñó** | ✅ Sí — `14-11-2025 poo/models/database.py` línea 1: `# patron sigliton` con `__new__` |

**Explicación oral:**  
"Singleton lo aplicamos en el servicio CRUD. En vez de crear un nuevo servicio cada vez que necesitamos operar con la base de datos, creamos uno solo al iniciar la aplicación y lo reutilizamos. Esto es como tener una única puerta de entrada a los datos."

**Diagrama:**
```
  Aplicación
  ┌─────────────────────────┐
  │  _record_service ───────┼── CrudService(Record)     ← Una sola
  │  _producto_service ─────┼── CrudService(Producto)   ← Una sola
  │  admin.site ────────────┼── AdminSite               ← Una sola
  └─────────────────────────┘
```

---

## 2. Repository

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón estructural que **abstrae el acceso a datos**, separando la lógica de negocio de la BD |
| **¿Dónde está?** | `dcrm/core/repository.py` — `BaseRepository` y `DjangoRepository` |
| **¿Qué hace?** | Provee métodos como `find_all()`, `find_by_id()`, `save()`, `remove()` sin exponer SQL |
| **¿Por qué?** | Si cambiamos de SQLite a MySQL, el código de negocio NO cambia, solo el repositorio |
| **Código clave** | `class DjangoRepository(BaseRepository):` y `def find_all(self): return self._model_class.objects.all()` |
| **La profe lo enseñó** | ✅ Sí — mencionado en Clase 5 y la actividad de patrones |

**Explicación oral:**  
"Repository es una capa intermedia entre la lógica del negocio y la base de datos. Mi código nunca escribe SQL directamente; llama a `repositorio.find_all()` y el repositorio decide cómo traer los datos. Así, si mañana cambiamos de base de datos, solo cambiamos el repositorio."

**Diagrama:**
```
  Vista (lógica)  ──→  BaseRepository (contrato)  ──→  DjangoRepository (impl)  ──→  ORM  ──→  BD
       find_all()         find_all()                      .all()                      SQL
```

---

## 3. Template Method

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón de comportamiento que define el **esqueleto de un algoritmo** y delega pasos a subclases |
| **¿Dónde está?** | `dcrm/core/models.py` — `BaseModel` como clase abstracta, y los formularios `ModelForm.save()` |
| **¿Qué hace?** | `BaseModel` define `_created_at`, `_updated_at` y `get_metadata()`; los modelos hijos heredan sin modificar |
| **¿Por qué?** | DRY (No Repetirse): todos los modelos comparten campos de fecha sin escribirlos cada vez |
| **Código clave** | `class BaseModel(models.Model): class Meta: abstract = True` |
| **La profe lo enseñó** | ✅ Sí — mencionado explícitamente en Clase 5 como Template Method |

**Explicación oral:**  
"Template Method es como una plantilla. `BaseModel` define los campos de fecha de creación y actualización que todos los modelos van a tener. Luego `Record`, `Producto`, `Categoria` y `Catalogo` heredan de esa plantilla sin tener que escribir esos campos cada vez."

**Jerarquía:**
```
  BaseModel (abstracta) ─── tiene _created_at, _updated_at
    ├── Record          ─── hereda sin cambios
    ├── Producto        ─── hereda sin cambios
    ├── Categoria       ─── hereda sin cambios
    └── Catalogo        ─── hereda sin cambios
```

---

## 4. Strategy

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón de comportamiento que define una **familia de algoritmos intercambiables** |
| **¿Dónde está?** | `dcrm/core/validators.py` — `RegexValidator` con distintas validaciones por tipo de campo |
| **¿Qué hace?** | Según el tipo de campo (email, teléfono, password), aplica una validación específica |
| **¿Por qué?** | Los campos se validan de manera diferente; con Strategy podemos añadir nuevos tipos sin modificar código existente |
| **Código clave** | `RegexValidator.validate("email", valor)` o `RegexValidator.validate("phone", valor)` |
| **Está en el catálogo GoF** | ✅ Sí |

**Explicación oral:**  
"Strategy lo usamos en las validaciones. Cada tipo de campo tiene su propia estrategia: el email se valida con una expresión regular, el teléfono con otra, la contraseña con otra. Todas son intercambiables y podemos agregar una nueva validación sin tocar las existentes."

---

## 5. Observer (Señales de Django)

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón de comportamiento donde un **sujeto notifica** a múltiples observadores cuando cambia |
| **¿Dónde está?** | `dcrm/usuarios/signals.py` — señal `post_save` de `User` |
| **¿Qué hace?** | Cuando se crea un `User`, automáticamente se crea su `UserProfile` sin acoplar código |
| **¿Por qué?** | Desacopla la creación del usuario de la creación del perfil |
| **Código clave** | `@receiver(post_save, sender=User)` y `def create_user_profile(sender, instance, created, **kwargs)` |
| **Está en el catálogo GoF** | ✅ Sí |

**Explicación oral:**  
"Django usa Observer con las señales. Cuando un usuario se registra, Django emite una señal `post_save` y nuestro código, que está escuchando, crea automáticamente el perfil del usuario con su rol. Así el código de registro no necesita saber cómo se crea el perfil."

---

## 6. Decorator

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón estructural que **agrega responsabilidades** a un objeto dinámicamente |
| **¿Dónde está?** | En todas las vistas protegidas: `@login_required` |
| **¿Qué hace?** | Envuelve la función para verificar autenticación antes de ejecutar la lógica real |
| **¿Por qué?** | Sepala la seguridad de la lógica de negocio; el código de la vista solo hace CRUD |
| **Código clave** | `@login_required` antes de cada función que requiere autenticación |
| **Está en el catálogo GoF** | ✅ Sí |

**Explicación oral:**  
"Decorator en Python es como una envoltura. Ponemos `@login_required` arriba de cada vista y Django automáticamente verifica que el usuario esté autenticado antes de ejecutar la función. La vista no tiene que preocuparse por la seguridad, solo por su lógica."

---

## 7. Factory Method (ModelForm)

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Patrón creacional que **encapsula la creación de objetos** |
| **¿Dónde está?** | Todos los `forms.py` — `form.save()` que crea instancias de modelos |
| **¿Qué hace?** | `UserRegisterForm.save()` crea un `User` y automáticamente crea el `UserProfile` |
| **¿Por qué?** | Centraliza la lógica de creación en un solo lugar |
| **Código clave** | `def save(self, commit=True):` en `usuarios/forms.py` |
| **Está en el catálogo GoF** | ✅ Sí |

---

# PARTE 2: CONCEPTOS POO

## 8. Encapsulación

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Ocultar datos internos y solo permitir acceso mediante métodos controlados |
| **¿Dónde está?** | `dcrm/core/models.py` (`_created_at`, `_updated_at`) y `dcrm/usuarios/models.py` (`_rol`) |
| **¿Cómo se aplica?** | Los campos con `_` (convención protected) + `db_column` para nombre limpio en BD |
| **¿Por qué?** | El rol del usuario no se debe modificar directamente, solo mediante `es_admin()`, etc. |
| **Código clave** | `_rol = models.CharField(db_column="rol")` y `def es_admin(self): return self._rol == self.ROL_ADMIN` |
| **La profe lo enseñó** | ✅ Sí — `7-11-2025/privados.py` y `protegidos.py` |

**Explicación oral:**  
"Encapsulación significa que los datos internos de un objeto están protegidos. En nuestro caso, el rol del usuario `_rol` tiene un guion bajo que indica que no debe modificarse directamente. Solo accedemos a través de métodos como `es_admin()` que el usuario puede llamar sin saber cómo está guardado el rol."

---

## 9. Herencia

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Una clase **hereda atributos y métodos** de otra clase padre |
| **¿Dónde está?** | `BaseModel` → `Record`, `Producto`, `Categoria`, `Catalogo` |
| **¿Cómo se aplica?** | Todos los modelos heredan `_created_at`, `_updated_at` y `get_metadata()` |
| **¿Por qué?** | Evita repetir campos comunes en cada modelo |
| **La profe lo enseñó** | ✅ Sí — conceptos básicos POO y `protegidaHereda.py` |

---

## 10. Polimorfismo

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Un mismo método se comporta diferente según el objeto que lo ejecuta |
| **¿Dónde está?** | `CrudService` funciona igual para `Record` que para `Producto` |
| **¿Cómo se aplica?** | `_record_service.delete(x)` y `_producto_service.delete(x)` usan el mismo método |
| **¿Por qué?** | Un solo servicio CRUD sirve para cualquier modelo |
| **La profe lo enseñó** | ✅ Sí — `7-11-2025/polimorfismo.py` |

---

## 11. Abstracción

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Ocultar la complejidad mostrando solo lo esencial |
| **¿Dónde está?** | `BaseService` (clase abstracta con `@abstractmethod`) |
| **¿Cómo se aplica?** | Define qué métodos debe tener un servicio, pero no cómo implementarlos |
| **¿Por qué?** | Cualquier servicio CRUD debe tener `get_all()`, `get_by_id()`, etc. |

---

# PARTE 3: ARQUITECTURA GENERAL

## 12. MVT (Model-View-Template)

| Aspecto | Respuesta |
|---------|-----------|
| **¿Qué es?** | Arquitectura nativa de Django — variante del MVC clásico |
| **Roles** | **Model** (datos en `models.py`), **View** (lógica en `views.py`), **Template** (HTML) |
| **Flujo** | URL → View (lógica) → Model (datos) → Template (presentación) → Usuario |
| **Código clave** | `urls.py` mapea rutas, `views.py` procesa, `models.py` define datos, `templates/` presenta |

---

# RESUMEN PARA LA SUSTENTACIÓN

**La profesora pidió: "Identificar al menos 5 patrones de diseño aplicables a su proyecto"**

### Mis 5 patrones oficiales (GoF):
| # | Patrón | Archivo clave | Frase para decir en la sustentación |
|---|--------|---------------|-------------------------------------|
| 1 | **Singleton** | `core/services.py` | "Un solo servicio CRUD para toda la app" |
| 2 | **Repository** | `core/repository.py` | "Separamos la lógica de negocio de la BD" |
| 3 | **Template Method** | `core/models.py` | "BaseModel como plantilla para todos los modelos" |
| 4 | **Strategy** | `core/validators.py` | "Cada campo se valida con su propia estrategia" |
| 5 | **Observer** | `usuarios/signals.py` | "Al crear un User, automaticamente se crea su perfil" |

### Conceptos POO adicionales (de 7-11-2025):
| # | Concepto | Dónde | Frase |
|---|----------|-------|-------|
| 6 | **Encapsulación** | `usuarios/models.py` `_rol` | "El rol está protegido con guion bajo" |
| 7 | **Herencia** | `core/models.py` `BaseModel` | "Record hereda de BaseModel" |
| 8 | **Polimorfismo** | `core/services.py` `CrudService` | "CrudService sirve para Record y Producto" |
| 9 | **Abstracción** | `core/services.py` `BaseService` | "BaseService define el contrato" |

### Arquitectura:
| # | Concepto | Frase |
|---|----------|-------|
| 10 | **MVT** | "Django usa Model-View-Template, donde el modelo son los datos, la vista es la lógica y el template es el HTML" |

---

**Ver apéndice completo en `docs/patrones_diseno.md` (30 patrones documentados)**
