**Story** - UserStory

**Feature** - UserFeature

## сценарии

### позитивные

- P0: do not descease progress for in_progress achieve: вернуть меньшее число друзей чем есть сейчас для in_progress ачивки -> прогресс не уменьшается
    * in_progress
    * completed
    * new
- P0: do not descease progress for completed achieve: вернуть меньшее число друзей чем есть сейчас для completed ачивки -> прогресс не уменьшается

### негативные

- P2: try to get bonuses with invalid data: получение бонуса с невалидным параметром data -> 400 ошибка
    * string
    * array
    * max int
    * negative int
