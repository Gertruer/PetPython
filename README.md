# CandyGame

Это симуляция игры, в которой различные типы игроков соревнуются за конфеты, используя стратегии сотрудничества или обмана.

## Описание

В этой игре машина контролирует распределение конфет между двумя группами людей в зависимости от их действий. Игроки могут либо сотрудничать, либо обманывать, и получают очки в зависимости от своих действий и действий противника.

### Правила начисления очков:

- Если оба игрока сотрудничают: +2 очка каждому
- Если один игрок обманывает, а другой сотрудничает: +3 очка обманщику, -1 очко сотрудничающему
- Если оба игрока обманывают: 0 очков обоим

## Типы игроков

| Тип поведения | Действия игрока     |
|---------------|---------------------|
| Cheater       | Всегда обманывает   |
| Cooperator    | Всегда сотрудничает |
| Copycat       | Начинает с сотрудничества, затем повторяет ходы противника |
| Grudger       | Сотрудничает, пока противник не обманет хотя бы раз, после чего всегда обманывает |
| Detective     | Первые четыре раза идет с [Сотрудничать, Обманывать, Сотрудничать, Сотрудничать], и если за эти четыре хода другой парень обманывает хотя бы один раз — превращается в Подражателя. В противном случае сам переключается на Читера. |
| Copykitten    | Более мягкая версия Copycat. Он начинает с сотрудничества, затем в течение первых трех ходов может ответить обманом, если оппонент обманывает. Однако после третьего хода Copykitten становится исключительно сотрудничающим, независимо от действий оппонента. |



## Структура проекта

Проект состоит из следующих основных компонентов:

- Абстрактный базовый класс `Player`
- Пять подклассов `Player`, представляющих различные типы игроков
- Класс `Game` для управления игровым процессом

## Как запустить

Для запуска симуляции выполните основной скрипт Python. Он проведет серию игр между всеми возможными парами игроков и выведет топ-3 победителей.

## Результаты

После выполнения симуляции вы увидите результаты в виде списка трех лучших игроков с их итоговыми очками.

Пример вывода:
```
Топ 3 игрока:
Copycat: 77
Copykitten: 69
Cheater: 66
```

Обратите внимание, что результаты могут немного отличаться в зависимости от количества проведенных игр и случайных факторов в поведении некоторых игроков.

 _Идеей для создания послужила [оригинальная версия игры](https://ncase.me/trust/), по которой была сделана модель._
