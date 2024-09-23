#!/usr/bin/env python3

from pathlib import Path
import subprocess

ASCII_ART_PATH = Path(__file__).parent.joinpath('./figures/ned2_ascii')
MOTD_PATH = Path('/etc/update-motd.d')
MOTD_CONTENT = "50-landscape-sysinfo"
COMMAND_PATH =  Path(__file__).parent.joinpath('./figures/command_help')

MIN_PADDING = 3

# we don't center the art in order to avoid the most possible line wraps after a terminal resize
CENTER_ART = False


def get_output(*bash_command):
    process = subprocess.run(bash_command, capture_output=True, encoding='utf-8')
    return process.stdout


def read_motd(path: Path):
    if path.is_file():
        return get_output(path).strip()
    motd = ''
    for p in path.iterdir():
        if p.name != MOTD_CONTENT:
            continue
        motd += get_output(p)
    return motd.strip()


def get_term_width():
    return int(get_output('tput', 'cols'))


def get_text_height(text):
    return len(text.splitlines())


def get_text_width(text):
    return max(len(line) for line in text.splitlines())


if __name__ == '__main__':
    ascii_art = ASCII_ART_PATH.read_text('utf-8')
    motd = read_motd(MOTD_PATH)
    commands_help = COMMAND_PATH.read_text('utf-8')
    motd = motd + commands_help

    term_width = get_term_width()

    ascii_height = get_text_height(ascii_art)
    ascii_width = get_text_width(ascii_art)
    motd_height = get_text_height(motd)
    motd_width = get_text_width(motd)

    available_space = term_width - motd_width - 2 * MIN_PADDING

    if available_space < ascii_width:
        print(motd)
        print(ascii_art)
        exit(0)

    motd_lines = motd.splitlines()
    ascii_art_lines = ascii_art.splitlines()

    height_diff = motd_height - ascii_height

    abs_height_diff = abs(height_diff)

    top_padding = abs_height_diff // 2
    bottom_padding = abs_height_diff - top_padding

    # motd_height > ascii_height
    if height_diff > 0:
        ascii_art_lines = [' '] * top_padding + ascii_art_lines + [' '] * bottom_padding
    # ascii_height > motd_height
    elif height_diff < 0:
        motd_lines = [' '] * top_padding + motd_lines + [' '] * bottom_padding

    const_padding = (available_space - ascii_width) // 2 if CENTER_ART else MIN_PADDING
    for motd_line, ascii_art_line in zip(motd_lines, ascii_art_lines):
        padding = ' ' * (const_padding + motd_width - len(motd_line))
        line = motd_line + padding + ascii_art_line
        print(line)
