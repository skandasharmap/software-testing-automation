from services.auth_service.main import hash_pwd


def test_hash_pwd_stable():
    assert hash_pwd("secret") == hash_pwd("secret")
    assert hash_pwd("secret") != hash_pwd("Secret")
