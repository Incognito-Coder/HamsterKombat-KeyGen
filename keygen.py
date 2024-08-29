import time
import random
import uuid
import aiohttp
import asyncio
import sys
import os
import requests
from loguru import logger
os.system('title HamsterKombat Games Code Generator')

logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"" | <level>{level: <8}</level>"" | <cyan><b>{line}</b></cyan>"" - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

games = requests.request(method='GET', url='https://mr-alireza.ir/API/hamster.json').json()


def generate_client_id():
    current_time = int(time.time() * 1000)
    random_part = random.randint(100, 999)
    random_first = int(str(current_time)[:10] + str(random_part))
    return f"{random_first}-6873914666961597855"


def generate_event_id():
    return str(uuid.uuid4())


async def get_promo_code(app_token: str, promo_id: str, file: str, event_timeout: int, max_attempts: int = 30):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.gamepromo.io"
    }

    async with aiohttp.ClientSession(headers=headers) as http_client:
        client_id = generate_client_id()
        json_data = {
            "appToken": app_token,
            "clientId": client_id,
            "clientOrigin": "deviceid"
        }
        response = await http_client.post(url="https://api.gamepromo.io/promo/login-client", json=json_data)
        response_json = await response.json()
        access_token = response_json.get("clientToken")
        http_client.headers["Authorization"] = f"Bearer {access_token}"
        await asyncio.sleep(delay=1)
        attempts = 0
        while attempts < max_attempts:
            try:
                event_id = generate_event_id()
                json_data = {
                    "promoId": promo_id,
                    "eventId": event_id,
                    "eventOrigin": "undefined"
                }
                response = await http_client.post(url="https://api.gamepromo.io/promo/register-event", json=json_data)
                response.raise_for_status()
                response_json = await response.json()
                has_code = response_json.get("hasCode", False)
                if has_code:
                    json_data = {
                        "promoId": promo_id
                    }
                    response = await http_client.post(url="https://api.gamepromo.io/promo/create-code", json=json_data)
                    response.raise_for_status()
                    response_json = await response.json()
                    promo_code = response_json.get("promoCode")
                    if promo_code:
                        logger.success(f"Promo code is found: {promo_code}")
                        open(f'{file}.txt', 'a').write(promo_code + "\n")
                        return promo_code
            except Exception as error:
                logger.error(f"Error while getting promo code: {error}")
            attempts += 1
            logger.info(f"Attempt {attempts} was successful | Sleep {event_timeout}s before {attempts + 1} attempt to get promo code")
            await asyncio.sleep(delay=event_timeout)
    logger.warning(f"Promo code not found out of {max_attempts} attempts")
    input("Press enter to exit")
    exit(0)

if __name__ == '__main__':
    print(f'HamsterKombat Promo(Games) Key Generator - https://github.com/Incognito-Coder\n')
    print("Select a game:")
    for key, value in games.items():
        print(f"{key}: {value['name']}")
    print("0: Exit")
    game_choice = str(input("\nEnter the game number: "))
    if game_choice in games.keys():
        max_attemps = input("Max retry number,(Default is 30): ")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while True:
                if max_attemps:
                    loop.run_until_complete(get_promo_code(app_token=games[game_choice]['appToken'], promo_id=games[game_choice]['promoId'], file=games[game_choice]['short'], max_attempts=int(max_attemps), event_timeout=20))
                else:
                    loop.run_until_complete(get_promo_code(app_token=games[game_choice]['appToken'], promo_id=games[game_choice]['promoId'], file=games[game_choice]['short'], event_timeout=20))
        except KeyboardInterrupt:
            pass
