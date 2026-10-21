"""Tk: the main window, with an event loop, timers (after), and key bindings.

There is no way to read the keyboard while the program runs (no system module
and input() blocks), so the loop works like this:
  * time is virtual: every loop frame is FRAME_MS milliseconds, paced by core.pacer;
  * `after(ms, func)` schedules callbacks on that virtual time, exactly as tkinter does;
  * Ctrl+C pauses the loop and opens a key menu: typing a key fires its `<Key-x>`
    bindings (every Button with a key has one), like pressing it on a keyboard.
"""

from clock_library.minitk.colors import parse_color
from clock_library.minitk.surface import Surface
from clock_library.minitk.widgets import Frame
from core.pacer import (
    FRAMES_PER_SECOND,
    MIN_CALIBRATION_SECONDS,
    create_pacer,
    finish_calibration,
    start_calibration,
    wait_frame,
)

FRAME_MS = 1000 // FRAMES_PER_SECOND
CURSOR_HOME = "\033[H"
CLEAR_SCREEN = "\033[2J\033[H"
CLEAR_LINE = "\033[K"
CLEAR_BELOW = "\033[J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
DIM = "\033[2m"
RESET = "\033[0m"


class Event:
    """What a key binding receives: the typed text as 'char' and 'keysym'."""

    def __init__(self, text):
        self.char = text
        self.keysym = text.lower()


class Tk(Frame):
    """Main window. Build widgets inside it, schedule work with after(), call mainloop()."""

    def __init__(self, title="minitk"):
        super().__init__(None, border="silver", title=title)
        self.pacer = create_pacer()
        self.buttons = []
        self.changed = True
        self.hint = "Ctrl+C = pausa y menú de teclas"
        self._bindings = {}
        self._timers = []  # (due time in ms, id, function, arguments)
        self._next_timer = 1
        self._now = 0
        self._running = False
        self._interrupted = False
        self._bell = False

    # -- window ----------------------------------------------------------------

    def title(self, text=None):
        """Get or set the window title."""
        if text is None:
            return self.options["title"]
        self.configure(title=text)
        return None

    def bell(self):
        """Ring the terminal bell on the next redraw."""
        self._bell = True

    # -- timers and events -----------------------------------------------------

    def after(self, ms, func, *args):
        """Run func(*args) after ms milliseconds of loop time. Return an id for after_cancel."""
        timer_id = self._next_timer
        self._next_timer += 1
        self._timers.append((self._now + ms, timer_id, func, args))
        return timer_id

    def after_cancel(self, timer_id):
        """Cancel a pending timer."""
        self._timers = [timer for timer in self._timers if timer[1] != timer_id]

    def bind(self, sequence, func):
        """Call func(event) when a key is typed in the menu: '<Key-x>' or '<Key>' for any."""
        self._bindings.setdefault(sequence.lower(), []).append(func)

    def _dispatch_key(self, text):
        """Fire the bindings of a typed key. Return False if nothing was bound to it."""
        event = Event(text)
        handlers = self._bindings.get("<key-" + event.keysym + ">", [])
        handlers = handlers + self._bindings.get("<key>", [])
        for handler in handlers:
            handler(event)
        return bool(handlers)

    def _run_due_timers(self):
        while True:
            due = [timer for timer in self._timers if timer[0] <= self._now]
            if not due:
                return
            timer = min(due)
            self._timers.remove(timer)
            # Callbacks should reschedule themselves first: a Ctrl+C that lands inside
            # one is kept for the end of the frame so the loop never loses its timers.
            try:
                timer[2](*timer[3])
            except KeyboardInterrupt:
                self._interrupted = True

    # -- drawing ---------------------------------------------------------------

    def draw_window(self):
        """Redraw the window in place, without clearing the screen (no flicker)."""
        width, height = self.natural_size()
        surface = Surface(width, height)
        self.draw(surface, 0, 0, width, height)
        lines = [line + CLEAR_LINE for line in surface.lines()]
        lines.append(DIM + " " + self.hint + RESET + CLEAR_LINE)
        ring = "\a" if self._bell else ""
        print(CURSOR_HOME + "\n".join(lines) + "\n" + CLEAR_BELOW + ring, end="", flush=True)
        self._bell = False
        self.changed = False

    def update(self):
        """Redraw now if anything changed (like tkinter's update())."""
        if self.changed:
            self.draw_window()

    # -- loop ------------------------------------------------------------------

    def _frame(self):
        self._interrupted = False
        self._run_due_timers()
        self.update()
        wait_frame(self.pacer)
        self._now += FRAME_MS
        if self._interrupted:
            raise KeyboardInterrupt

    def _run_frames(self, limit=None):
        """Run frames until quit(), the limit, or Ctrl+C. Return True if interrupted."""
        count = 0
        try:
            while self._running and (limit is None or count < limit):
                self._frame()
                count += 1
        except KeyboardInterrupt:
            return True
        return False

    def mainloop(self, max_frames=None):
        """Run the window until quit(). max_frames stops earlier (useful for tests)."""
        self._running = True
        print(CLEAR_SCREEN + HIDE_CURSOR, end="")
        try:
            while self._running:
                if self._run_frames(max_frames):
                    print(SHOW_CURSOR, end="")
                    self._key_menu()
                    print(CLEAR_SCREEN + HIDE_CURSOR, end="")
                    self.changed = True
                elif max_frames is not None:
                    break
        finally:
            print(SHOW_CURSOR)

    def quit(self):
        """Stop mainloop()."""
        self._running = False

    destroy = quit

    # -- Ctrl+C menu -----------------------------------------------------------

    def _key_menu(self):
        """Paused window plus a prompt where typed keys fire their bindings."""
        while self._running:
            print(CLEAR_SCREEN, end="")
            self.draw_window()
            print("Pausa. Teclas disponibles:")
            for button in self.buttons:
                if button.options["key"]:
                    print("  " + button.options["key"].ljust(3) + button.options["text"])
            print("  calibrar   ajustar la velocidad del reloj      salir   cerrar la ventana")
            try:
                line = input("Tecla (Enter = seguir): ").strip()
            except (EOFError, KeyboardInterrupt):
                self.quit()
                return
            if line == "":
                return
            if line.lower() == "salir":
                self.quit()
            elif line.lower() == "calibrar":
                self._calibrate()
            elif not self._dispatch_key(line):
                print("Esa tecla no hace nada.")
                input("[Enter para continuar]")

    def _calibrate(self):
        """Correct the speed: the window runs while the user times it with a stopwatch."""
        print("Calibración: inicia un cronómetro real (el del celular sirve) y pulsa Enter.")
        print(f"Deja correr el reloj al menos {MIN_CALIBRATION_SECONDS} s (mejor 30 s o más) "
              "y pulsa Ctrl+C en el instante en que pares tu cronómetro.")
        input("Enter para empezar... ")
        print(CLEAR_SCREEN + HIDE_CURSOR, end="")
        self.changed = True
        start_calibration(self.pacer)
        self._run_frames()
        print(SHOW_CURSOR)
        try:
            real_seconds = float(input("¿Cuántos segundos marcó tu cronómetro? ").replace(",", "."))
        except ValueError:
            print("Número no válido: sin cambios.")
            return
        accuracy = finish_calibration(self.pacer, real_seconds)
        if accuracy is None:
            print(f"Medida muy corta (mínimo {MIN_CALIBRATION_SECONDS} s): sin cambios.")
        else:
            print(f"Calibrado: el reloj iba al {accuracy} %. Repite para afinar.")
        input("[Enter para continuar]")
