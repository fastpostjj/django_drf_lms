## Учебный проект SPA веб-приложение - LMS-система

### Реализованы модели урока и курса
Для них реализован CRUD. Для курса через ViewSets, а для урока через Generic-классы.

Для работы контроллеров реализованы сериализаторы.

Для модели курса в сериализатор  добавлено поле вывода количества уроков.
Эндпоинты курса и урока закрыты для неавторизованных пользователей.

Модераторы (staff) могут просматривать любые уроки или курсы, но без возможности их удалять и создавать новые. 
Пользователи, которые не входят в группу модераторов, могут видеть и редактировать только свои курсы и уроки.

### Реализованы модель платежа за урок или за курс

### Реализована модель пользователя с авторизацей по email

Для пользователя реализован вывод платежей этого пользователя


urls  для проверки функциональности:
http://localhost:8000/university/curs/
http://localhost:8000/university/lessons/
http://localhost:8000/user_auth/user/

фильтрация и сортировка:
сортировка  по  дате оплаты и по сумме
localhost:8000/university/payings/?ordering=-date_pay
localhost:8000/university/payings/?ordering=amount

фильтрация по курсу или уроку,
localhost:8000/university/payings/?paid_for_curs=1
localhost:8000/university/payings/?paid_for_lesson=2

фильтрация по способу оплаты.
localhost:8000/university/payings/?payment_method=cash
localhost:8000/university/payings/?payment_method=transfer