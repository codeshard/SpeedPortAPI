import pytest
from Crypto.Cipher import AES

from app.core.utils import decrypt_response, get_field

report = [
    {"varid": "dsl_downstream", "varvalue": "5000000"},
    {"varid": "dsl_upstream", "varvalue": "2000000"},
    {"varid": "inet_download", "varvalue": "10000000"},
    {"varid": "inet_upload", "varvalue": "3000000"},
    {"varid": "mdevice_downspeed", "varvalue": "7000000"},
    {"varid": "mdevice_upspeed", "varvalue": "1500000"},
    {"varid": "non_bps_field", "varvalue": "42"},
]


@pytest.mark.parametrize(
    "name, human_readable, expected",
    [
        ("dsl_downstream", False, 5000000),
        ("dsl_upstream", True, 2.0),
        ("inet_download", True, 10.0),
        ("inet_upload", False, 3000000),
        ("mdevice_downspeed", True, 7.0),
        ("mdevice_upspeed", False, 1500000),
        ("non_bps_field", False, "42"),
        ("non_existing_field", False, None),
    ],
)
def test_get_field(name, human_readable, expected):
    assert get_field(report, name, human_readable) == expected


def test_get_field_empty_report():
    assert get_field([], "dsl_downstream") is None


def test_get_field_non_numeric_varvalue():
    invalid_report = [{"varid": "dsl_downstream", "varvalue": "invalid"}]
    with pytest.raises(ValueError):
        get_field(invalid_report, "dsl_downstream")


def generate_encrypted_data(hex_key, plaintext):
    key = bytes.fromhex(hex_key)
    nonce = key[:8]
    cipher = AES.new(key, AES.MODE_CCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    return (ciphertext + tag).hex()


def tamper_data(data_hex):
    return data_hex[:-1] + ("0" if data_hex[-1] != "0" else "1")


def test_decrypt_response_success():
    hex_key = "0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff"
    plaintext = "Hello, world!"
    encrypted_data_hex = generate_encrypted_data(hex_key, plaintext)
    result = decrypt_response(hex_key, encrypted_data_hex)
    assert result == plaintext


def test_decrypt_response_incorrect_key():
    hex_key = "0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff"
    wrong_hex_key = "1000111122223333444455556666777788889999aaaabbbbccccddddeeeefff1"
    plaintext = "Hello, World!"
    encrypted_data_hex = generate_encrypted_data(hex_key, plaintext)

    with pytest.raises(
        ValueError, match="Decryption failed. Possible wrong key or tampered data."
    ):
        decrypt_response(wrong_hex_key, encrypted_data_hex)


def test_decrypt_response_tampered_data():
    hex_key = "0000111122223333444455556666777788889999aaaabbbbccccddddeeeeffff"
    plaintext = "Hello, World!"
    encrypted_data_hex = generate_encrypted_data(hex_key, plaintext)
    tampered_data_hex = tamper_data(encrypted_data_hex)

    with pytest.raises(
        ValueError, match="Decryption failed. Possible wrong key or tampered data."
    ):
        decrypt_response(hex_key, tampered_data_hex)
