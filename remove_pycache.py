import os
import shutil

def remove_pycache(directory: str) -> None:
    """删除指定目录及子目录中的 __pycache__ 文件夹。"""

    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                full_path = os.path.join(root, dir_name)
                print(f"删除内容: {full_path}")
                shutil.rmtree(full_path)


# 使用当前工作目录
if __name__ == "__main__":
    start_path = os.getcwd()
    print(f"开始删除下面的 __pycache__ 目录 {start_path}")
    remove_pycache(start_path)
    print("已完成所有 __pycache__ 目录的删除.")
