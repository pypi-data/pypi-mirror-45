import io
import shutil
import warnings
import os
import traceback

__version__ = '1.0.4'


class DiarySkipLoggingException(Exception):
    """
    Tagging exception used to signal the diary prompt to not log the function it is raised in.
    """
    pass


class Diary:
    """
    MatLab style commands logger for the Python interpreter, with added feature. Construct a new instance to enable
    logging and call diary.off() to disable it.
    """

    # Default values for parameters
    _default_filename = 'diary.py'
    _buffered_default = True

    _diary_on = False
    _filename = None

    _buffered = None

    # Stream where commands are written. Can be either a file or a StringIO depending on the mode used
    _cmd_stream = None

    def __init__(self, filename=_default_filename, buffered=_buffered_default):
        """
        Initializes and starts a new Diary, with the given or default filename.

        :param filename: Name of the file where the commands are logged
        """
        self._filename = filename
        self._buffered = buffered

        self.on()

    def _print_command_line(self, secondary=False):
        if secondary:
            print('[{}] ... '.format(os.path.basename(self._filename)), end='')
        else:
            print('[{}] >>> '.format(os.path.basename(self._filename)), end='')

    def _check_and_start_secondary_prompt(self, cmd):
        if cmd[-1:] == ':':
            cmd += '\n'

            while True:
                self._print_command_line(True)

                current_cmd = input()
                cmd += current_cmd + '\n'

                if not current_cmd[:1] == ' ' and not current_cmd[:1] == '\t' and not current_cmd[-1:] == ':':
                    break
        return cmd

    def _start_prompt(self):
        # Allows calling diary.off()
        diary = self

        while True:
            self._print_command_line()

            cmd = None
            try:
                cmd = input()

                # Check if expression need continuation and eventually start a prompt
                cmd = self._check_and_start_secondary_prompt(cmd)

                code = compile(cmd, filename='<string>', mode='single')
                exec(code)
            except EOFError:
                self.off()
            except KeyboardInterrupt:
                print('\nKeyboardInterrupt')
                continue
            except DiarySkipLoggingException:
                # Requested to skip logging
                continue
            except Exception:
                traceback.print_exc()
                continue

            if not self._diary_on:
                break

            self._cmd_stream.write(cmd + '\n')

    def flush(self) -> None:
        """
        Writes commands stored in the buffer to the diary file. This feature is only supported in buffered mode.
        """
        if not self._diary_on:
            warnings.warn('Diary is off. Cannot flush commands.')

        if self._buffered:
            with open(self._filename, 'a+') as f:
                # Go to beginning of stream
                self._cmd_stream.seek(0)
                # Copy content of buffer stream to actual file
                shutil.copyfileobj(self._cmd_stream, f)
                # Empty the stream
                self._cmd_stream.seek(0)
                self._cmd_stream.truncate(0)
        else:
            warnings.warn('Not in buffered mode: commands already written to file.')
        # If still logging, skip logging the flush function itself
        if self._diary_on:
            raise DiarySkipLoggingException

    def discard(self) -> None:
        """
        Discards all commands stored in the buffer. These are all commands typed after the last diary.flush() or
        diary.on() call. This feature is only supported in buffered mode.
        """
        if not self._diary_on:
            warnings.warn('Diary is off. Cannot discard commands.')

        if self._buffered:
            # Empty the stream
            self._cmd_stream.seek(0)
            self._cmd_stream.truncate(0)
        else:
            warnings.warn('Not in buffered mode: feature not supported.')
        raise DiarySkipLoggingException

    def on(self) -> None:
        """
        Turns this Diary instance on, logging any command typed afterwards. Call diary.off() to disable logging.
        """
        if self._diary_on:
            return

        # Open stream depending on whether buffered mode is active or not
        if self._buffered:
            self._cmd_stream = io.StringIO()
        else:
            self._cmd_stream = open(self._filename, 'a+')

        self._diary_on = True
        self._start_prompt()

    def off(self) -> None:
        """
        Turns this Diary instance off, disabling logging and flushing any buffered command to the file, if needed. As
        long as the Diary is enabled, diary.off() is an alias for self.off().
        """
        if not self._diary_on:
            return

        self._diary_on = False
        if self._buffered:
            self.flush()
        self._cmd_stream.close()
