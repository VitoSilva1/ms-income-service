# ms-income-service

Servicio FastAPI dedicado a **registrar los ingresos** de los usuarios y proveer consultas filtradas o resúmenes agregados. Complementa a `ms-expense-service` para el cálculo de balances en el dashboard.

## Características
- Modelo `Income` con campos `salary`, `bonus`, `other_income`, `total_income` y fecha (`income_date`).
- Filtros por usuario y por rango de fechas en `GET /incomes/`.
- Operaciones CRUD completas (`create`, `list`, `get`, `update`, `delete`).
- Endpoint `summarize_income` (utilizado internamente) que agrupa los montos por tipo de ingreso.

## Ejecución
```bash
cd BackendFinTrack/ms-income-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

Con Docker:
```bash
cd BackendFinTrack/ms-income-service
docker compose up --build
```

## Endpoints
- `POST /incomes/`: crea un ingreso individual.
- `GET /incomes/`: lista ingresos filtrando por `user_id` y opcionalmente `date_from`, `date_to`.
- `GET /incomes/{income_id}`: retorna un ingreso (validando opcionalmente `user_id`).
- `PATCH /incomes/{income_id}`: actualiza un ingreso.
- `DELETE /incomes/{income_id}`: elimina un ingreso.

## Notas de implementación
Toda la lógica está en `app/services/income_service.py`. Si deseas añadir pruebas unitarias, puedes reutilizar una sesión SQLite en memoria para cubrir:
- Validaciones de `get_income` (404 cuando no existe).
- Filtros de `list_income`.
- Cálculo de `summarize_income`.
