import xml.etree.ElementTree as ET
from pathlib import Path


def modify_xml_annotations(data_dir: Path):
    xml_files = list(data_dir.glob("annotations*.xml"))
    xml_files = [f for f in xml_files if not f.stem.endswith("_modified")]

    if not xml_files:
        print(f"Исходные XML-файлы не найдены в: {data_dir.resolve()}")
        return

    for xml_path in xml_files:
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            images = root.findall("image")
            if not images:
                print(f"В файле {xml_path.name} нет элементов <image>")
                continue

            original_ids = [img.get("id") for img in images]
            reversed_ids = original_ids[::-1]

            for index, img in enumerate(images):
                if reversed_ids[index] is not None:
                    img.set("id", reversed_ids[index])

                old_name = img.get("name")
                if old_name:
                    pure_name = Path(old_name).stem  # Получаем только имя без пути и расширения
                    img.set("name", f"{pure_name}.png")

            output_path = xml_path.parent / f"{xml_path.stem}_modified.xml"

            tree.write(output_path, encoding="utf-8", xml_declaration=True)
            print(f"Успешно изменен и сохранен: {output_path.name}")

        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Ошибка при обработке файла {xml_path.name}: {e}")
            continue


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    modify_xml_annotations(current_dir)
