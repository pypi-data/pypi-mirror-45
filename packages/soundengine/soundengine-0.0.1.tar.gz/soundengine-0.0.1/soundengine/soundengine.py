import subprocess
import os

NULL_PIPE = open(os.devnull, 'w')


def ffplay_err_catch(f):
    def fun(*args, **kwargs):
        p = f(*args, **kwargs)
        out, err = p.communicate(input=None, timeout=0.1)
        err = str(err).replace('\\n', '\n')
        err = str(err).replace('\\r', '\n')
        for l in str(err).splitlines():
            if 'No such file or directory' in l:
                raise RuntimeError(l)
        return p

    return fun


def unix_dep_catch(f):
    def fun(*args, **kwargs):
        try:
            f2 = ffplay_err_catch(f)
            f2(*args, **kwargs)
        except FileNotFoundError as fnf:
            if "ffplay" in fnf.strerror:
                raise RuntimeError(
                    "ffplay not found. If in Ubuntu, please run `sudo apt install ffmpeg` in a terminal. "
                    "If in Mac OS, run `brew install ffmpeg` instead."
                    "If in Windows, please go to the github repo for this project, code a fix, and make a pull request "
                    "to support windows.")
            else:
                raise fnf

    return fun


@unix_dep_catch
def play_file(filename):
    return subprocess.Popen(["ffplay", "-nodisp", "-autoexit", filename], stderr=subprocess.PIPE, stdout=NULL_PIPE)


@unix_dep_catch
def loop_file(filename, loops):
    return subprocess.Popen(["ffplay", "-nodisp", "-loop", str(loops), filename], stderr=subprocess.PIPE,
                            stdout=NULL_PIPE)


if __name__ == '__main__':
    play_file('test.mp3')
    loop_file('test.flac', 9999)
    input("Play forever?")
