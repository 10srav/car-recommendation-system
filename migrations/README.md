# Database Migrations

This directory contains Alembic database migration scripts.

## Commands

### Create a new migration
```bash
# Auto-generate migration based on model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"
```

### Run migrations
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by one revision
alembic upgrade +1

# Downgrade by one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>
```

### View migration history
```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show migration history with details
alembic history --verbose
```

## Best Practices

1. Always review auto-generated migrations before applying
2. Test migrations on a copy of production data
3. Keep migrations small and focused
4. Never edit migrations that have been applied to production
5. Use descriptive migration messages

## SQLite Considerations

SQLite has limited ALTER TABLE support. Alembic is configured with `render_as_batch=True`
to handle this by recreating tables when necessary.
