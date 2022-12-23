#!/usr/bin/env python3

"""
© 2022 ROMAIN DUDEK

A very simple batch audio converter using python
"""

import sys
import os
from os import path, listdir
from colorPrint import cprint
from pydub import AudioSegment

HELP = """
    §_#I### Conversion de fichiers audio d'un répertoire ###§
    
    §-#Wmain.py§ §-#I[source, -h] encodage§

      §-#I-h, --help§    show this help
      §-#Isource§        source directory
      §-#Iencodage§      file type to convert to (mp3 by default)
    """

class AudioBatch:

    AUDIO_EXT = ["mp3", "wav", "aac"]

    def __init__(self, source_dir: str, codage: str):
        self.source_dir = source_dir
        self.codage = codage
        self.file_list = self.__list_audio_files_in_dir()

    def __list_audio_files_in_dir(self):
        cprint(path.join(f"§_#IListing audio files§ in {self.source_dir}, please wait..."))
        rawList = listdir(self.source_dir)
        rawList = [path.join(self.source_dir, filename) for filename in rawList if self.__is_it_audio(filename)]
        rawList.sort()
        return  [ file for file in rawList ]
    
    def __is_it_audio(self, filename: str):
        for ext in self.AUDIO_EXT:
            if filename.endswith(ext):
                return True
        return False
    
    def convert_files(self):
        for audio_file in self.file_list:
            audio_file_name, old_format = audio_file.split(".")
            target = audio_file.replace(old_format, self.codage)
            if old_format != self.codage and not path.exists(target):
                convert = AudioSegment.from_file(audio_file)
                convert.export(target, format=self.codage)
                cprint(f"§_#SFichier {audio_file}§ converti au format '§_#S{self.codage}§'")
            elif path.exists(target):
                cprint(f"§_#ILe fichier cible§ {target} existe déjà...")
            else:
                cprint(f"§_#WLe fichier§ {audio_file} est déjà au format '§_I{self.codage}§'")


if __name__ == '__main__':
    args = sys.argv[1:]
    source = target = codage = False

    if len(args) > 0:
        source = args[0]
    if len(args) > 1:
        codage = args[1]
    if len(args) == 0 or len(args) > 2:
        cprint(HELP)

    if source in ["--help", "-h"]:
        cprint(HELP)
        exit()
    # check if directory is a directory
    if not path.exists(source):
        raise ValueError(f"Source directory must exists\n{HELP}")
    
    if not codage:
        codage = 'mp3'

    batch = AudioBatch(source, codage)
    batch.convert_files()
    

    

