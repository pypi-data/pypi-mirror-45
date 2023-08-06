import subprocess
import os
from threading import Thread
import localpubsub as lps

NULL_PIPE = open(os.devnull, 'w')

SoundErrorPub = lps.VariablePub()


def ffmpeg_err_fun(line):
    if 'No such file or directory' in line:
        SoundErrorPub.publish(RuntimeError(line))
        raise RuntimeError(line)


def process_output(process,  # type: subprocess.Popen
                   err_fun=ffmpeg_err_fun):
    #  https://stackoverflow.com/a/34317431
    polled = True
    while polled:
        process.wait()
        out, err = process.communicate()
        err = str(err).replace('\\n', '\n')
        err = str(err).replace('\\r', '\n')
        for line in err.splitlines():
            err_fun(line)
        polled = process.poll()


def ffplay_err_catch(f):
    def fun(*args, **kwargs):
        p = f(*args, **kwargs)
        Thread(target=process_output, args=[p]).start()
        return p

    return fun


def unix_dep_catch(f):
    def fun(*args, **kwargs):
        try:
            f2 = ffplay_err_catch(f)
            f2(*args, **kwargs)
        except FileNotFoundError as fnf:
            if fnf.strerror is not None and "ffplay" in fnf.strerror:
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
    if os.path.isfile(filename):
        return subprocess.Popen(["ffplay", "-nodisp", "-autoexit", '--', filename], stderr=subprocess.PIPE,
                                stdout=NULL_PIPE)
    else:
        raise FileNotFoundError("Could not find file: {}".format(filename))


@unix_dep_catch
def loop_file(filename, loops):
    assert isinstance(loops, int)
    if os.path.isfile(filename):
        return subprocess.Popen(["ffplay", "-nodisp", "-loop", str(loops), '--', filename], stderr=subprocess.PIPE,
                                stdout=NULL_PIPE)
    else:
        raise FileNotFoundError("Could not find file: {}".format(filename))
