Write-Host "==> Creando entorno virtual..." -ForegroundColor Cyan
python -m venv entorno

Write-Host "==> Activando entorno virtual..." -ForegroundColor Cyan
& .\entorno\Scripts\Activate.ps1

Write-Host "==> Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet

Write-Host "==> (Opcional) Intentando instalar mysqlclient..." -ForegroundColor Cyan
pip install mysqlclient==2.2.8 --quiet 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "    mysqlclient instalado (MySQL disponible)" -ForegroundColor Green
} else {
    Write-Host "    mysqlclient no disponible - usando SQLite" -ForegroundColor Yellow
}

Write-Host "==> Aplicando migraciones..." -ForegroundColor Cyan
Set-Location dcrm
python manage.py migrate --noinput

Write-Host "==> Cargando datos de seed..." -ForegroundColor Cyan
python manage.py seed_data

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  Setup completo!" -ForegroundColor Green
Write-Host "  Ejecuta: cd dcrm; python manage.py runserver" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
