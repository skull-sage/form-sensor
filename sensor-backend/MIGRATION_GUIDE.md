# Migration Guide: Modular Architecture

## What Changed

### Backend Changes

1. **Folder Rename**: `app/` → `form-sensor/`
   - The module now has a descriptive name matching its purpose

2. **New File**: `form-sensor/router.py`
   - All API endpoints moved from `main.py` to module router
   - Router uses `/form-sensor` prefix for all endpoints

3. **Updated main.py**:
   - Simplified to focus on app initialization
   - Includes module routers instead of defining endpoints
   - Service injection pattern for module routers

### API Endpoint Changes

All form-sensor endpoints now have the `/form-sensor` prefix:

**Old URLs** → **New URLs**:
- `/create-text-sensor/{id}` → `/form-sensor/create-text-sensor/{id}`
- `/text-sensor/{id}` → `/form-sensor/text-sensor/{id}`
- `/text-sensors` → `/form-sensor/text-sensors`
- `/bulk-create-sensors` → `/form-sensor/bulk-create-sensors`

**Unchanged**:
- `/` - Root endpoint
- `/health` - Health check
- `/reload-model` - Model reload

### Frontend Changes

Updated API URLs in:
- `sensor-ui/src/app-main/form-sensor/field-list.vue`
- `sensor-ui/src/app-main/form-sensor/field-verify.vue`

All fetch calls now use the `/form-sensor` prefix.

## Testing the Changes

### 1. Start the Backend
```bash
cd sensor-backend
python main.py
```

### 2. Verify API Documentation
Visit: http://localhost:8000/docs

You should see endpoints grouped under the "form-sensor" tag.

### 3. Start the Frontend
```bash
cd sensor-ui
pnpm dev
```

### 4. Test Functionality
- Navigate to `/smart-form/list`
- Create a new sensor
- Navigate to `/smart-form/verify`
- Test similarity checking

## Rollback (if needed)

If you need to rollback:
1. Rename `form-sensor/` back to `app/`
2. Restore original `main.py` from git
3. Update frontend URLs to remove `/form-sensor` prefix

## Next Steps

With this modular structure, you can now:
1. Add new modules alongside `form-sensor/`
2. Each module manages its own routes, services, and schemas
3. Share common utilities across modules
4. Scale the application horizontally
