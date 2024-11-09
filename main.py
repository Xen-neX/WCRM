"""Модуль для выполнения HTTP-запросов и обработки JSON-данных."""

import json
import time
import requests

ATTEMPTS = 3

# делаем запрос
def response(url: str, headers: dict) -> requests.Response:
    """
    Выполняет GET-запрос к указанному URL.

    Args:
        url (str): URL для запроса
        headers (dict): Заголовки запроса

    Returns:
        requests.Response: Объект ответа
    """
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()  # Проверяем статус-код ответа
    return resp


# основная функция
def main(url: str, headers: dict) -> dict | str:
    """Получает и обрабатывает данные с указанного URL."""
    for attempt in range(ATTEMPTS):
        try:
            data = response(url, headers)
            try:
                return data.json()
            except json.JSONDecodeError as e:
                return f"Ошибка парсинга JSON: {e}"
        except requests.RequestException as e:
            if attempt < ATTEMPTS - 1:
                print(f"Попытка {attempt + 1} не удалась. Повторная попытка...")
                time.sleep(1)
            else:
                return f"Ошибка получения данных: {e}"
    return "Превышено максимальное количество попыток"


if __name__ == "__main__":
    result = main(
        "https://dev.whatc3rm.net/v3/tariffs?currency=RUB&crm=lk",
        {"X-Whatsapp-Token": "5d8af8faaeb61680883a850be0c577e2"},
    )
    print(json.dumps(result, indent=4, ensure_ascii=False))
