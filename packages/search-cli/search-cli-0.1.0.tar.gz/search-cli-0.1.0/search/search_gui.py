try:
    from tkinter import *
except ImportError:
    from Tkinter import *

import os
import sys
import argparse
import platform
from search.search import get_highlighted, get_clipboard, search, get_engine


def search_gui_highlighted(text=None):
    text = " ".join(text) if text is not None else ""
    search_gui(text)


def search_gui(seed=None):
    seed = seed if seed is not None else []
    engine = get_engine('google')

    master = Tk()

    v = StringVar()
    e = Entry(master, textvariable=v, width=len(seed) + 100)
    e.pack()
    if seed:
        v.set(seed)
        e.icursor(len(seed))

    def callback(event):
        query = v.get().split()
        search(engine, query)
        close(event)

    def close(event):
        master.destroy()
        sys.exit()

    e.bind("<Return>", callback)
    e.bind("<Escape>", close)
    if platform.system() != 'Windows':
        master.wm_attributes('-type', 'splash')
        if os.getenv('SR_CLOSE_LOSS_FOCUS', 'yes') == 'yes':
            e.bind("<FocusOut>", close)

    e.focus()
    mainloop()


def main():
    parser = argparse.ArgumentParser("Search the web.")
    parser.add_argument("query", nargs="*", help="What to seed the search bar with")
    args = parser.parse_args()
    args.query = args.query if args.query is not None else get_highlighted()
    search_gui_highlighted(args.query)


if __name__ == "__main__":
    main()
