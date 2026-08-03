import xml.etree.ElementTree as ET
from pathlib import Path


def analyze_xml_annotations(data_dir: Path):
    """Сбор статистики распределения классов по XML-файлам аннотаций"""
    total_images = 0
    labeled_images_count = 0
    unlabeled_images_count = 0
    total_shapes = 0

    largest_img = None
    smallest_img = None

    xml_files = list(data_dir.glob("annotations*.xml"))
    if not xml_files:
        print(f"XML-файлы не найдены в директории: {data_dir.resolve()}")
        return

    target_shapes = {"box", "polygon", "points"}

    for xml_path in xml_files:
        try:
            # Читаем потоком через iterparse, чтобы не держать в памяти огромные XML
            context = ET.iterparse(xml_path, events=("start", "end"))
            context = iter(context)
            event, root = next(context)

            current_image_attr = None
            current_image_shapes_count = 0

            for event, elem in context:
                if event == "start" and elem.tag == "image":
                    current_image_attr = {
                        "name": elem.get("name"),
                        "width": int(elem.get("width", 0)),
                        "height": int(elem.get("height", 0)),
                    }
                    current_image_shapes_count = 0

                elif event == "end" and elem.tag in target_shapes:
                    current_image_shapes_count += 1
                    total_shapes += 1

                elif event == "end" and elem.tag == "image":
                    total_images += 1

                    if current_image_shapes_count > 0:
                        labeled_images_count += 1
                    else:
                        unlabeled_images_count += 1

                    area = current_image_attr["width"] * current_image_attr["height"]
                    current_image_attr["area"] = area

                    if largest_img is None or area > largest_img["area"]:
                        largest_img = current_image_attr

                    if smallest_img is None or area < smallest_img["area"]:
                        smallest_img = current_image_attr

                    # Очищаем обработанный элемент, предотвращая утечку памяти
                    elem.clear()

            root.clear()

        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Ошибка при обработке файла {xml_path.name}: {e}")
            continue

    print("Общая статистика по XML-аннотациям")
    print(f"1. Общее количество изображений: {total_images}")
    print(f"2. Количество размеченных изображений: {labeled_images_count}")
    print(f"3. Количество неразмеченных изображений: {unlabeled_images_count}")
    print(f"4. Количество всех фигур в сумме: {total_shapes}")
    print("5. Самое большое и маленькое изображения:")

    if largest_img:
        print(f"   - Наибольшее: {largest_img['name']} ({largest_img['width']}x{largest_img['height']})")
    if smallest_img:
        print(f"   - Наименьшее: {smallest_img['name']} ({smallest_img['width']}x{smallest_img['height']})")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    analyze_xml_annotations(current_dir)
