import json
import os
import uuid
import requests
from aiogram import Bot
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth
load_dotenv(find_dotenv())

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')


def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),  # уникальный идентификатор запроса
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(CLIENT_ID, SECRET),
            data=payload,
            verify=False,  # Убедитесь, что использование verify=False безопасно для вашей среды
        )
        res.raise_for_status()  # проверка на наличие ошибок
        access_token = res.json().get("access_token")
        if not access_token:
            raise ValueError("Токен доступа не был получен.")
        return access_token
    except requests.RequestException as e:
        print("Ошибка при получении access token:", e)
        return None


def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()  # проверка на наличие ошибок
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print("Ошибка при отправке запроса к GigaChat API:", e)
        return "Ошибка при получении ответа от GigaChat."


def sent_prompt_and_get_response(msg: str, language: str):
    access_token = get_access_token()

    # Создаем сообщение в зависимости от языка
    if language == "ru":
        message = f'Сочини для меня одну интересную сказку про {msg}'
    elif language == "en":
        message = f'Write an interesting story about {msg} for me'
    else:
        message = f'Сочини для меня одну интересную сказку про {msg}'

    # Проверка наличия access token
    if access_token:
        return send_prompt(message, access_token)
    else:
        return "Не удалось получить access token."