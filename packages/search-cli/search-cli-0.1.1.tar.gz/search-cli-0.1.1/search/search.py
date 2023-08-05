"""Search the web with surfraw. `sudo apt install surfraw surfraw-extras xclip`"""

import os
import argparse
import platform
from subprocess import call, check_output, PIPE


def get_engine(default, ENV_KEY="SRENGINE"):
    return os.environ.get(ENV_KEY, default)


def get_clipboard_linux(board="c"):
    try:
        return check_output(
            ["xclip", "-sel", board, "-o"],
            stderr=PIPE,
            universal_newlines=True,
        ).rstrip("\n").split()
    except:
        return ""


def get_highlighted():
    return get_clipboard_linux(board="p")

	
def get_clipboard():
	if platform.system() == 'Windows':
		return get_clipboard_win()
	return get_clipboard_linux()


def get_clipboard_win():
	import pyperclip
	return pyperclip.paste().split()


def search_linux(engine, query):
    cmd = ["surfraw", engine]
    cmd.extend(query)
    call(cmd)


def search_win(query):
	query = "+".join(query)
	cmd = ['start', 'www.google.com/search?q={}'.format(query)]
	call(" ".join(cmd), shell=True)

	
def search(engine, query):
	if platform.system() == 'Windows':
		search_win(query)
	else:
		search_linux(engine, query)


def main():
    parser = argparse.ArgumentParser("Search the web.")
    parser.add_argument(
        '--engine', '-e',
        default=get_engine('google'),
        help="The search engine to use. You can also set with `$SRENGINE` env variable."
    )
    parser.add_argument('query', nargs="*", help="What to search for, if none then read from the clipboard.")
    args = parser.parse_args()

    if not args.query:
        args.query = get_clipboard()

    search(args.engine, args.query)


def search_highlighted():
    query = get_highlighted()
    engine = get_engine('google')
    search(engine, query)


if __name__ == "__main__":
    main()
