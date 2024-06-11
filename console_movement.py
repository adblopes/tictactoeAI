import msvcrt
import ctypes

# Define necessary types from ctypes
SHORT = ctypes.c_short
WORD = ctypes.c_ushort
DWORD = ctypes.c_ulong

class COORD(ctypes.Structure):
    _fields_ = [("X", SHORT), ("Y", SHORT)]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", SHORT), ("Top", SHORT),
                ("Right", SHORT), ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", WORD),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]

# Get handle to standard output
STD_OUTPUT_HANDLE = -11
stdout_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

# Get the current cursor position.
def get_cursor_position():
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    ctypes.windll.kernel32.GetConsoleScreenBufferInfo(stdout_handle, ctypes.byref(csbi))
    return csbi.dwCursorPosition.Y, csbi.dwCursorPosition.X

# Move the cursor to the specified position.
def move_cursor(y, x):
    pos = COORD(x, y)
    ctypes.windll.kernel32.SetConsoleCursorPosition(stdout_handle, pos)

# Replace whatever is at the (y, x) coordinate with the given character.
def replace_at_position(char, y, x):
    move_cursor(y, x)
    ctypes.windll.kernel32.WriteConsoleW(stdout_handle, ctypes.create_unicode_buffer(char), 1, None, None)

# Wait for keyboard input.
def wait_for_input():
    return msvcrt.getch()

def run_cursor_movement():
    while True:
        key = wait_for_input()

        if key == b'\xe0':  # Arrow keys are a two-byte sequence in Windows
            arrow_key = wait_for_input()
            y, x = get_cursor_position()

            if arrow_key == b'H':  # Up arrow
                y = max(0, y - 1)
            elif arrow_key == b'P':  # Down arrow
                y += 1
            elif arrow_key == b'K':  # Left arrow
                x = max(0, x - 1)
            elif arrow_key == b'M':  # Right arrow
                x += 1
            
            move_cursor(y, x)
        elif key == b'\r':  # Enter key
            return get_cursor_position()
        elif key == b'\x03':
            raise KeyboardInterrupt

if  __name__ == "__main__":
    run_cursor_movement()