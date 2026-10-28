from django.conf import settings
from django.db import connection
from django.http import JsonResponse


def health(request):
    """Temporary diagnostics: reports database connectivity without revealing credentials."""
    db = settings.DATABASES["default"]
    info = {
        "db_host_prefix": str(db["HOST"])[:16],
        "db_host_is_pooler": "-pooler" in str(db["HOST"]),
        "db_name": db["NAME"],
        "db_port": str(db["PORT"]),
        "sslmode": db.get("OPTIONS", {}).get("sslmode"),
    }
    try:
        tables = connection.introspection.table_names()
        info["database"] = "ok"
        info["table_count"] = len(tables)
        info["has_user_table"] = "accounts_user" in tables
    except Exception as exc:
        info["database"] = "error"
        info["error_type"] = type(exc).__name__
        info["error"] = str(exc)[:300]
    return JsonResponse(info)
