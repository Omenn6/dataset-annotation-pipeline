import json
from pathlib import Path
import matplotlib.pyplot as plt


def validate_coco_dataset(base_dir: Path):
    updated_json_path = base_dir / "updated_annotations.json"

    if not updated_json_path.exists():
        print(f"Файл {updated_json_path.name} не найден. Сначала запусти первый скрипт!")
        return

    print(f"Загрузка обновленного JSON: {updated_json_path.name}...")
    with open(updated_json_path, "r", encoding="utf-8") as f:
        coco_data = json.load(f)

    class_distribution = {}
    valid_count = 0
    corrupted_count = 0

    for img_entry in coco_data.get("images", []):
        relative_path = img_entry["file_name"]
        full_path = base_dir / relative_path

        if full_path.exists() and full_path.is_file():
            valid_count += 1

            class_folder = Path(relative_path).parent.name
            class_distribution[class_folder] = class_distribution.get(class_folder, 0) + 1
        else:
            corrupted_count += 1
            print(f"Файл не найден на диске: {relative_path}")

    print("Отчет о валидации датасета")
    print(f"Всего проверено изображений по JSON: {len(coco_data.get('images', []))}")
    print(f"Успешно найдено на диске: {valid_count}")
    print(f"Ошибок (не найдено): {corrupted_count}")

    print("\nРаспределение изображений по папкам классов:")
    for folder_name, count in sorted(class_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {folder_name}: {count} шт.")

    if class_distribution:
        folders = list(class_distribution.keys())
        counts = list(class_distribution.values())

        plt.figure(figsize=(10, 6))
        plt.barh(folders, counts, color="skyblue", edgecolor="gray")
        plt.xlabel("Количество изображений")
        plt.ylabel("Папки классов / Комбинации")
        plt.title("Распределение изображений по классам в реструктурированном датасете")
        plt.tight_layout()

        graph_path = base_dir / "class_distribution.png"
        plt.savefig(graph_path, dpi=150)
        plt.close()
        print(f"График распределения сохранен как: {graph_path.name}")


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    validate_coco_dataset(current_dir)
