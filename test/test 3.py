import os


def compare_folders(folder1, folder2):
    # Get the list of files in each folder
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # Find the common file names
    common_files = files1.intersection(files2)

    return list(common_files)


folder_one = "/path/to/folder/One"
folder_two = "/path/to/folder/Two"

same_files = compare_folders(folder_one, folder_two)
print(f"Files present in both folders: {same_files}")
print(f"Number of common files: {len(same_files)}")