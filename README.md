Скрипт для генерации файлов с тестами на фрейморвке vedro по тестовым сценариям

## Как использовать?

### Параметры скрипта

*   `--scenarios-path` - путь к файлу сценариев (по умолчанию равен scenarios.md в текущей рабочей директории);
*   `--template-path`\- путь к файлу шаблону для тестов;
*   `--target-dir` - путь к директории куда сохранить созданные тесты (по умолчанию равен file\_path);
*   `--ai` - использовать ChatGPT для генерации subject и имен файлов тестов (в переменных окружения должны быть определены переменные `OPENAI_API_KEY` & `OPENAI_URL`);
*   `--force` - пересоздать файлы тестов даже если они уже существуют в `target-dir` директории.
*   `--reversed` - сгенерировать md-файл со сценариями по уже имеющимся тестам.
*   `--md-example` - сгенерировать новый md-файл со сценариями.

### Формат md-файла

```plaintext
- В виде списка: `--md-format=md_list_format`
- В виде таблицы: `--md-format=md_table_format`
```

### Getting Started

#### Step 1. Создать новый md-файл со сценариями

Генерация нового md-файла со сценариями, оформленными в виде таблицы:

```python
python3 generate_scenarios.py --scenarios-path=$PROJECT_PATH/new_scenarios.md --md-format=md_table_format --md-example
```

где $PROJECT\_PATH - путь к проекту

Генерация нового md-файла со сценариями, оформленными в виде списка:

```python
python3 generate_scenarios.py --scenarios-path=$PROJECT_PATH/new_scenarios.md --md-format=md_list_format --md-example
```

#### Step 2. Создать py-файлы по сценариям

Генерация py-файлов без использования интерфейса по md-файлу со сценариями:

```python
python3 generate_scenarios.py --template-path=$PROJECT_PATH/templates/test_template.txt --scenarios-path=$PROJECT_PATH/new_scenarios.md --md-format=md_table_format --no-interface
```

Генерация py-файлов без использования интерфейса по md-файлу со сценариями:

```python
python3 generate_scenarios.py --template-path=$PROJECT_PATH/templates/test_template.txt --scenarios-path=$PROJECT_PATH/new_scenarios.md --md-format=md_table_format --no-interface`
```

#### Step 3. Создать md-файл со сценариями по py-файлам

Cгенерировать md-файл со сценариями по уже имеющимся тестам:

```python
python3 generate_scenarios.py --scenarios-path=$PROJECT_PATH/new_scenarios.md --target-dir=$PROJECT_PATH/PATH_TO_TESTS --md-format=md_table_format --reversed
```
