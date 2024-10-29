import pytest

from app.core.utils import decrypt_response, get_field


# Test get_field
def test_get_field_normal():
    report = [{"varid": "dsl_downstream", "varvalue": "1000000"}]
    assert get_field(report, "dsl_downstream") == 1000000


def test_get_field_human_readable():
    report = [{"varid": "dsl_downstream", "varvalue": "1000000"}]
    assert get_field(report, "dsl_downstream", human_readable=True) == 1.0


def test_get_field_not_in_report():
    report = [{"varid": "some_other_field", "varvalue": "1000"}]
    assert get_field(report, "nonexistent_field") is None


@pytest.fixture
def valid_data():
    hex_key = "4faf1e1d497339f0fbf2e9aad4a68897d22349e9bf5d75e1c02bda3a3ea41ecf"
    encrypted_data_hex = "ce1b963bdf8022386b825f75b4c07634365a12257e2727"
    expected_decrypted_text = "SpeedPort Response Data"
    return hex_key, encrypted_data_hex, expected_decrypted_text


# def test_decrypt_success(valid_data):
#     hex_key, encrypted_data_hex, expected_decrypted_text = valid_data
#     decrypted_text = decrypt_response(hex_key, encrypted_data_hex)
#     assert decrypted_text == expected_decrypted_text


def test_decrypt_invalid_key(valid_data):
    _, encrypted_data_hex, expected_decrypted_text = valid_data
    wrong_key = "000102030405060708090a0b0c0d0e00"

    with pytest.raises(
        ValueError, match="Decryption failed. Possible wrong key or tampered data."
    ):
        decrypt_response(wrong_key, encrypted_data_hex)


def test_decrypt_tampered_data(valid_data):
    hex_key, encrypted_data_hex, expected_decrypted_text = valid_data
    tampered_data = (
        encrypted_data_hex[:-1] + "0"
    )  # Modify the last character to simulate tampering
    with pytest.raises(
        ValueError, match="Decryption failed. Possible wrong key or tampered data."
    ):
        decrypt_response(hex_key, tampered_data)


def test_decrypt_invalid_hex_key():
    invalid_hex_key = "not_a_hex_key"
    encrypted_data_hex = "b1c4c5d4a1aefb8f9bb9a0633b1d2a0b"

    with pytest.raises(
        ValueError, match="Decryption failed. Possible wrong key or tampered data."
    ):
        decrypt_response(invalid_hex_key, encrypted_data_hex)
