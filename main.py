import datetime as dt

# Основные претензии ниже сводятся к отсутствию единого оформлению кода и некоторым трудно читаемым конструкциям
# Так же советую обратить внимание на PEP-484: https://peps.python.org/pep-0484/ 
# Использование аннотаций поможет сделать код более читаемым и явным
# конструкция dt.datetime.now().date() используется несколько раз по ходу программы. Ее можно вынести в глобальную переменную.


class Record:
    def __init__(self, amount, comment, date=''):  # для избежания использования троичного оператора в качестве аттриуба date можно использовать date=now()
        self.amount = amount
        """
        Если сильно хочется использовать данную конструкцию, то лучше сделать обратный if.
        Ex: 
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date() if date else dt.datetime.now().date()
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # неявный метод. Не очень то понятно что из себя представляет аргумент record
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:  # зарезервированное наименование классом Record. Тем более, что с заглавной буквы именуются именно классы
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount  # соблюдайте единый стиль написания и используй оператор "+=", как в методе get_week_stats
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            """
            Данное условие можно успростить: 
                if 7 > (today - record.date).days >= 0 
            """
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()  # неявное именование переменной 
        if x > 0:
            # для многострочных операторов лучше использовать круглые скобки вместо "\" 
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # если убрать else, то логика программы не нарушится
        else:
            return('Хватит есть!')  # а вот тут круглые скобки не нужны 


class CashCalculator(Calculator):
    # комментарии к переменным тут излишни, так как их назначение ясно из названия
    # операции для перевода int к float также излишни
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # при именовании аргументов лучше использовать строчные буквы. В данном случае их передача не обязательна, так как они уже определены внутри класса
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):  
        currency_type = currency  # данное переопределение не будет иметь какого либо влияния на ход программы
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00  # данная строчка не имеет смысла, так как тут происходит сравнение переменной со значением. Скорее всего имелось ввиду использование "="
            currency_type = 'руб'
        # предпочтительнее использовать конструкцию if-elif-else так как первые два условия покрывают все, кроме отрицательных значений cash_remained
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)  # лучше соблюдать единый стиль офромления f-строк и также использовать скобки вместо \ для многострочных операторов

    # данный метод формально переопределяет метод родительского класса, но по факту работает точно так же. Поэтому лучше вызывать его напрямую если он необходим.                
    def get_week_stats(self):
        super().get_week_stats()
