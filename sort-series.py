import os,re,shutil
from glob import glob


def main():
    quality = False
    format = input("Enter Files Format : ")#"mp4"
    format = format.replace(".","")
    rename = input("rename files (yes|no) : ")#False
    if rename.lower().startswith('y') :
        rename = True
    elif rename.lower().startswith('n') :
        rename = False
    else:
        return
    if rename:
        main_name = input("Enter name for set to files : ")
        main_name = main_name.replace(" ", ".")
        quality = input("Enter the quality of movies to set in the names : ")

    for i in glob(f"*.{format}"):
        m = re.search(r"(.*S\D?(\d+).*E\D?(\d+).*)\..*",i,re.I)
        if not m :
            continue
        s = m.group(2)
        e = m.group(3)
        if rename:
            t = f"{main_name}.S{s}.E{e}"
            if quality:
                t += "."+quality
            #name = re.sub(m.group(1),t,i,re.I)
            name = f"{t}.{format}"
        else:
            name = i
        if not os.path.exists(s):
            os.mkdir(s)
        shutil.move(i,f"{s}/{name}")
        print(name)


if __name__ == "__main__":
    main()
    input('Press Any key to quit !')