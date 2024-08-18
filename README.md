Скрипт для генерации файлов с тестами на фрейморвке vedro по тестовым сценариям

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
gena --template-path=$(pwd)/templates/test_template.txt --no-interface
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
gena --template-path=$(pwd)/templates/test_template.txt --no-interface --ai
```


## Форматы md-файлов

- В виде списка: `--md-format=md_list_format`
- В виде таблицы: `--md-format=md_table_format`

## Help

```bash
usage: generate_scenarios.py [-h] [--scenarios-path SCENARIOS_PATH] [--template-path TEMPLATE_PATH] [--target-dir TARGET_DIR] [--md-example] [--ai]
                             [--md-format MD_FORMAT] [--force] [--reversed] [--no-interface] [--interface-only] [--yaml-path YAML_PATH]
                             [--interface-path INTERFACE_PATH]

Parse scenario file and generate scenario files from template.

options:
  -h, --help            show this help message and exit
  --scenarios-path SCENARIOS_PATH
                        Path to the scenario file. Defaults to scenarios.md in the current directory.
  --template-path TEMPLATE_PATH
                        Path to the test template file (used for tests generation).
  --target-dir TARGET_DIR
                        Directory to put or read generated test files. Defaults to the directory of scenarios-path.
  --md-example          Generate new md-file with scenarios.
  --ai                  Use AI to generate test file names and subjects for tests (if not exsists).
  --md-format MD_FORMAT
                        Name of the format to use. Available scenarios.md formats are: md_list_format, md_table_format
  --force               Force overwrite existing files.
  --reversed            Create scenarios file from test files.Tests should have same story and feature.
  --no-interface        Generated without interface
  --interface-only      Generate interface only.
  --yaml-path YAML_PATH
                        Path to the swagger yaml file. Used for interface generating.
  --interface-path INTERFACE_PATH
                        Path to the interface file. Used for interface generating.
```