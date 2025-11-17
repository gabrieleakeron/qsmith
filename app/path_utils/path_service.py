import os

def path_up_to(file_path, target_dir_name) -> str:
    dir_path = os.path.dirname(file_path)  # inizia dalla directory del file
    while True:
        head, tail = os.path.split(dir_path)
        if tail == target_dir_name:
            return dir_path
        if head == dir_path:  # siamo arrivati alla root
            raise ValueError(f"Directory '{target_dir_name}' non trovata nel path")
        dir_path = head


def get_app_path() -> str:
    return os.path.join(os.getcwd(), "app")


def get_project_root_path() -> str:
    return os.getcwd()
