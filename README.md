### Телеграмм бот "Обмен валюты" (Конвертер валют ).

Рабочая версия https://t.me/RuChyExch_Bot запущена на хостинге.

#### Доступные команды:

/help - Данное описание

/convert - Конвертер валют

/default - Список валют по умолчанию

/list - Список доступных валют и их коды

/change - Изменить последние 4 валюты 
 ( Пример: /change AED BYR IRR KGS )


#### Три способа работы:

1. Нажимаете /convert, выходит цифровая клавиатура, вводите сумму для конвертации, нажимаете 'Enter'. 
   Выходит список валют, выбираете валюту в чём указали сумму, после выбираете валюту в которую надо конвертировать.

   Список валют состоит из 8-ми валют, четыре постоянные, четыре можно изменить под себя командой /change ....
   ( Пример: /change AED BYR IRR KGS ). 


2. После вывода результатов, можно выбрать одну из указанных значений для ее конвертации в другую валюту,
   чтобы повторно не вводить данные.


3. В строке ввода: "сумма" "в чем" "во что конвертировать". 
   
   > Примеры: 

   > 950 usd EUR

   > 1250.55 аргентин датск

Значения валют можно указывать в тикерах (RUB, USD, ..) не важно заглавными или нет. 

Второй способ по русскому (сокращенному) названию валют (аргентин - "Аргентинское песо", датск - "Датская крона").
Сокращения возможно любое, главное чтобы не двоякое, например при "ира" может быть "Иракский динар" или
 "Иранский риал".

Если введенные валюты не входят в состав списка валют, то они заменят две последние в ней.

#### Особенности:
1. Так как клавиатура Inline изменяемая, то пришлось сохранять настройки для каждого пользователя системы, 
  чтобы не перебивать свой список валют.
2. В качестве БД не стал брать, хотя бы SQLite, взял Redis в облаке (понимаю что не верное решение), но не думаю 
  что будет много пользователей (данных). Да и можно установить время жизни ключа.
3. Так как используется бесплатный API конвертора, то могут быть ограничения на количество запросов.
4. Указанный выше рабочий бот запущен на бесплатном тарифе хостинга "alwaysdata" как сервис(служба).
5. ~~В планах запустить через вебхуки и Aiohttp, так как использовал Aiogram, где-нибудь на хостинге.~~ 
Реализовано на вебхуке и на хостинге Alwaysdata.

