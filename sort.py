import re
import shutil
import os
from glob import glob, iglob


class Episode:
    def __init__(self):
        self.series_name = ''
        self.season = ''
        self.episode = ''
        self.quality = ''
        self.extension = ''

    def make_fullname(self):
        #make parameters to standard format
        if len(self.season) == 1:
            self.season = "0" + self.season
        if len(self.episode) == 1:
            self.episode = "0" + self.episode
        if self.extension.startswith('.'):
            self.extension = self.extension[1:]
        #symbols
        s = "S" + self.season
        e = "E" + self.episode
        ext = self.extension
        #
        self.fullname = ".".join((self.series_name, s, e, self.quality, ext))
        return self.fullname

    def __str__(self):
        self.make_fullname()
        return self.fullname

def main():
    #get rename as input
    rename = input('Do you want to rename files when moving (y|n) ? ').lower()
    if rename.startswith('n'):
        rename = False
    elif rename.startswith('y'):
        rename = input("Enter the new name to rename files (just the name without season, episode, etc) : ")
    else :
        print("Invalid input !")
        return main()
    #find videos with file extension
    suffs = ('mkv', 'mp4', 'srt',)
    is_movie = lambda x:  any((filename.endswith(suff) for suff in suffs))
    pattern = re.compile(r"(?P<name>.+?)[^a-z]?s\D?(?P<s>\d+).?e(?P<e>\d+).?(?P<q>.*)\.(?P<ext>.+)", re.I)
    count = {'s':0, 'e':0}

    for filename in iglob('*.*'):
        #skip another files
        if not is_movie(filename):
            continue
        #check episode and season info in filename
        info = pattern.search(filename)
        if not info :
            continue
        #episode object
        episode = Episode()
        episode.series_name, episode.season, episode.episode = info.group('name'), info.group('s'), info.group('e')
        episode.quality, episode.extension = info.group('q'), info.group('ext')
        #change filename by user select
        if rename:
            episode.series_name = rename
        #new filename with standard format
        new_filename = episode.make_fullname()
        #make season folder
        try:
            os.mkdir(episode.season)
            count['s'] += 1
        except:
            pass
        #move file
        shutil.move(filename, os.path.join(episode.season, new_filename))
        count['e'] += 1
    print(f"{count['e']} episodes moved to {count['s']} seasons folders")


if __name__ == "__main__":
    main()
    input('Press Any key to quit !')
