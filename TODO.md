# Moka Cafe Website Autofix and Autocomplete Plan

## Information Gathered

The project has two app setups:

- Monolithic in `run.py`
- Modular factory in `app/`

Key points:

- `run.py` includes models, contact routes, and sample data creation
- `app/` has modular structure with models, forms, routes for main and admin
- Templates are in `app/templates/`
- Database file `database.db` exists
- Static files in `static/`

Inconsistencies found:

- Database URI ('cafe.db' vs 'database.db')
- Missing contact in app/routes.py
- Import issues

## Plan

1. **Merge Models**: Add ContactMessage model to `app/models.py`
2. **Update Routes**: Add contact routes to `app/routes.py`, fix imports (add current_app)
3. **Fix App Factory**: Update `app/__init__.py` to use 'database.db', add sample data creation
4. **Update Entry Point**: Modify `run.py` to use create_app(), remove redundant code
5. **Fix Templates/Static**: Ensure all paths are correct
6. **Complete Features**: Ensure all routes and functionality work
7. **Test App**: Run and verify

## Dependent Files

- `app/models.py`: Add ContactMessage
- `app/routes.py`: Add contact routes, fix imports
- `app/__init__.py`: Change DB URI, add sample data
- `run.py`: Simplify to use factory
- Templates: Verify paths

## Followup Steps

- Install dependencies if needed
- Run `python run.py` to test
- Check for any errors and fix
