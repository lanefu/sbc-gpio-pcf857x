import gpiod
import threading

class armbianGpios():
    """
    A class used to manipulate gpios as outputs.

    It uses gpiod. All lines are set to gpio output active high.
    Once the class is instantiated, all lines are set to 0.

    Attributes
    ----------
    chip : str
        gpio chip device file path (e.g. /dev/gpiochip0)
    lines : dict
        a dictionnary associating a gpio line number to a gpiod line
    timer : Threading.Timer
        a timer to bounce lines
time
    Methods
    -------
    get_all()
        Returns a dictionnary summuraizing the gpios line state
    get(line)
        Returns a dictionnary summuraizing the gpio `line` state
    set_all(value)
        Sets all lines to `value`
    set(line, value)
        Sets `line` to `value`
    toggle_all()
        Toggles all lines
    toggle(line)
        Toggles `line`
    bounce_all(timeSec)
        Toggles all lines for `timeSec` seconds
    bounce(line, timeSec)
        Toggles `line` for `timeSec` seconds

    """
    def __init__(self, chip, lines):
        """
        Parameters
        ----------
        chip : str
            gpio chip device file path (e.g. /dev/gpiochip0)
        lines : list of int
            A list of gpio lines

        """
        self.chip = gpiod.chip(chip)
        self.lines = dict()
        self.timer = None

        for l in lines:
            line = self.chip.get_line(l)
            self.lines[l] = line
            config = gpiod.line_request()
            config.consumer = "armbian-gpio"
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT
            line.request(config)
            line.set_value(0)

    def get_all(self):
        """
        Returns
        -------
        state : a dictionnary of gpio lines attributes

        """
        state = dict()
        for l in self.lines:
            state[l] = self.get(l)
        return state

    def get(self, line):
        """
        Parameters
        ----------
        line : int
            the line number to get info from
        Returns
        -------
        state : a dictionnary of gpio `line` attributes

        """
        state = dict()
        if self.lines[line].direction == gpiod.line.DIRECTION_INPUT:
            state['direction'] = "input"
        else:
            state['direction'] = "output"
        if self.lines[line].active_state == gpiod.line.ACTIVE_HIGH:
            state['active'] = "high"
        else:
            state['active'] = "low"
        state['value'] = self.lines[line].get_value()
        return state

    def set_all(self, value):
        """
        Parameters
        ----------
        value : int
            the value to set for all lines (0 or 1)

        """
        for l in self.lines:
            self.set(l, value)

    def set(self, line, value):
        """
        Parameters
        ----------
        line : int
            the line number to set
        value : int
            the value to set for `line` (0 or 1)

        """
        try:
            self.lines[line].set_value(value)
        except KeyError:
            raise

    def toggle_all(self):
        for l in self.lines:
            self.toggle(l)

    def toggle(self, line):
        """
        Parameters
        ----------
        line : int
            the line number to toggle

        """
        try:
            self.set(line, not self.lines[line].get_value())
        except KeyError:
            raise

    def bounce_all(self, timeSec):
        """
        Parameters
        ----------
        timeSec : int
            the bounce time in second

        """
        if self.timer is not None:
            if self.timer.is_alive():
                return
        self.toggle_all()
        self.timer = threading.Timer(timeSec, self.toggle_all)
        self.timer.start()

    def bounce(self, line, timeSec):
        """
        Parameters
        ----------
        line : int
            the line number to bounce
        timeSec : int
            the bounce time in second

        """
        if self.timer is not None:
            if self.timer.is_alive():
                return
        try:
            self.toggle(line)
            self.timer = threading.Timer(timeSec, self.toggle, [line])
            self.timer.start()
        except KeyError:
            raise
