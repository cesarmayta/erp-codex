# ERP Codex

ERP retail para una sola empresa, construido con Django, Django REST Framework y PostgreSQL en el schema `public`.

## Modulos actuales

- empresa, sucursales, almacenes y parametros
- categorias, productos, stock y movimientos
- clientes y ventas
- cajas, sesiones y movimientos de caja
- punto de venta web con Bootstrap

## Puesta en marcha

```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py bootstrap_empresa1
python manage.py runserver
```

Tambien puedes usar:

```bash
./scripts/run_empresa1_demo.sh
```

## Acceso demo

- URL: `http://127.0.0.1:8000/`
- usuario: `admin`
- clave: `admin123`

## Navegacion

- `/` dashboard
- `/inventario/productos/` productos
- `/ventas/clientes/` clientes
- `/caja/sesiones/` caja
- `/pos/` punto de venta
