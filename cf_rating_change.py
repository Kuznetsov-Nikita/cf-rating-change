# Основная программа
import get_rating_change
import get_user_info
import flask
import views

from __init__ import app


# Маршрут приложения
@app.route('/', methods=["GET", "POST"])
def index():
	# форма на сайте
	form = views.DataForm()

	user_info = ""
	if form.validate_on_submit():
		try:
			rating_change = get_rating_change.get_result(form.username.data, form.start_date.data, form.end_date.data) # изменение рейтинга
			user_info = get_user_info.get_result(form.username.data) # информация о пользователе - картинка

			if rating_change > 0:
				result = "Рейтинг вырос на " + str(rating_change)
			elif rating_change == 0:
				result = "Рейтинг не изменился"
			else:
				result = "Рейтинг упал на " + str(-rating_change)
		except ValueError:
			result = "Ошибка codeforces при запросе"
		except:
			result = "Упс... что-то сломалось("
	else:
		result = "Запрос не отправлен, неверный формат входных данных"

	return flask.render_template("index.html", form=form, handle=form.username.data, image=user_info, result=result)

# Маршрут подгрузки css
@app.route('/mycss.css', methods=["GET"])
def get_css():
	return flask.render_template("mycss.css")


if __name__ == "__main__":
	app.run()
