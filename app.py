from flask import Flask, render_template
import requests
from googletrans import Translator

app = Flask(__name__)

translator = Translator()


@app.route('/')
def random_quote():
    try:
        # Запрашиваем случайную цитату из API, отключив проверку SSL
        response = requests.get('https://api.quotable.io/random', verify=False)
        if response.status_code == 200:
            data = response.json()
            quote = data.get('content')
            author = data.get('author')

            # Переводим цитату и автора на русский язык
            translated_quote = translator.translate(quote, src='en', dest='ru').text
            translated_author = translator.translate(author, src='en', dest='ru').text
        else:
            quote = "Не удалось получить цитату"
            translated_quote = ""
            translated_author = ""
    except requests.exceptions.RequestException:
        quote = "Произошла ошибка при запросе цитаты"
        translated_quote = ""
        translated_author = ""

    return render_template('quote.html', quote=quote, translated_quote=translated_quote, author=author,
                           translated_author=translated_author)


if __name__ == '__main__':
    app.run(debug=True)
