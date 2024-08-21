import os
import subprocess
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import logging
from datetime import datetime
import ctypes

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для выбора папки проекта
def select_project_folder():
    folder_path = ctk.filedialog.askdirectory()
    return folder_path

# Функция для поиска виртуального окружения
def find_virtualenv(project_folder):
    env_folders = ['env', 'venv']
    for env_folder in env_folders:
        if os.path.exists(os.path.join(project_folder, env_folder)):
            return os.path.join(project_folder, env_folder)
    return None

# Функция для активации виртуального окружения
def activate_virtualenv(env_path):
    if os.name == 'nt':
        activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(env_path, 'bin', 'activate')
    try:
        subprocess.call(activate_script, shell=True)
    except Exception as e:
        logging.error(f"Ошибка активации виртуального окружения: {e}")

# Функция для создания или обновления файла requirements.txt
def create_requirements(manage_py_folder, env_path):
    requirements_path = os.path.join(manage_py_folder, 'requirements.txt')
    if os.name == 'nt':
        pip_path = os.path.join(env_path, 'Scripts', 'pip')
    else:
        pip_path = os.path.join(env_path, 'bin', 'pip')
    subprocess.call(f'{pip_path} freeze > {requirements_path}', shell=True)
    return requirements_path

# Функция для поиска папки, где находится manage.py
def find_manage_py_folder(project_folder):
    for root, dirs, files in os.walk(project_folder):
        if 'manage.py' in files:
            return root
    return None

# Функция для проверки наличия Django в requirements.txt
def check_django_in_requirements(requirements_path):
    if not os.path.exists(requirements_path) or os.path.getsize(requirements_path) == 0:
        return False
    with open(requirements_path, 'r') as requirements_file:
        for line in requirements_file:
            if 'Django' in line:
                return True
    return False

# Функция для получения названия проекта и приложений
def get_project_and_apps(manage_py_folder):
    project_name = None
    apps = []

    for root, dirs, files in os.walk(manage_py_folder):
        if 'settings.py' in files:
            settings_path = os.path.join(root, 'settings.py')
            logging.info(f"Найден файл settings.py: {settings_path}")
            with open(settings_path, 'r') as settings_file:
                settings_content = settings_file.read()
                
                # Извлечение названия проекта из ROOT_URLCONF
                root_urlconf_start = settings_content.find('ROOT_URLCONF')
                if root_urlconf_start != -1:
                    root_urlconf_end = settings_content.find('\n', root_urlconf_start)
                    root_urlconf_str = settings_content[root_urlconf_start:root_urlconf_end].strip().split('=')[1].strip().strip("'")
                    project_name = root_urlconf_str.split('.')[0]
                
                # Извлечение приложений из INSTALLED_APPS
                installed_apps_start = settings_content.find('INSTALLED_APPS')
                if installed_apps_start != -1:
                    installed_apps_end = settings_content.find(']', installed_apps_start)
                    installed_apps_str = settings_content[installed_apps_start:installed_apps_end + 1]
                    apps_lines = installed_apps_str.split('=')[1].strip().strip('[]').split(',')
                    for app_line in apps_lines:
                        app_name = app_line.strip().strip("'")
                        if app_name and not app_name.startswith('django.'):
                            apps.append(app_name)
            break

    logging.info(f"Извлечены приложения: {apps}")
    return project_name, apps

# Функция для генерации файла README.md
def generate_readme(manage_py_folder, requirements_path, project_name, apps, repo_name, description):
    readme_path = os.path.join(manage_py_folder, 'README.md')

    with open(readme_path, 'w', encoding='utf-8') as readme:
        if repo_name:
            readme.write(f'# {repo_name}\n\n')
            
        if not repo_name:
            if project_name:
                readme.write(f'# {project_name}\n\n')
                readme.write('## Приложения:\n')
                for app in apps:
                    readme.write(f'- {app}\n')
                readme.write('\n')
        
        if description:
            readme.write(f'## Описание\n{description}\n\n')
            
        elif not project_name:
            readme.write('# Универсальный шаблон\n\n')
     
        readme.write('## Структура папок и файлов\n\n')
        readme.write('```\n')
        for root, dirs, files in os.walk(manage_py_folder):
            if 'env' in dirs:
                dirs.remove('env')
            if 'venv' in dirs:
                dirs.remove('venv')
            if '.git' in dirs:
                dirs.remove('.git')
            if 'build' in dirs:
                dirs.remove('build')
            if 'dist' in dirs:
                dirs.remove('dist')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            if 'migrations' in dirs:
                dirs.remove('migrations')
            level = root.replace(manage_py_folder, '').count(os.sep)
            indent = ' ' * 4 * (level)
            readme.write(f'{indent}{os.path.basename(root)}/\n')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if f != '__init__.py':
                    readme.write(f'{subindent}{f}\n')
        readme.write('```\n\n')
        
        if os.path.exists(requirements_path) and os.path.getsize(requirements_path) > 0:
            readme.write('## Библиотеки\n\n')
            with open(requirements_path, 'r') as requirements:
                for line in requirements:
                    readme.write(f'- {line}')

# Основная функция для запуска программы
def main():
    root = ctk.CTk()
    root.withdraw()

    console_text = ctk.StringVar()

    def log_to_console(level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {level} - {message}\n"
        console_text.set(console_text.get() + log_message)
        logging.info(message)

    def on_select_folder():
        project_folder = select_project_folder()
        if not project_folder:
            CTkMessagebox(title="Информация", message="Папка проекта не выбрана.", icon="warning")
            log_to_console("INFO", "Папка проекта не выбрана.")
            return

        log_to_console("INFO", "Поиск виртуального окружения...")
        env_path = find_virtualenv(project_folder)
        if not env_path:
            CTkMessagebox(title="Информация", message="Виртуальное окружение не найдено.", icon="warning")
            log_to_console("INFO", "Виртуальное окружение не найдено.")
            return

        log_to_console("INFO", "Активация виртуального окружения...")
        activate_virtualenv(env_path)

        log_to_console("INFO", "Поиск папки с manage.py...")
        manage_py_folder = find_manage_py_folder(project_folder)
        if not manage_py_folder:
            CTkMessagebox(title="Информация", message="Файл manage.py не найден.", icon="warning")
            log_to_console("INFO", "Файл manage.py не найден.")
            manage_py_folder = project_folder

        log_to_console("INFO", "Создание файла requirements.txt...")
        requirements_path = create_requirements(manage_py_folder, env_path)

        log_to_console("INFO", "Проверка наличия Django в requirements.txt...")
        is_django_project = check_django_in_requirements(requirements_path)

        if is_django_project:
            log_to_console("INFO", "Получение названия проекта и приложений...")
            project_name, apps = get_project_and_apps(manage_py_folder)
            if not project_name:
                CTkMessagebox(title="Информация", message="Название проекта не найдено.", icon="warning")
                log_to_console("INFO", "Название проекта не найдено.")
                return
        else:
            project_name = None
            apps = []

        repo_name = repo_name_entry.get()
        description = description_entry.get()

        log_to_console("INFO", "Генерация файла README.md...")
        generate_readme(manage_py_folder, requirements_path, project_name, apps, repo_name, description)
        CTkMessagebox(title="Информация", message="README.md успешно сгенерирован.", icon="check")
        log_to_console("INFO", "README.md успешно сгенерирован.")

    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # Создаем окно с кнопкой для выбора папки
    window = ctk.CTkToplevel(root)
    window.title("Генератор README.md")
    window.geometry("480x600")
    center_window(window, 480, 600)

    repo_name_label = ctk.CTkLabel(window, text="Название репозитория:")
    repo_name_label.pack(pady=5)
    repo_name_entry = ctk.CTkEntry(window, width=400)
    repo_name_entry.pack(pady=5)

    description_label = ctk.CTkLabel(window, text="Описание:")
    description_label.pack(pady=5)
    description_entry = ctk.CTkEntry(window, width=400)
    description_entry.pack(pady=5)

    select_button = ctk.CTkButton(window, text="Выбрать папку проекта", command=on_select_folder)
    select_button.pack(pady=20)

    console_label = ctk.CTkLabel(window, text="Консоль:", text_color="green")
    console_label.pack(pady=5)

    console_frame = ctk.CTkFrame(window)
    console_frame.pack(pady=5, fill="both", expand=True)

    console = ctk.CTkTextbox(console_frame, width=580, height=200, wrap="word", state="disabled")
    console.pack(pady=5, padx=5, fill="both", expand=True)

    def update_console(*args):
        console.configure(state="normal")
        console.delete(1.0, "end")
        console.insert("end", console_text.get())
        console.configure(state="disabled")
        console.see("end")

    console_text.trace("w", update_console)

    window.mainloop()

if __name__ == "__main__":
    main()