import os


def view_dir(root_dir=".", ignore_dirs=None, prefix="", file=None):
    if ignore_dirs is None:
        ignore_dirs = []

    items = sorted(os.listdir(root_dir))
    items = [
        item for item in items if not item.startswith(".")
    ]  # 隠しファイル/フォルダを無視

    for index, item in enumerate(items):
        path = os.path.join(root_dir, item)
        is_last = index == len(items) - 1

        if os.path.isdir(path):
            if item in ignore_dirs:
                print(f"{prefix}{'└── ' if is_last else '├── '}{item}/", file=file)
                print(f"{prefix}{'    ' if is_last else '│   '}└── ...", file=file)
            else:
                print(f"{prefix}{'└── ' if is_last else '├── '}{item}/", file=file)
                view_dir(
                    path, ignore_dirs, prefix + ("    " if is_last else "│   "), file
                )
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{item}", file=file)


def is_in_ignored_dir(file_path, ignore_dirs):
    parts = file_path.split(os.sep)
    return any(ignored_dir in parts for ignored_dir in ignore_dirs)


def get_python_files(directory, ignore_dirs):
    python_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [
            d for d in dirs if d not in ignore_dirs
        ]  # 無視するディレクトリをスキップ
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if not is_in_ignored_dir(file_path, ignore_dirs):
                    python_files.append(file_path)
    return python_files


def main(ignore_dirs, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        # ディレクトリ構造の出力
        print("ディレクトリ構造:", file=f)
        print("root/", file=f)
        view_dir(".", ignore_dirs, file=f)
        print("\n", file=f)

        # Pythonファイルの内容出力
        python_files = get_python_files(".", ignore_dirs)
        for py_file in python_files:
            relative_path = os.path.relpath(py_file, ".")
            print(f"{relative_path}の内容:", file=f)
            try:
                with open(py_file, "r", encoding="utf-8") as py_content:
                    content = py_content.read()
                    print(content, file=f)
            except Exception as e:
                print(
                    f"エラー: {py_file}の読み込み中にエラーが発生しました。{str(e)}",
                    file=f,
                )
            print("\n", file=f)

    print(f"ディレクトリ構造とPythonファイルの内容が{output_file}に出力されました。")


if __name__ == "__main__":
    ignore_dirs = [".limbus_db_env", "__pycache__"]  # 無視するフォルダのリスト
    output_file = "directory_structure_and_contents.txt"  # 出力ファイル名
    main(ignore_dirs, output_file)
