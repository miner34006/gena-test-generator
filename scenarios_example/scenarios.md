## Описание

**Feature** - UserFeature

**Story** - UserStory

**Api method** - POST /path/to/endpoint

## Сценарии

### Позитивные
- P0: do not descease progress for in_progress achieve: Вернуть меньшее число друзей чем есть сейчас для in_progress ачивки -> прогресс не уменьшается
    * in_progress
    * completed
    * new
- P0: do not descease progress for completed achieve: Вернуть меньшее число друзей чем есть сейчас для completed ачивки -> прогресс не уменьшается

### Негативные
- P2: try to get bonuses with invalid data: Получение бонуса с невалидным параметром data -> 400 ошибка
    * string
    * array
    * max int
    * negative int
