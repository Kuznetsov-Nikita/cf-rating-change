# Функции и элементы представления
from datetime import date
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


# Форма ввода данных
class DataForm(FlaskForm):
	username = StringField("Ник на Codeforces: ", validators=[DataRequired()]) # никнейм на codeforces
	start_date = DateField("Начальная дата:  ", default=date.today()) # начальная дата
	end_date = DateField("Конечная дата:   ", default=date.today()) # конечная дата

	# проверка на корректность запроса при посылке
	def validate_on_submit(self):
		result = super(DataForm, self).validate()

		if (self.start_date.data > self.end_date.data):
			return False
		else:
			return result
