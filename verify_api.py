"""Verify API configuration."""
from main import app

print("✓ App initialized successfully")
print(f"✓ Title: {app.title}")
print(f"✓ Version: {app.version}")
print()
print("📚 Documentation URLs:")
print("   - Swagger UI: http://127.0.0.1:8080/docs")
print("   - ReDoc: http://127.0.0.1:8080/redoc")
print("   - OpenAPI JSON: http://127.0.0.1:8080/openapi.json")
print()
print("🔗 Main API Routes:")
for route in app.routes:
    if 'api/users' in route.path:
        methods = list(route.methods) if hasattr(route, 'methods') else ['GET']
        print(f"   - {route.path} {methods}")
