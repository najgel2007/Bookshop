from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DecimalField, FileField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange


class BookForm(FlaskForm):
    name = StringField(
        'Наименование книги',
        render_kw={'placeholder': 'Мастер и Маргарита'},
        validators=[
            InputRequired(),
            Length(min=1, max=64, message='В названии должно быть менее 64 символов')
        ]
    )
    author = StringField(
        'Автор',
        validators=[InputRequired()],
        description='в формате Фамилия И.О. (например, Булгаков. М.А.)',
        render_kw={'placeholder': 'Булгаков М.А.'}
    )
    genre = SelectField(
        'Жанр',
        choices=[
            ('Роман', 'Роман'),
            ('Поэзия', 'Поэзия'),
            ('Драма', 'Драма')
        ]
    )
    price = DecimalField(
        'Цена экземпляра',
        render_kw={'placeholder': '17.49'},
        validators=[
            InputRequired(),
            NumberRange(min=0.01, message='Цена должна быть положительным числом')
        ]
    )
    amount = IntegerField(
        'Наличие экземпляров',
        default=0,
        render_kw={'placeholder': '5'},
        validators=[
            InputRequired(),
            NumberRange(min=0, message='Наличие экземпляров должно быть положительным числом')
        ]
    )
    image = FileField(
        'Изображение обложки',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только jpg и png!')]
    )
    description = TextAreaField(
        'Описание книги',
        render_kw={
            'placeholder': '«Ма́стер и Маргари́та» — роман Михаила Афанасьевича Булгакова, работа над которым началась в конце 1920-х годов и продолжалась вплоть до смерти писателя. Роман относится к незавершённым произведениям; редактирование и сведение воедино черновых записей осуществляла после смерти мужа вдова писателя — Елена Сергеевна.'}
    )
    submit = SubmitField('Ок')
