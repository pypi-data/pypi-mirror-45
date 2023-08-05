import sys
import json
import os
import subprocess
from shutil import copyfile

import logging
from .logger import build_logger
# from logger import build_logger
logger = build_logger("flauncher", level=logging.INFO)


CRED = '\033[31m'
CBYELLOW = '\033[1;33m'
CBWHITE = '\033[1;37m'
CBPURPLE = '\033[1;35m'
CBBLUE = '\033[1;34m'
CNORMAL_WHITE = '\033[0m'

# COCCURRENCES = CBPURPLE
# CFILE_PATHS = CBBLUE
# CTEXT_FILES = CBWHITE


def check_help_request(arguments):
    if len(arguments) == 1 and (arguments[0] == "-h" or arguments[0] == "--help"):
        README_path = "/usr/lib/flauncher/README.md"

        f = open(README_path, 'r')
        print(CBBLUE + "\n\t#######      flauncher documentation      #######\n" + CBWHITE)

        for line in f:
            if line == "```sh\n" or line == "```\n" or line == "<pre>\n" or line == "</pre>\n":
                continue
            line = line.replace('```sh', '')
            line = line.replace('```', '')
            line = line.replace('<pre>', '')
            line = line.replace('</b>', '')
            line = line.replace('<b>', '')
            line = line.replace('<!-- -->', '')
            line = line.replace('<br/>', '')
            line = line.replace('```sh', '')
            line = line.replace('***', '')
            line = line.replace('**', '')
            line = line.replace('*', '')
            print(" " + line, end='')
        print(CNORMAL_WHITE)
        exit()


def run(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.readlines()


def init_fdata():

    file_data = {
        "audio": {"nb": 0, "file_paths": list()},
        "image": {"nb": 0, "file_paths": list()},
        "pdf": {"nb": 0, "file_paths": list()},
        "rar": {"nb": 0, "file_paths": list()},
        "tar": {"nb": 0, "file_paths": list()},
        "tar_gz": {"nb": 0, "file_paths": list()},
        "tar_xz": {"nb": 0, "file_paths": list()},
        "tar_bz2": {"nb": 0, "file_paths": list()},
        "text": {"nb": 0, "file_paths": list()},
        "tgz": {"nb": 0, "file_paths": list()},
        "zip": {"nb": 0, "file_paths": list()},
        "video": {"nb": 0, "file_paths": list()}
    }
    return file_data


def get_launchers():

    default_launchersconf_name = "default_launchers.json"
    perso_launchersconf_name = "launchers.json"
    HOME_PATH = os.environ['HOME']
    perso_launchersconf_path = HOME_PATH + "/.config/flauncher/" + perso_launchersconf_name

    if not os.path.exists(perso_launchersconf_path):
        default_launchersconf_path = "/usr/lib/flauncher/" + default_launchersconf_name
        logger.info("the personal launchers conf path %s doesn't exist\n\tcopying the default launchers conf from %s "
                    "to %s\n\t\tdon't forget to customize the launchers by editing "
                    "this file" % (perso_launchersconf_path, default_launchersconf_path, perso_launchersconf_path))
        copyfile(default_launchersconf_path, perso_launchersconf_path)

    with open(perso_launchersconf_path) as f:
        return json.load(f)


def get_abs_path(files):
    abs_file_paths = list()
    for file in files:
        # abs_file_paths.append(os.path.abspath(file))
        abs_file_paths.append(os.path.normpath((os.path.join(os.getcwd(), os.path.expanduser(file)))))
    return abs_file_paths


def check_path_issues(file_path):
    path_issue = True
    if not os.path.exists(file_path):
        logger.warning("the path %s doesn't exist" % file_path)
    elif os.path.isdir(file_path):
        logger.warning("the path %s is a directory, not a file" % file_path)
    else:
        path_issue = False
    return path_issue


def check_binary(file_path):
    is_binary = False
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    try:
        if is_binary_string(open(file_path, 'rb').read(1024)):
            is_binary = True
    except:
        pass
    return is_binary


def get_media_exts():
    audio_exts = json.load(open("/usr/lib/flauncher/audio_exts.json"))
    image_exts = json.load(open("/usr/lib/flauncher/image_exts.json"))
    video_exts = json.load(open("/usr/lib/flauncher/video_exts.json"))
    return audio_exts, image_exts, video_exts


def file_router_one_ext(f, file_path, ext, audio_exts, image_exts, video_exts):

    for audio_ext in audio_exts:
        if ext == audio_ext:
            f["audio"]["nb"] += 1
            f["audio"]["file_paths"].append(file_path)
            return

    for image_ext in image_exts:
        if ext == image_ext:
            f["image"]["nb"] += 1
            f["image"]["file_paths"].append(file_path)
            return

    for video_ext in video_exts:
        if ext == video_ext:
            f["video"]["nb"] += 1
            f["video"]["file_paths"].append(file_path)
            return

    if ext == "pdf":
        f["pdf"]["nb"] += 1
        f["pdf"]["file_paths"].append(file_path)

    elif ext == "rar":
        f["rar"]["nb"] += 1
        f["rar"]["file_paths"].append(file_path)

    elif ext == "tar":
        f["tar"]["nb"] += 1
        f["tar"]["file_paths"].append(file_path)

    elif ext == "tgz":
        f["tgz"]["nb"] += 1
        f["tgz"]["file_paths"].append(file_path)

    elif ext == "zip":
        f["zip"]["nb"] += 1
        f["zip"]["file_paths"].append(file_path)

    else:
        if not check_binary(file_path):
            f["text"]["nb"] += 1
            f["text"]["file_paths"].append(file_path)


def file_router_two_exts(f, file_path, ext):

    found = True
    if ext == "tar.gz":
        f["tar_gz"]["nb"] += 1
        f["tar_gz"]["file_paths"].append(file_path)

    elif ext == "tar.xz":
        f["tar_xz"]["nb"] += 1
        f["tar_xz"]["file_paths"].append(file_path)

    elif ext == "tar.bz2":
        f["tar_bz2"]["nb"] += 1
        f["tar_bz2"]["file_paths"].append(file_path)
    else:
        found = False
    return found


def generate_folder_from_archive(archive_path, file_type):

    base_path = os.path.dirname(archive_path)
    fname = os.path.basename(archive_path)

    if file_type in ("tar_gz", "tar_xz", "tar_bz2"):
        folder_name = '.'.join(fname.split('.')[:-2])
    else:
        folder_name = '.'.join(fname.split('.')[:-1])

    folder_path = base_path + "/" + folder_name
    if os.path.exists(folder_path):
        folder_path = find_folder_path_not_existing(base_path, folder_name, file_type)

    try:
        os.mkdir(folder_path)
    except OSError:
        logger.error("creation of the directory %s failed" % folder_path)
        folder_path = None

    return folder_path


def check_nb_files(input_files):
    if len(input_files) == 0:
        raise ValueError("need at least one file to open ...")


def print_cmd(cmd):
    print(CBWHITE + "\n\t%s\n" % cmd + CNORMAL_WHITE, end='')


def find_folder_path_not_existing(base_path, folder_name, file_type):
    folder_archive_path = base_path + "/" + folder_name + "_" + file_type
    ref_folder_archive_path = folder_archive_path
    if os.path.exists(folder_archive_path):
        folder_archive_path = ref_folder_archive_path + "_archive"
        if os.path.exists(folder_archive_path):
            for i in range(20):
                folder_archive_path = ref_folder_archive_path + "_" + str(i+1)
                if not os.path.exists(folder_archive_path):
                    break
            logger.warning("all the archive folder names are already existing\n\tplease remove "
                           "some archive folder in %s" % base_path)
    return folder_archive_path


def route_file_regarding_dots(file_path, nb_dot, f, fname, audio_exts, image_exts, video_exts):
    if nb_dot == 0:
        if not check_binary(file_path):
            f["text"]["nb"] += 1
            f["text"]["file_paths"].append(file_path)
    elif nb_dot == 1:
        ext = fname.split('.')[-1]
        file_router_one_ext(f, file_path, ext.lower(), audio_exts, image_exts, video_exts)
    else:
        ext = fname.split('.')[-2] + '.' + fname.split('.')[-1]
        found = file_router_two_exts(f, file_path, ext.lower())
        if not found:
            file_router_one_ext(f, file_path, ext.lower(), audio_exts, image_exts, video_exts)


def launch_cmds(f, file_type, launchers):
    if f[file_type]["nb"] > 0:
        if file_type in ("tar_gz", "tar_xz", "tar_bz2", "tgz", "zip"):
            for archive_path in f[file_type]["file_paths"]:
                folder_path = generate_folder_from_archive(archive_path, file_type)
                if not folder_path:
                    logger.warning("skipping the %s archive" % archive_path)
                    continue
                cmd_pattern = launchers[file_type]
                cmd = cmd_pattern.replace("FOLDER_PATH", folder_path)
                cmd = cmd.replace("ARCHIVE_PATH", archive_path)
                print_cmd(cmd)
                run(cmd)
                run("ls -lart " + folder_path)
        elif file_type in ("rar", "tar"):
            for archive_path in f[file_type]["file_paths"]:
                cmd_pattern = launchers[file_type]
                cmd = cmd_pattern.replace("ARCHIVE_PATH", archive_path)
                print_cmd(cmd)
                run(cmd)

        else:
            app_cmd = launchers[file_type]
            cmd = app_cmd + " \"" + '\" \"'.join(f[file_type]["file_paths"]) + "\""
            print_cmd(cmd)
            run(cmd)


def main():

    input_parms = sys.argv[1:]
    check_help_request(input_parms)
    check_nb_files(input_parms)

    launchers = get_launchers()
    file_paths = get_abs_path(input_parms)
    file_types = ["audio", "image", "pdf", "rar", "tar", "tar_gz", "tar_xz", "tar_bz2", "text", "tgz", "zip", "video"]

    audio_exts, image_exts, video_exts = get_media_exts()

    f = init_fdata()

    for file_path in file_paths:

        if check_path_issues(file_path):
            continue

        fname = os.path.basename(file_path)
        nb_dot = fname.count('.')
        route_file_regarding_dots(file_path, nb_dot, f, fname, audio_exts, image_exts, video_exts)

    for file_type in file_types:
        launch_cmds(f, file_type, launchers)


if __name__ == "__main__":
    main()
