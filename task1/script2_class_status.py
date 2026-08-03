import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def analyze_class_stats(data_dir: Path):
    class_counter = Counter()
    target_shapes = {"box", "polygon", "points"}

    xml_files = list(data_dir.glob("annotations*.xml"))
    if not xml_files:
        print(f"Файлы не найдены в: {data_dir.resolve()}")
        return

    for xml_path in xml_files:
        try:
            # Читаем файлы потоком, чтобы не перегружать память
            context = ET.iterparse(xml_path, events=("end",))
            for event, elem in context:
                if elem.tag in target_shapes:
                    label = elem.get("label")
                    if label:
                        class_counter[label] += 1

                    # Освобождаем память от элемента
                    elem.clear()
        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Ошибка обработки файла {xml_path.name}: {e}")
            continue

    print("Статистика по классам аннотаций")

    if not class_counter:
        print("Фигуры с классами не найдены")
    else:
        # Выводим по убыванию частоты
        for label, count in class_counter.most_common():
            print(f"{label}: {count}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    analyze_class_stats(current_dir)
