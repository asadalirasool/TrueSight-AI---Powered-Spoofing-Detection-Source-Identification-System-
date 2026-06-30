try:
    from src.shared.database import init_db
    print("init_db imported successfully")
except Exception as e:
    print("init_db import error:", str(e))

try:
    from src.shared.database import init_database
    print("init_database imported successfully")
except Exception as e:
    print("init_database import error:", str(e))