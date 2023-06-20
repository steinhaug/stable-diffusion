# -*- coding: utf-8 -*-
"""
Dir manipulation - misc tools for editing directories
Author: steinhaug at gmail dot com
"""
import os

def remove_matching_dirs(root_directory, dir_match):
    for root, dirs, files in os.walk(root_directory):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            if directory.lower().endswith(dir_match):
                try:
                    # Remove the directory and its contents
                    for sub_root, sub_dirs, sub_files in os.walk(directory_path, topdown=False):
                        for file in sub_files:
                            file_path = os.path.join(sub_root, file)
                            os.remove(file_path)
                        for sub_dir in sub_dirs:
                            sub_dir_path = os.path.join(sub_root, sub_dir)
                            os.rmdir(sub_dir_path)
                    
                    # Remove the directory
                    os.rmdir(directory_path)
                    print(f"Directory '{directory_path}' and its contents have been deleted.")
                
                except OSError as e:
                    print(f"Error deleting directory '{directory_path}': {e}")
    return ''


def recursively_remove_directory(directory_path):
    """
    Recursively deletes a directory and its contents.
    
    Args:
        directory_path (str): The path to the directory to be deleted.
    """
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return
    
    try:
        # Remove all files and subdirectories
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)

        # Remove the top-level directory
        os.rmdir(directory_path)
        print(f"Directory '{directory_path}' and its contents have been deleted.")
    
    except OSError as e:
        print(f"Error deleting directory '{directory_path}': {e}")

