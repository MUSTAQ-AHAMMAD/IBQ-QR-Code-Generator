# Troubleshooting Guide

## Error: Traceback at app.py line 17

### Problem
When running `python app.py`, you encounter a traceback error at line 17, which contains the import statement for utilities.

### Root Cause
This error typically occurs due to missing Python dependencies (Flask and related packages not installed in your virtual environment).

### Solution

#### For Windows Users (MINGW64/Git Bash)

1. **Activate your virtual environment:**
   ```bash
   source venv/Scripts/activate
   ```
   Or in Windows Command Prompt:
   ```cmd
   venv\Scripts\activate
   ```

2. **Upgrade pip (recommended):**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Install all required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -c "import flask; print(flask.__version__)"
   ```
   This should print the Flask version (e.g., `3.0.0`) without errors.

5. **Run the application:**
   ```bash
   python app.py
   ```

#### For Linux/Mac Users

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

### Common Issues and Solutions

#### Issue: "No module named 'flask'"
**Solution:** Your virtual environment doesn't have Flask installed. Follow steps above to install requirements.

#### Issue: PIL/Pillow AttributeError with Image.LANCZOS
**Problem:** Error like `AttributeError: module 'PIL.Image' has no attribute 'LANCZOS'` at line 97 in PIL/Image.py or when using QR code generation features.

**Root Cause:** Pillow 10.0.0+ deprecated direct access to resampling filters like `Image.LANCZOS`. These have been moved to `Image.Resampling.LANCZOS`.

**Solution:** This has been fixed in the codebase. All references to deprecated constants like `Image.LANCZOS` have been updated to `Image.Resampling.LANCZOS`. If you see this error:
1. Pull the latest code: `git pull origin main`
2. Reinstall Pillow: `pip install --upgrade Pillow>=11.0.0`
3. Restart the application

#### Issue: ImportError: cannot import name '_imaging' from 'PIL' (Windows)
**Problem:** When trying to import PIL/Pillow, you get an error like:
```
ImportError: cannot import name '_imaging' from 'PIL' (C:\path\to\venv\Lib\site-packages\PIL\__init__.py)
```

**Root Cause:** This error indicates a corrupted Pillow installation. The `_imaging` module is a compiled C extension that's essential for Pillow to work. This commonly occurs on Windows when:
- Pillow was installed but the binary components weren't properly compiled/copied
- Pip's cache contains corrupted files
- There's a conflict with another package or Python installation
- Antivirus software interfered with the installation

**Solution (Windows Users):**

**Method 1: Clean reinstall with cache clearing (Recommended)**
```bash
# Activate your virtual environment
source venv/Scripts/activate  # Git Bash/MINGW64
# OR
venv\Scripts\activate  # Command Prompt

# Uninstall Pillow completely
pip uninstall -y Pillow

# Clear pip cache (important!)
pip cache purge

# Reinstall with no cache
pip install --no-cache-dir "Pillow>=11.0.0"

# Verify installation
python -c "from PIL import Image; print('PIL import successful, version:', Image.__version__)"
```

**Method 2: Force reinstall from wheel**
```bash
# Uninstall existing Pillow
pip uninstall -y Pillow

# Install with force-reinstall and no-cache flags
pip install --force-reinstall --no-cache-dir "Pillow>=11.0.0"

# Verify
python -c "from PIL import Image; print('Success!')"
```

**Method 3: Fresh virtual environment (if above methods fail)**
```bash
# Deactivate current environment
deactivate

# Remove corrupted virtual environment
rm -rf venv  # Git Bash
# OR
rmdir /s /q venv  # Command Prompt

# Create fresh virtual environment
python -m venv venv

# Activate new environment
source venv/Scripts/activate  # Git Bash
# OR
venv\Scripts\activate  # Command Prompt

# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements fresh
pip install --no-cache-dir -r requirements.txt

# Verify
python -c "from PIL import Image; print('Success! PIL version:', Image.__version__)"
```

**Method 4: Use pre-built wheel (alternative)**
```bash
# Download and install from PyPI directly
pip install --no-cache-dir --force-reinstall --upgrade Pillow
```

**Additional Windows-specific checks:**
- Ensure no antivirus is blocking pip installations (temporarily disable if needed)
- Run Git Bash or Command Prompt as Administrator if permissions are an issue
- Check that you have Visual C++ Redistributables installed (required for compiled extensions)
- Verify Python version is 64-bit if you're on a 64-bit system: `python -c "import platform; print(platform.architecture())"`

#### Issue: "No module named 'werkzeug'" or similar
**Solution:** Some dependencies are missing. Run `pip install -r requirements.txt` again.

#### Issue: Virtual environment not activating
**Solution:**
- Ensure you created the virtual environment: `python -m venv venv`
- On Windows, you may need to allow script execution:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

#### Issue: Import errors after pulling new changes
**Solution:**
1. Pull the latest changes: `git pull origin <branch-name>`
2. Reinstall requirements (in case dependencies changed): `pip install -r requirements.txt`
3. Run database migrations if needed: `python migrations_v2.py`

#### Issue: Database errors on startup
**Solution:**
1. The app automatically runs migrations on startup
2. If you encounter SQLite column errors, run: `python migrations_v2.py`
3. Or delete the database file (for development only): `rm instance/app.db`

### Environment Setup Checklist

Before running the application, ensure:

- [ ] Python 3.8+ is installed
- [ ] Virtual environment is created (`python -m venv venv`)
- [ ] Virtual environment is activated
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists (copy from `.env.example` if needed)
- [ ] Database directory exists (`mkdir -p instance`)

### Quick Start Commands

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file (if not exists)
cp .env.example .env

# Run the application
python app.py
```

### Production Setup

For production deployment, install production dependencies:

```bash
pip install -r requirements-prod.txt
```

Then run with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Getting Help

If you continue to experience issues:

1. Check that your Python version is 3.8 or higher: `python --version`
2. Ensure your virtual environment is activated (you should see `(venv)` in your prompt)
3. Try creating a fresh virtual environment:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
4. Check for any error messages in the full traceback and search for similar issues

### Database Migration Issues

If you encounter "no such column" errors:

1. The application automatically runs migrations on startup via `_run_database_migrations()` function
2. For manual migration, run: `python migrations_v2.py`
3. The migrations use SQLite-compatible ALTER TABLE syntax with column existence checks

See `SQLITE_MIGRATION_FIX.md` for detailed information about SQLite migration handling.
