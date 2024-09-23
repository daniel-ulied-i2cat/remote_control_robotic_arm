import sys
import tty
import termios
import select
import time


class StdInOutController:
    """
    Class to control the standard input and output of the terminal.
    """
    def __init__(self):
        pass

    def disable_echo(self) -> list:
        """
        Function to disable user keys to be seen in terminal

        Parameters
        ----------
        None

        Returns
        -------
        list
            Settings of the terminal
        """
        fd = sys.stdin.fileno()
        original_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        new_settings = termios.tcgetattr(fd)
        new_settings[3] &= ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
        return original_settings

    def restore_terminal(self, original_settings: list) -> None:
        """
        Function to restore terminal

        Parameters
        ----------
        original_settings: list

        Returns
        -------
        None
        """
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)

    def get_key(self) -> str:
        """
        Function to get the key pressed by the user.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The key pressed by the user
        """
        original_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
            else:
                key = ''
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)
        return key

    def animate(self) -> None:
        """
        Function to animate the moving message on the terminal.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        animation = ["Moving...   ", "Moving..    ", "Moving...   "]
        for frame in animation:
            sys.stdout.write(f"\r{frame}")
            sys.stdout.flush()
            time.sleep(0.2)
