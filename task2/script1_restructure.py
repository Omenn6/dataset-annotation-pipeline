import json
import shutil
from pathlib import Path


def restructure_coco_dataset(base_dir: Path):
    coco_dir = base_dir / "task_train_coco 1.0"

    # Рекурсивно ищем JSON-файл в подпапках разметки
    json_files = list(coco_dir.rglob("*.json"))
    if not json_files:
        print(f"Файл аннотаций JSON не найден в {coco_dir.resolve()}")
        return
    annotation_path = json_files[0]

    # Создаем новую чистую папку для результата в корне task2
    output_images_dir = base_dir / "images"
    output_images_dir.mkdir(parents=True, exist_ok=True)

    print(f"Чтение аннотаций из: {annotation_path.resolve()}")
    with open(annotation_path, "r", encoding="utf-8") as f:
        coco_data = json.load(f)

    categories = {cat["id"]: cat["name"] for cat in coco_data.get("categories", [])}

    image_to_classes = {}
    for ann in coco_data.get("annotations", []):
        img_id = ann["image_id"]
        cat_id = ann["category_id"]
        class_name = categories.get(cat_id)

        if class_name:
            if img_id not in image_to_classes:
                image_to_classes[img_id] = set()
            image_to_classes[img_id].add(class_name)

    # Рекурсивный поиск всех картинок внутри папки датасета
    available_files = {}
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG"}

    for path in coco_dir.rglob("*"):
        if path.is_file() and path.suffix in extensions:
            available_files[path.name.lower()] = path

    success_count = 0
    missing_count = 0

    for img_entry in coco_data.get("images", []):
        img_id = img_entry["id"]
        old_file_name = img_entry["file_name"]

        img_classes = image_to_classes.get(img_id)
        if img_classes:
            class_folder_name = "_".join(sorted(img_classes))
        else:
            class_folder_name = "unlabeled"

        pure_img_name = Path(old_file_name).name

        # Берем точный путь к физическому файлу на диске
        src_img_path = available_files.get(pure_img_name.lower())

        target_class_dir = output_images_dir / class_folder_name
        target_class_dir.mkdir(parents=True, exist_ok=True)
        dst_img_path = target_class_dir / pure_img_name

        if src_img_path and src_img_path.exists():
            shutil.copy(src_img_path, dst_img_path)
            success_count += 1
        else:
            missing_count += 1

        img_entry["file_name"] = f"images/{class_folder_name}/{pure_img_name}"

    updated_json_path = base_dir / "updated_annotations.json"
    with open(updated_json_path, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=4)

    print(f"Успешно скопировано файлов: {success_count}")
    if missing_count > 0:
        print(f"Не найдено картинок на диске: {missing_count}")
    print(f"Новый JSON сохранен в: {updated_json_path.name}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    restructure_coco_dataset(current_dir)
