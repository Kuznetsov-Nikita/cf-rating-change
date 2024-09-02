# Получение изменения рейтинга
import datetime
import json
import requests
import typing


def get_result(handle: str, start_date: datetime.date, end_date: datetime.date) -> int:
	# ответ на запрос, список изменений рейтинга
	rating = json.loads(requests.get("https://codeforces.com/api/user.rating?handle={}".format(handle)).text)
	
	# проверка статуса запроса
	if (rating["status"] != "OK"):
		raise ValueError

	if len(rating["result"]) == 0: # нет изменений рейтинга
		rating_change: int = 0
	else:
		start_rating_i: int = 0 # позиция рейтинга в начальное время
		while start_rating_i < len(rating["result"]) and datetime.date.fromtimestamp(rating["result"][start_rating_i]["ratingUpdateTimeSeconds"]) < start_date:
			start_rating_i += 1
		if start_rating_i != 0:
			start_rating_i -= 1

		end_rating_i: int = len(rating["result"]) - 1 # позиция рейтинга в конечное время
		while end_rating_i >= 0 and datetime.date.fromtimestamp(rating["result"][end_rating_i]["ratingUpdateTimeSeconds"]) >= end_date:
			end_rating_i -= 1
		if end_rating_i != len(rating["result"]) - 1:
			end_rating_i += 1

		# находим изменение рейтинга
		if start_rating_i == 0 and start_date < datetime.date.fromtimestamp(rating["result"][start_rating_i]["ratingUpdateTimeSeconds"]): # начальная дата меньше первого изменения рейтинга
			if end_rating_i == len(rating["result"]) - 1 and end_date >= datetime.date.fromtimestamp(rating["result"][end_rating_i]["ratingUpdateTimeSeconds"]):
				rating_change: int = rating["result"][end_rating_i]["newRating"] # конечная дата позже последнего изменения рейтинга
			else:
				rating_change: int = rating["result"][end_rating_i]["oldRating"] # конечная дата раньше последнего изменения рейтинга
		else: # начальная дата не меньше первого изменения рейтинга
			if end_rating_i == len(rating["result"]) - 1 and end_date >= datetime.date.fromtimestamp(rating["result"][end_rating_i]["ratingUpdateTimeSeconds"]):
				rating_change: int = rating["result"][end_rating_i]["newRating"] - rating["result"][start_rating_i]["newRating"] # конечная дата позже последнего изменения рейтинга
			else:
				rating_change: int = rating["result"][end_rating_i]["oldRating"] - rating["result"][start_rating_i]["newRating"] # конечная дата раньше последнего изменения рейтинга

	return rating_change
