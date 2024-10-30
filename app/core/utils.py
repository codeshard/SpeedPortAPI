import asyncio
import logging
import logging.config

import hishel
import httpx
import orjson
from Crypto.Cipher import AES

from app.core.settings import get_settings

settings = get_settings()
logging.config.dictConfig(settings.logging_config)
logger = logging.getLogger("httpx")


BPS_FIELD = [
    "dsl_downstream",
    "dsl_upstream",
    "inet_download",
    "inet_upload",
    "mdevice_downspeed",
    "mdevice_upspeed",
]


def get_field(
    report: list[dict], name: str, human_readable: bool = False
) -> str | int | float:
    """
    Retrieves the value of a field from a report based on the field name.

    Args:
        report (list[dict]): A list of dictionaries representing the json fields.
        name (str): The name (or varid) of the field to retrieve.
        human_readable (bool): If True and the field is in BPS_FIELD, the value is divided by 1000.

    Returns:
        int, str or float: The field value, either as an integer or a string depending on the field type.
        None: If the field is not found or has no value.
    """

    field = next((item for item in report if item.get("varid") == name), None)

    if not field:
        return None

    if name in BPS_FIELD:
        value = int(field["varvalue"])
        if human_readable:
            return round(value / 1000000, 3)
        return value
    return field.get("varvalue")


def decrypt_response(hex_key: str, encrypted_data_hex: str) -> str:
    """
    Decrypts the given encrypted data using AES-CCM mode.

    Args:
        encrypted_data_hex (str): Hexadecimal string of the encrypted data (ciphertext + tag).

    Returns:
        str: Decrypted data as a UTF-8 string.

    Raises:
        ValueError: If decryption fails due to wrong key or tampered data.
    """

    try:
        hex_key = settings.hex_key
        key = bytes.fromhex(hex_key)
        nonce = key[:8]

        ciphertext_and_tag = bytes.fromhex(encrypted_data_hex)
        ciphertext = ciphertext_and_tag[:-16]
        tag = ciphertext_and_tag[-16:]
        cipher = AES.new(key, AES.MODE_CCM, nonce=nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode("utf-8")

    except ValueError as e:
        raise ValueError(
            "Decryption failed. Possible wrong key or tampered data."
        ) from e


async def get_encrypted_json(path: str, params: dict[str] = None):
    """
    Makes an asynchronous GET request, decrypts the response if necessary, and parses the JSON.

    Args:
        params (dict): Optional query parameters to include in the request.

    Returns:
        tuple: (response, error_message) where response is the parsed JSON (or decrypted data), and
               error_message is any error encountered during the process.
    """
    if params is None:
        params = {}

    res = None
    error_msg = None
    headers = {"Accept": "application/json"}
    cache_transport = hishel.AsyncCacheTransport(transport=httpx.AsyncHTTPTransport())
    cache_controller = hishel.Controller(
        cacheable_methods=["GET"],
        cacheable_status_codes=[200],
        allow_stale=True,
        always_revalidate=True,
    )

    async with hishel.AsyncCacheClient(
        controller=cache_controller,
        transport=cache_transport,
        timeout=settings.http_timeout,
    ) as client:
        for attempt in range(settings.http_max_retries + 1):
            try:
                response = await client.get(
                    f"{settings.speedport_host}{path}", params=params, headers=headers
                )
                response.raise_for_status()

                try:
                    res = response.json()
                    break
                except ValueError:
                    try:
                        decrypted = decrypt_response(settings.hex_key, response.text)
                        res = orjson.loads(decrypted)
                        break
                    except (ValueError, orjson.JSONDecodeError) as e:
                        error_msg = f"Decryption or JSON parsing failed: {e}"
                        logger.error(error_msg)
                        continue

            except httpx.HTTPStatusError as e:
                error_msg = (
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
                logger.error(error_msg)

            except httpx.RequestError as e:
                error_msg = f"Request error occurred: {e}"
                logger.error(error_msg)

            if attempt < settings.http_max_retries:
                logger.info(
                    f"Retry {attempt + 1}/{settings.http_max_retries} in {settings.http_retry_wait} seconds..."
                )
                await asyncio.sleep(settings.http_retry_wait)
            else:
                logger.error("Maximum number of retries exceeded, giving up")
                break

    return res, error_msg
