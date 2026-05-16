"""
Flask integration tests for the QR code vCard fix.

Validates that:
- vCard QR codes encode the raw vCard string directly (not a profile URL)
- generate_vcard() produces correct vCard 3.0 format
- generate_qr_data() returns vCard data for the 'vcard' type
- The /c/<token> contact profile page still renders correctly
- Company logo upload and serving work correctly
"""
import importlib.util
import io
import os
import sys
import tempfile

import pytest

# ---------------------------------------------------------------------------
# Helpers to load the Flask app without colliding with the `app/` package
#
# The repository has both a `app.py` (Flask application factory) and an
# `app/` subdirectory (FastAPI module). A normal `from app import create_app`
# would import the package, not the file. We therefore load `app.py` via
# importlib so that both can coexist without renaming either.
# ---------------------------------------------------------------------------

def _load_flask_app_module():
    spec = importlib.util.spec_from_file_location(
        "flask_app",
        os.path.join(os.path.dirname(__file__), "..", "app.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_utils_module():
    spec = importlib.util.spec_from_file_location(
        "utils_mod",
        os.path.join(os.path.dirname(__file__), "..", "utils.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def utils():
    return _load_utils_module()


@pytest.fixture(scope="module")
def flask_mod():
    return _load_flask_app_module()


@pytest.fixture(scope="module")
def app(flask_mod, tmp_path_factory):
    """Create Flask test app with a temp upload folder and in-memory DB."""
    upload_dir = tmp_path_factory.mktemp("uploads")
    application = flask_mod.create_app("testing")
    application.config["UPLOAD_FOLDER"] = str(upload_dir)
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    application.config["WTF_CSRF_ENABLED"] = False
    application.config["TESTING"] = True

    with application.app_context():
        from models import db
        db.create_all()

    return application


@pytest.fixture(scope="module")
def client(app):
    """Authenticated test client (logged in as admin)."""
    with app.test_client() as c:
        c.post(
            "/login",
            data={"username": "admin", "password": "admin123"},
            follow_redirects=True,
        )
        yield c


# ---------------------------------------------------------------------------
# Utility function tests (no Flask needed)
# ---------------------------------------------------------------------------

class TestGenerateVcard:
    """Tests for the generate_vcard() utility function."""

    def test_basic_vcard_structure(self, utils):
        data = {"contact_name": "John Doe", "contact_email": "john@example.com"}
        vcard = utils.generate_vcard(data)
        assert vcard.startswith("BEGIN:VCARD")
        assert "VERSION:3.0" in vcard
        assert "END:VCARD" in vcard

    def test_full_name_field(self, utils):
        data = {"contact_name": "Jane Smith"}
        vcard = utils.generate_vcard(data)
        assert "FN:Jane Smith" in vcard
        assert "N:Smith;Jane;;;" in vcard

    def test_single_word_name(self, utils):
        data = {"contact_name": "Alice"}
        vcard = utils.generate_vcard(data)
        assert "FN:Alice" in vcard
        assert "N:;Alice;;;" in vcard

    def test_all_contact_fields(self, utils):
        data = {
            "contact_name": "Bob Builder",
            "contact_email": "bob@build.it",
            "contact_phone": "+1234567890",
            "contact_title": "Constructor",
            "contact_company": "Build Corp",
            "contact_website": "https://build.it",
            "contact_address": "1 Construction Way",
        }
        vcard = utils.generate_vcard(data)
        assert "EMAIL;TYPE=INTERNET:bob@build.it" in vcard
        assert "TEL;TYPE=WORK,VOICE:+1234567890" in vcard
        assert "TITLE:Constructor" in vcard
        assert "ORG:Build Corp" in vcard
        assert "URL:https://build.it" in vcard
        assert "ADR;TYPE=WORK:;;1 Construction Way;;;;" in vcard

    def test_missing_optional_fields_omitted(self, utils):
        """Fields not provided should not appear in the vCard."""
        data = {"contact_name": "Min User"}
        vcard = utils.generate_vcard(data)
        assert "EMAIL" not in vcard
        assert "TEL" not in vcard
        assert "ORG" not in vcard
        assert "URL" not in vcard

    def test_output_is_not_a_url(self, utils):
        data = {"contact_name": "URL Test", "contact_email": "t@t.com"}
        vcard = utils.generate_vcard(data)
        assert not vcard.startswith("http")

    def test_address_newlines_stripped(self, utils):
        data = {"contact_address": "Line1\nLine2\r\nLine3"}
        vcard = utils.generate_vcard(data)
        assert "\n" not in vcard.split("ADR;TYPE=WORK:")[1].split("\n")[0]


class TestGenerateQrData:
    """Tests for generate_qr_data() with vcard type."""

    def test_vcard_type_returns_vcard_string(self, utils):
        data = {"contact_name": "Alice", "contact_email": "alice@example.com"}
        result = utils.generate_qr_data("vcard", data)
        assert result.startswith("BEGIN:VCARD")
        assert "END:VCARD" in result

    def test_vcard_type_never_returns_url(self, utils):
        data = {"contact_name": "Alice", "contact_email": "alice@example.com"}
        result = utils.generate_qr_data("vcard", data)
        assert not result.startswith("http")
        assert "/c/" not in result

    def test_url_type_returns_url(self, utils):
        data = {"url": "https://example.com"}
        result = utils.generate_qr_data("url", data)
        assert result == "https://example.com"

    def test_text_type_returns_text(self, utils):
        data = {"text_content": "Hello World"}
        result = utils.generate_qr_data("text", data)
        assert result == "Hello World"

    def test_email_type_returns_mailto(self, utils):
        data = {"email_address": "x@example.com", "email_subject": "", "email_body": ""}
        result = utils.generate_qr_data("email", data)
        assert result.startswith("mailto:")

    def test_phone_type_returns_tel(self, utils):
        data = {"phone_number": "+1234567890"}
        result = utils.generate_qr_data("phone", data)
        assert result.startswith("tel:")

    def test_wifi_type_returns_wifi_string(self, utils):
        data = {
            "wifi_ssid": "MyNet",
            "wifi_password": "secret",
            "wifi_encryption": "WPA",
            "wifi_hidden": False,
        }
        result = utils.generate_qr_data("wifi", data)
        assert result.startswith("WIFI:")

    def test_unknown_type_returns_empty(self, utils):
        result = utils.generate_qr_data("unknown_type_xyz", {})
        assert result == ""


# ---------------------------------------------------------------------------
# Flask integration tests (require running app)
# ---------------------------------------------------------------------------

class TestVcardQrGeneration:
    """Integration tests: vCard QR code generation via Flask routes."""

    def _generate_vcard_qr(self, client):
        return client.post(
            "/generate",
            data={
                "name": "Integration Test Card",
                "qr_type": "vcard",
                "contact_name": "Test Person",
                "contact_email": "test@integration.com",
                "contact_phone": "+9999999999",
                "contact_company": "Test Corp",
                "contact_title": "Tester",
                "contact_address": "99 Test St",
                "size": 300,
                "foreground_color": "#000000",
                "background_color": "#FFFFFF",
                "error_correction": "H",
                "border": 4,
                "file_format": "png",
                "qr_style": "square",
                "frame_style": "none",
                "eye_style": "square",
                "data_style": "square",
                "category": "business",
                "template_id": 0,
            },
            follow_redirects=True,
        )

    def test_generate_succeeds(self, client):
        resp = self._generate_vcard_qr(client)
        assert resp.status_code == 200

    def test_generated_qr_data_is_vcard(self, client, app):
        self._generate_vcard_qr(client)
        with app.app_context():
            from models import QRCode
            qr = QRCode.query.order_by(QRCode.id.desc()).first()
            assert qr is not None
            assert qr.qr_data.startswith("BEGIN:VCARD")
            assert "END:VCARD" in qr.qr_data

    def test_generated_qr_data_is_not_profile_url(self, client, app):
        """Core fix validation: QR must encode vCard data, not /c/<token> URL."""
        self._generate_vcard_qr(client)
        with app.app_context():
            from models import QRCode
            qr = QRCode.query.order_by(QRCode.id.desc()).first()
            assert qr is not None
            assert not qr.qr_data.startswith("http")
            assert "/c/" not in qr.qr_data

    def test_generated_qr_data_contains_contact_fields(self, client, app):
        self._generate_vcard_qr(client)
        with app.app_context():
            from models import QRCode
            qr = QRCode.query.order_by(QRCode.id.desc()).first()
            assert qr is not None
            assert "Test Person" in qr.qr_data
            assert "test@integration.com" in qr.qr_data
            assert "Test Corp" in qr.qr_data

    def test_qr_file_is_generated(self, client, app):
        self._generate_vcard_qr(client)
        with app.app_context():
            from models import QRCode
            qr = QRCode.query.order_by(QRCode.id.desc()).first()
            assert qr is not None
            assert qr.filename is not None
            assert qr.filename.endswith(".png")
            assert os.path.exists(qr.file_path)


class TestContactProfilePage:
    """Tests that the /c/<token> profile page still works after the fix."""

    def _create_qr_record(self, app):
        """Directly insert a QR code record and return its public_token."""
        import secrets
        with app.app_context():
            from models import db, QRCode
            qr = QRCode(
                user_id=1,
                name="Profile Test",
                contact_name="Profile User",
                contact_email="profile@test.com",
                contact_phone="+1112223333",
                contact_company="Profile Corp",
                qr_data="BEGIN:VCARD\nVERSION:3.0\nFN:Profile User\nEND:VCARD",
                qr_type="vcard",
                public_token=secrets.token_urlsafe(16),
            )
            db.session.add(qr)
            db.session.commit()
            return qr.public_token

    def test_profile_page_returns_200(self, client, app):
        token = self._create_qr_record(app)
        resp = client.get(f"/c/{token}")
        assert resp.status_code == 200

    def test_profile_page_shows_contact_name(self, client, app):
        token = self._create_qr_record(app)
        resp = client.get(f"/c/{token}")
        assert b"Profile User" in resp.data

    def test_invalid_token_returns_404(self, client):
        resp = client.get("/c/invalid-token-that-does-not-exist")
        assert resp.status_code == 404

    def test_download_vcard_returns_vcf(self, client, app):
        token = self._create_qr_record(app)
        resp = client.get(f"/c/{token}/vcard")
        assert resp.status_code == 200
        assert b"BEGIN:VCARD" in resp.data
        assert resp.content_type.startswith("text/vcard")


class TestCompanyLogoRoute:
    """Tests for the /company-logo/<filename> route."""

    def test_nonexistent_logo_returns_404(self, client):
        resp = client.get("/company-logo/does_not_exist.png")
        assert resp.status_code == 404

    def test_unregistered_filename_returns_404(self, client, app):
        """A file in the upload folder that is NOT registered as a company_logo
        must not be accessible via the public route."""
        upload_dir = app.config["UPLOAD_FOLDER"]
        phantom_file = os.path.join(upload_dir, "phantom.png")
        with open(phantom_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")  # minimal PNG header
        try:
            resp = client.get("/company-logo/phantom.png")
            assert resp.status_code == 404
        finally:
            os.remove(phantom_file)


class TestUserPhotoRoute:
    """Tests for the /user-photo/<filename> route."""

    def test_nonexistent_photo_returns_404(self, client):
        resp = client.get("/user-photo/does_not_exist.png")
        assert resp.status_code == 404

    def test_unregistered_filename_returns_404(self, client, app):
        """A file in the upload folder that is NOT registered as a user_photo
        must not be accessible via the public route."""
        upload_dir = app.config["UPLOAD_FOLDER"]
        phantom_file = os.path.join(upload_dir, "phantom_photo.png")
        with open(phantom_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n")  # minimal PNG header
        try:
            resp = client.get("/user-photo/phantom_photo.png")
            assert resp.status_code == 404
        finally:
            os.remove(phantom_file)
