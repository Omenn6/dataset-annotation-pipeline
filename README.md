# dataset-annotation-pipeline

Пайплайны обработки, анализа и конвертации датасетов для задач Computer Vision.

## Структура проекта

* `task1/` — Анализ и модификация XML-аннотаций (CVAT формат).
* `task2/` — Реструктуризация COCO датасета и конвертация разметки в формат YOLO.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск скриптов

### Задание 1 (XML)
```bash
python task1/script1_general_stats.py
python task1/script2_class_stats.py
python task1/script3_shape_stats.py
python task1/script4_modify_xml.py
```

### Задание 2 (COCO & YOLO)
```bash
python task2/script1_restructure.py
python task2/script2_validation.py
python task2/script3_yolo_convert.py
```
