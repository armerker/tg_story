import json
import os
from config import USER_DATA_FILE


class UserManager:
    def __init__(self):
        self.user_data = self.load_user_data()

    def load_user_data(self):
        """Загружает данные пользователей из файла"""
        if os.path.exists(USER_DATA_FILE):
            try:
                with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}

    def save_user_data(self):
        """Сохраняет данные пользователей в файл"""
        try:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def get_user(self, user_id):
        """Возвращает данные пользователя или создает нового"""
        user_id_str = str(user_id)
        if user_id_str not in self.user_data:
            self.user_data[user_id_str] = {
                "user_name": "",
                "current_scene": "start",
                "inventory": [],
                "points": 0,
                "registered": False
            }
            self.save_user_data()
        return self.user_data[user_id_str]

    def reset_user(self, user_id):
        """Сбрасывает прогресс пользователя"""
        user_id_str = str(user_id)
        if user_id_str in self.user_data:
            self.user_data[user_id_str] = {
                "user_name": self.user_data[user_id_str]["user_name"],
                "current_scene": "start",
                "inventory": [],
                "points": 0,
                "registered": True
            }
            self.save_user_data()

    def update_user_scene(self, user_id, scene_id, scene_data):
        """Обновляет сцену пользователя и применяет изменения"""
        user = self.get_user(user_id)
        user["current_scene"] = scene_id


        if "inventory_add" in scene_data:
            user["inventory"].extend(scene_data["inventory_add"])
        if "inventory_remove" in scene_data:
            for item in scene_data["inventory_remove"]:
                if item in user["inventory"]:
                    user["inventory"].remove(item)
        if "points_change" in scene_data:
            user["points"] += scene_data["points_change"]

        self.save_user_data()

    def register_user(self, user_id, user_name):
        """Регистрирует нового пользователя"""
        user = self.get_user(user_id)
        user["user_name"] = user_name
        user["registered"] = True
        self.save_user_data()