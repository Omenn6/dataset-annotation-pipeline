import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def analyze_shape_stats(data_dir: Path):
    shape_counter = Counter()
    target_shapes = {"box", "polygon", "points"}

    xml_files = list(data_dir.glob("annotations*.xml"))
    if not xml_files:
        print(f"Файлы не найдены в: {data_dir.resolve()}")
        return

    for xml_path in xml_files:
        try:
            context = ET.iterparse(xml_path, events=("end",))
            for event, elem in context:
                if elem.tag in target_shapes:
                    shape_counter[elem.tag] += 1
                    elem.clear()
        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Ошибка обработки файла {xml_path.name}: {e}")
            continue

    print("Статистика по типам фигур")

    for shape_type in ["box", "polygon", "points"]:
        count = shape_counter.get(shape_type, 0)
        print(f"{shape_type}: {count}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    analyze_shape_stats(current_dir)
