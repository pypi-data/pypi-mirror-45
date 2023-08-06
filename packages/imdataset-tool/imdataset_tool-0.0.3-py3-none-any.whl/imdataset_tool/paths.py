#coding = utf-8
import os

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")

def list_images(root_dir, type="rela"):
    """
    :param root_dir: 搜索的目录地址，将查找包含所有子目录中的所有文件
    :param type: 指定文件路径格式，如果希望得到以root_dir为基础的相对路径，默认或给type参数"rela",如果希望得到完整路径type参数"full"
    """
    imagesList = []
    _list_images(root_dir, imagesList)

    if type=="full":
        imagesList = _add_prefix(imagesList, root_dir)
    return imagesList


def _list_dirs(root_dir):
    dirsList = []
    subdirs = os.listdir(root_dir)
    for d in subdirs:
        if os.path.isdir(os.path.join(root_dir, d)):
            dirsList.append(d)
    return dirsList


def _list_files(root_dir, sub_dir, validExts=image_types):
    filesList = []
    full_dir = root_dir if sub_dir == "" else os.path.join(root_dir, sub_dir)
    files = os.listdir(full_dir)
    for filename in files:

        # determine the file extension of the current file
        ext = filename[filename.rfind("."):].lower()

        # check to see if the file is an image and should be processed
        if validExts is None or ext.endswith(validExts):
            if os.path.isfile(os.path.join(full_dir, filename)):
                filesList.append(os.path.join(sub_dir, filename))
    return filesList

def _add_prefix(files_list, prefix):# prefix is root_dir, add to subdir as fulldir
    filesPath = files_list.copy()
    for idx, file_dir in enumerate(filesPath):
        filesPath[idx]= os.path.join(prefix, file_dir) # file_dir是copy的副本，修该file_dir不改变file_lists值，必须修改file_list[idx]
    return filesPath
    # 会修改file_list值，因此如果指向要file_list的值，要copy副本，这里copy了副本FilesPath,注意要使用b = a.copy()而不是b = a

def _list_images(root_dir, imagesList, sub_dir_from_root = ""):
    # for rootDir, subDirs, files in os.walk(dir, topdown=False):
    #     print(rootDir, subDirs, files)
    # get all foldernames in root_dir
    full_dir = root_dir if sub_dir_from_root=="" else os.path.join(root_dir, sub_dir_from_root)
    folder_names = _list_dirs(full_dir)
    file_names = _list_files(root_dir, sub_dir_from_root)

    if len(file_names)>0:
        imagesList += file_names
    for d in folder_names:
        new_subdir = d if sub_dir_from_root=="" else os.path.join(sub_dir_from_root, d)
        _list_images(root_dir, imagesList, new_subdir)
    return imagesList

