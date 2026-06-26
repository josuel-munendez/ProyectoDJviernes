# Patrones de Diseño Implementados

## 1. Singleton

**Archivo:** `dcrm/core/services.py`

**Descripción:** El servicio CrudService se instancia una única vez por modelo, reutilizando la misma instancia en toda la aplicación.

**Implementación:**
```python
_record_service = CrudService(Record)  # Instancia única
```

**Uso:** Se evita crear múltiples conexiones o instancias de servicio para el mismo modelo.

---

## 2. Repository

**Archivo:** `dcrm/core/repository.py`

**Descripción:** Abstrae la capa de acceso a datos, separando la lógica de negocio de la persistencia.

**Implementación:**
```python
class DjangoRepository(BaseRepository):
    def find_all(self): ...
    def find_by_id(self, pk): ...
    def save(self, instance): ...
    def remove(self, instance): ...
```

**Uso:** Permite cambiar el motor de base de datos sin afectar la lógica de negocio.

---

## 3. Template Method

**Archivo:** `dcrm/core/models.py`

**Descripción:** Define el esqueleto de un modelo con métodos protegidos que las subclases pueden implementar.

**Implementación:**
```python
class BaseModel(models.Model):
    _created_at = ...
    _updated_at = ...
    def get_metadata(self): ...
```

**Uso:** Record y Producto heredan de BaseModel, compartiendo la funcionalidad de fechas de creación/actualización.

---

## 4. ModelForm (DRY)

**Archivo:** `dcrm/website/forms.py`

**Descripción:** Django genera automáticamente formularios basados en modelos, evitando duplicación de código.

**Implementación:**
```python
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [...]
```

**Uso:** Todos los CRUD del sistema usan ModelForm, siguiendo el principio DRY.

---

## 5. Polimorfismo

**Archivo:** `dcrm/website/views.py`, `dcrm/productos/views.py`

**Descripción:** Diferentes vistas usan el mismo contrato CrudService para operaciones CRUD.

**Implementación:**
```python
_record_service = CrudService(Record)
_producto_service = CrudService(Producto)
```

**Uso:** Un solo servicio CRUD funciona para cualquier modelo.

---

## 6. Encapsulamiento

**Archivo:** `dcrm/core/models.py`, `dcrm/usuarios/models.py`

**Descripción:** Atributos protegidos/privados con acceso controlado mediante métodos públicos.

**Implementación:**
```python
class UserProfile(models.Model):
    _rol = models.CharField(db_column="rol")
    def es_admin(self):
        return self._rol == self.ROL_ADMIN
```

**Uso:** Los roles solo se modifican mediante métodos específicos, no directamente.
