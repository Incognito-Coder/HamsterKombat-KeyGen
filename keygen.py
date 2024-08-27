import time
import random
import uuid
import aiohttp
import asyncio
import sys
import os
import random
from loguru import logger
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL='mysql+pymysql://root:123123@192.168.10.28/123123'
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session
write_to_database = False

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    content = Column(String(255))
    date_sent = Column(String(10), nullable=True)

Base.metadata.create_all(engine)


os.system('title HamsterKombat Games Code Generator')

logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"" | <level>{level: <8}</level>"" | <cyan><b>{line}</b></cyan>"" - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

games = {
    1: {
        'name': 'Riding Extreme 3D',
        'short': 'bike',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f'
    },
    2: {
        'name': 'Chain Cube 2048',
        'short': 'cube',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'
    },
    3: {
        'name': 'Train Miner',
        'short': 'train',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954'
    },
    4: {
        'name': 'Merge Away',
        'short': 'away',
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4'
    },
    5: {
        'name': 'Twerk Race 3D',
        'short': 'twerk',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c'
    },
    6: {
        'name': 'Polysphere',
        'short': 'poly',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71'
    },
    7: {
        'name': 'Mow and Trim',
        'short': 'trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6'
    },
    8: {
        'name': 'Mud Racing',
        'short': 'mud',
        'appToken': '8814a785-97fb-4177-9193-ca4180ff9da8',
        'promoId': '8814a785-97fb-4177-9193-ca4180ff9da8'
    }
}


def generate_client_id():
    current_time = int(time.time() * 1000)
    random_part = random.randint(100, 999)
    random_first = int(str(current_time)[:10] + str(random_part))
    return f"{random_first}-6873914666961597855"


def generate_event_id():
    return str(uuid.uuid4())

def insert_to_db(promo_code):
    with Session() as session:
        new_code = Record(user_id=None, content=promo_code, date_sent=None)
        session.add(new_code)
        session.commit()
        session.close()


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
                        if write_to_database:
                            insert_to_db(promo_code)
                        else:
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
    for key, value in games.items():
         game_choice = random.randint(1, key)
         choisen_game = games[game_choice]
    if game_choice in games:
        max_attemps = 30
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            while True:
                if max_attemps:
                    print(f"Генерируется токен для игры {choisen_game['name']}")
                    loop.run_until_complete(get_promo_code(app_token=games[game_choice]['appToken'], promo_id=games[game_choice]['promoId'], file=games[game_choice]['short'], max_attempts=int(max_attemps), event_timeout=20))
                    game_choice = random.randint(1, key)
                    choisen_game = games[game_choice]
                else:
                    loop.run_until_complete(get_promo_code(app_token=games[game_choice]['appToken'], promo_id=games[game_choice]['promoId'], file=games[game_choice]['short'], event_timeout=20))
        except KeyboardInterrupt:
            pass
