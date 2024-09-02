# Получить информацию о пользователе
import json
import requests
import typing


def get_result(handle: str):
	# ответ на запрос, информация о пользователе, нужна конкретно картинка
	user_info = json.loads(requests.get("https://codeforces.com/api/user.info?handles={}".format(handle)).text)

	# проверка статуса запроса
	if (user_info["status"] != "OK"):
		raise ValueError

	return user_info["result"][0]["titlePhoto"]	 
