Скрипт для генерации файлов с тестами на основе текстовых сценариев.

## Features
- Генерация шаблонных тестов на основе сценариев, описанных в .md формате;
- Поддержка кастомных шаблонов тестов;
- Генерация имен тестов при помощи ChatGPT;
- Обратная генерация .md файла на основе файлов тестов;
- Генерация интерфейса для тестов на основе Swagger документации;
- Генерация схем для тестов на основе Swagger документации;

## Getting Started

WD - текущая директория

### Step 1. Создать новый md-файл со сценариями

Генерация нового md-файла со сценариями в WD:

```bash
gena --md-example --md-format=md_table_format
```

### Step 2. Создать py-файлы по сценариям

Генерация py-файлов в WD без использования интерфейса по md-файлу со сценариями в WD:

```bash
gena --template-path=$(pwd)/templates/test_template.txt
```

### Step 3. Создать md-файл со сценариями по py-файлам

Cгенерировать md-файл в WD по уже имеющимся тестам в TARGET_DIR и сабдиректориях:

```bash
gena --reversed --target-dir TARGET_DIR
```

## Использование AI

Для генерации имен тестов можно использовать AI ChatGPT

Для того чтобы имена тестов были сгенерированы AI:
- запустить скрипт генерации py файлов с ключом `--ai`;
- в файле сценариев поле subject должно быть не заполнено;
- должны быть определены env переменные `OPENAI_API_KEY` & `OPENAI_URL`.

```bash
gena --template-path=$(pwd)/templates/test_template.txt --ai
```


## Форматы md-файлов

- В виде списка: `--md-format=md_list_format`
- В виде таблицы: `--md-format=md_table_format`

## Кастомные шаблоны для генерации тестов

Скрипт может использовать кастомные шаблоны для генерации тестов (см. `/templates`)

При описании сценариев в форматах md_list_format & md_table_format в шаблоне доступны следующие переменные:
- `{{ test_scenarios }}` - массив тестов.

Каждый объект `scenario` из массива `test_scenarios` имеет следующие поля:
 - `{{ scenario.priority }}` - приоритет теста;
 - `{{ scenario.subject }}` - имя теста;
 - `{{ scenario.description }}` - описание теста;
 - `{{ scenario.expected_result }}` - ожидаемый результат теста;
 - `{{ scenario.is_positive }}` - признак позитивности теста;
 - `{{ scenario.params }}` - массив `str` параметров теста.

При описании сценариев в .md файле можно объявить переменные (в формате `**var_name** = var_value`), которые могут быть использованы в шаблоне тестов, например:
```
**feature** = my_feature_value
```

Использование в шаблоне:
```
This test is from {{ suite_data['feature'] }} feature
```

## Генерация api интерфейса и схемы:

 - `tests` - для генерации тестов;
 - `interface` - для генерации интерфейса;
 - `schemas` - для генерации схем;

Для этого нужно указать флаг --generate, и указать нужные нам варианты генерации. Например мы хотим сгенерировать тесты и интерфейс.

```bash
gena --generate=tests,interface --scenarios-path=$(pwd) --template-path=$(pwd) --yaml-path=$(pwd) --interface-path=$(pwd)
```

А если нам нужно сгенерировать всё: тесты, интерфейс, схемы

```bash
gena --generate=tests,interface,schemas --scenarios-path=$(pwd) --template-path=$(pwd) --yaml-path=$(pwd) --interface-path=$(pwd) --schemas-path=$(pwd)
```

Также мы можем генерировать что-то по отдельности, просто укажите что вам нужно!

```bash
gena --generate=tests --scenarios-path=$(pwd) --template-path=$(pwd)
```
```bash
gena --generate=interface --scenarios-path=$(pwd) --yaml-path=$(pwd), --interface-path=$(pwd)
```
```bash
gena --generate=schemas --scenarios-path=$(pwd) --yaml-path=$(pwd) --schemas-path=$(pwd)
```


## Help

```bash
usage: gena [-h] [--scenarios-path SCENARIOS_PATH] [--template-path TEMPLATE_PATH] [--api-template-path API_TEMPLATE_PATH] [--target-dir TARGET_DIR] [--md-example] [--ai] [--md-format MD_FORMAT] [--force]
            [--reversed] [--generate GENERATE] [--yaml-path YAML_PATH] [--interface-path INTERFACE_PATH] [--schemas-path SCHEMAS_PATH]

Parse scenario file and generate scenario files from template.

options:
  -h, --help            show this help message and exit
  --scenarios-path SCENARIOS_PATH
                        Path to the scenario file. Defaults to scenarios.md in the current directory.
  --template-path TEMPLATE_PATH
                        Path to the test template file (used for tests generation).
  --api-template-path API_TEMPLATE_PATH
                        Path to the api template file (used for api generation).
  --target-dir TARGET_DIR
                        Directory to put or read generated test files. Defaults to the directory of scenarios-path.
  --md-example          Generate new md-file with scenarios.
  --ai                  Use AI to generate test file names and subjects for tests (if not exsists).
  --md-format MD_FORMAT
                        Name of the format to use. Available scenarios.md formats are: md_list_format, md_table_format
  --force               Force overwrite existing files.
  --reversed            Create scenarios file from test files.Tests should have same story and feature.
  --generate GENERATE   List of generate. Available components are: tests, interface, schemas. Example: tests,interface,schemas - generate all, tests - generate only tests. Delimiter - ","
  --yaml-path YAML_PATH
                        Path to the swagger yaml file. Used for interface generating.
  --interface-path INTERFACE_PATH
                        Path to the interface file. Used for interface generating.
  --schemas-path SCHEMAS_PATH
                        Path to directory containing schemas. User for schemas generating.
```
