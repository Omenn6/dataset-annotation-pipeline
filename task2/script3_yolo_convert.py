import json
from pathlib import Path


def convert_coco_to_yolo(base_dir: Path):
    updated_json_path = base_dir / "updated_annotations.json"

    if not updated_json_path.exists():
        print(f"Файл {updated_json_path.name} не найден. Сначала запусти первый скрипт!")
        return

    print(f"Загрузка аннотаций для конвертации в YOLO...")
    with open(updated_json_path, "r", encoding="utf-8") as f:
        coco_data = json.load(f)

    categories = coco_data.get("categories", [])
    categories = sorted(categories, key=lambda x: x["id"])

    category_to_yolo_id = {cat["id"]: idx for idx, cat in enumerate(categories)}

    classes_txt_path = base_dir / "classes.txt"
    with open(classes_txt_path, "w", encoding="utf-8") as f:
        for cat in categories:
            f.write(f"{cat['name']}\n")

    images_meta = {}
    for img in coco_data.get("images", []):
        images_meta[img["id"]] = {
            "file_name": img["file_name"],
            "width": img["width"],
            "height": img["height"]
        }

    image_annotations = {}
    for ann in coco_data.get("annotations", []):
        img_id = ann["image_id"]
        if img_id not in image_annotations:
            image_annotations[img_id] = []
        image_annotations[img_id].append(ann)

    converted_count = 0

    for img_id, meta in images_meta.items():
        img_relative_path = meta["file_name"]
        img_width = meta["width"]
        img_height = meta["height"]

        img_full_path = base_dir / img_relative_path

        yolo_txt_path = img_full_path.with_suffix(".txt")

        yolo_lines = []
        annotations = image_annotations.get(img_id, [])

        for ann in annotations:
            cat_id = ann["category_id"]
            yolo_class_id = category_to_yolo_id.get(cat_id)

            if yolo_class_id is None:
                continue

            bbox = ann.get("bbox")
            if not bbox or len(bbox) != 4:
                continue

            x_min, y_min, w, h = bbox

            x_center = x_min + w / 2.0
            y_center = y_min + h / 2.0

            x_center_norm = x_center / img_width
            y_center_norm = y_center / img_height
            w_norm = w / img_width
            h_norm = h / img_height

            yolo_line = f"{yolo_class_id} {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}"
            yolo_lines.append(yolo_line)

        try:
            with open(yolo_txt_path, "w", encoding="utf-8") as f:
                if yolo_lines:
                    f.write("\n".join(yolo_lines) + "\n")
            converted_count += 1
        except FileNotFoundError:
            yolo_txt_path.parent.mkdir(parents=True, exist_ok=True)
            with open(yolo_txt_path, "w", encoding="utf-8") as f:
                if yolo_lines:
                    f.write("\n".join(yolo_lines) + "\n")
            converted_count += 1

    print("Конвертация в формат YOLO завершена")
    print(f"Обработано и создано YOLO-файлов (.txt): {converted_count}")
    print(f"Список классов сохранен в: {classes_txt_path.name}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    convert_coco_to_yolo(current_dir)
