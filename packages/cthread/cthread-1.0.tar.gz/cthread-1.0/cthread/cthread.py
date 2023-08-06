import logging
import threading
import time

import queue as q

class CThreadException(Exception):
    """ Base class of any ControllableThread exception. """

    def __init__(self, message=None, *args, **kwargs):
        """ Initialises the base class of the ControllableThread exception.
        
        Args:
            message: Information about the exception that was raised
        """
        Exception.__init__(self, *args, **kwargs)

        self._message = message

    def __str__(self):
        """ Overrides the __str__ method of the Exception class."""
        if self._message == None:
            return Exception.__str__(self)
        else:
            return self._message

class InvalidArgument(CThreadException):
    """ Base class of any invalid argument exception. """

    def __init__(self, message=None, *args, **kwargs):
        """ Initialises the base class of the invalid argument exception.
        
        Args:
            message: Information about the exception that was raised.
        """
        if message == None:
            message = "Specified argument is invalid."

        CThreadException.__init__(self, message, *args, *kwargs)

class InvalidState(InvalidArgument):
    """ Desired state of the thread is not a recognised state. """

    def __init__(self, message=None, *args, **kwargs):
        """ Initialises the invalid state exception.
        
        Args:
            message: Information about the exception that was raised.
        """
        if message == None:
            message = "Invalid state.  Ensure: state is <class 'int'> and " \
                    "STARTED <= state <= maxState."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class InvalidName(InvalidArgument):
    """ Desired name of the thread is not a string. """

    def __init__(self, message=None, *args, **kwargs):
        """ Initialises the invalid name exception.
        
        Args:
            message: Information about the exception that was raised.
        """
        if message == None:
            message = "Invalid name.  Ensure: name is <class 'str'>."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class InvalidQueue(InvalidArgument):
    """ Communication method to the initialising thread is not a queue. """

    def __init__(self, message=None, *args, **kwargs):
        """ Initialises the invalid queue exception.
        
        Args:
            message: Information about the exception that was raised.
        """
        if message == None:
            message = "Invalid queue.  Ensure: queue is <class 'queue.Queue'>."

        InvalidArgument.__init__(self, message, *args, **kwargs)

class ThreadState(object):
    """ Represents the state of the thread. """

    def __init__(self):
        """ Initialise the thread state constants and the thread state. """
        self.STARTED = 0
        self.ACTIVE = 1
        self.IDLE = 2
        self.PAUSED = 3
        self.RESUMED = 4
        self.KILLED = 5

        self._maxState = self.KILLED
        self._state = self.STARTED

    def update_max_state(self, maxState):
        """ Update the maximum state of the thread.

        Args:
            maxState: Maximum state that the thread can take.

        Raises:
            InvalidState: if the maximum state is < STARTED.
        """
        if not isinstance(maxState, int) or maxState < self.STARTED:
            raise InvalidState("Invalid maxState.  Ensure: maxState is " \
                    "<class 'int'> and STARTED <= maxState.")
        
        self._maxState = maxState

    def update_state(self, state):
        """ Update the state of the thread.
        
        Args:
            state: New state of the thread.

        Raises:
            InvalidState: If the updated state value is < STARTED or > maxState.
        """
        if not isinstance(state, int) or state < self.STARTED or \
                state > self._maxState:
            raise InvalidState()

        self._state = state

    def get_state(self):
        """ Get the state of the thread.

        Returns:
            STARTED: if the thread is being initialised,
            ACTIVE: if the thread is currently running,
            IDLE: if the thread is currently not running,
            PAUSED: if the thread is transitioning from running to not running.
            RESUMED: if the thread is transitioning from not running to running.
            KILLED: if the thread is in the process of terminating,
            other: if there is any individual thread-specific states.
        """
        return self._state

class ControllableThread(threading.Thread):
    """ Parent class for all of the threads used within Hugo.

    Allows threads to be killed, paused and resumed, and allows for direct
    communication to the main initialising thread.
    """

    def __init__(self, name, queue):
        """ Initialise the parent class of all the threads used in Hugo.

        Create the thread state and the communication queue to the main thread.

        Args:
            name: Name of the thread.
            queue: Priority queue for communication to the main thread.

        Raises:
            InvalidName: if name is not a string.
            InvalidQueue: if queue is not a Queue.
        """
        threading.Thread.__init__(self)

        if not isinstance(name, str):
            raise InvalidName()
            
        if not isinstance(queue, q.Queue):
            raise InvalidQueue()

        self._name = name
        self._queue = queue
        self._logger = logging.getLogger(name + "_t")
        self._threadState = ThreadState()

    def _started_callback(self):
        """ Thread start callback function.  May be overwritten by child. """
        self._logger.info("(Re)initialising...")

    def _active_callback(self):
        """ Thread active callback function.  May be overwritten by child. """
        pass

    def _idle_callback(self):
        """ Thread idle callback function.  May be overwritten by child. """
        pass

    def _paused_callback(self):
        """ Thread paused callback function.  May be overwritten by child. """
        self._logger.info("Pausing...")

    def _resumed_callback(self):
        """ Thread resume callback function.  May be overwritten by child. """
        self._logger.info("Resuming...")

    def _killed_callback(self):
        """ Thread killed callback function.  May be overwritten by child. """
        self._logger.info("Killing...")

    def _alternative_callback(self):
        """ Alternative state callback function.  May not be implemented. """
        pass

    def _is_started(self):
        """ Check if the thread state is STARTED.

        Returns:
            True if the thread state is STARTED, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.STARTED

    def _is_active(self):
        """ Check if the thread state is ACTIVE.

        Returns:
            True if the thread state is ACTIVE, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.ACTIVE

    def _is_idle(self):
        """ Check if the thread state is IDLE.

        Returns:
            True if the thread state is IDLE, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.IDLE

    def _is_paused(self):
        """ Check if the thread state is PAUSED.

        Returns:
            True if the thread state is PAUSED, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.PAUSED

    def _is_resumed(self):
        """ Check if the thread state is RESUMED.

        Returns:
            True if the thread state is RESUMED, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.RESUMED

    def _is_killed(self):
        """ Check if the thread state is KILLED.

        Returns:
            True if the thread state is KILLED, and
            False if the thread state is not.
        """
        return self._get_state() == self._threadState.KILLED

    def _update_max_state(self, maxState):
        """ Update the maximum state of the thread.

        Args:
            maxState: Maximum state that the thread can take.

        Raises:
            InvalidState: if the maximum state is < STARTED.
        """
        self._threadState.update_max_state(maxState)

    def _update_state(self, state):
        """ Update the state of the thread.
        
        Args:
            state: New state of the thread.

        Raises:
            InvalidState: If the updated state value is < STARTED or > KILLED.
        """
        self._threadState.update_state(state)

    def _get_state(self):
        """ Get the state of the thread.

        Returns:
            STARTED: if the thread is being initialised,
            ACTIVE: if the thread is currently running,
            IDLE: if the thread is currently not running,
            PAUSED: if the thread is transitioning from running to not running.
            RESUMED: if the thread is transitioning from not running to running.
            KILLED: if the thread is in the process of terminating,
            other: if there is any individual thread-specific states.
        """
        return self._threadState.get_state()

    def run(self):
        """ Entry point for the thread.

        Contains the cyclic executive of the thread.  There are at least six
        possible states for the thread:
            1. STARTED
            2. ACTIVE
            3. IDLE
            4. PAUSED
            5. RESUMED
            6. KILLED
            7. Any alternative individual thread-specific states.
        
        Each of these states has a callback function that must be implemented
        in any of the child threads.  Of course, the alterative state callback
        should not be implemented if there are no alternative states.
        
        This cyclic executive will execute as long as the thread is not killed.
        """
        self._logger.info("Starting thread: {0}...".format(self._name))

        while not self._is_killed():

            # Initialise thread #
            if self._is_started():
                self._started_callback()

            # Start running the thread #
            elif self._is_active():
                self._active_callback()

            # Stop running the thread #
            elif self._is_idle():
                self._idle_callback()

            # Transition the thread from running to not running #
            elif self._is_paused():
                self._paused_callback()

            # Transition the thread from not running to running #
            elif self._is_resumed():
                self._resumed_callback()

            # Thread specific state must begin #
            else:
                self._alternative_callback()

        # Kill the thread #
        self._killed_callback()
        self._logger.info("Stopping thread: {0}...".format(self.name))

    def reset(self):
        """ Update the state of the thread to reset it. """
        self._update_state(self._threadState.STARTED)

    def pause(self):
        """ Update the state of the thread to pause it. """
        self._update_state(self._threadState.PAUSED)

    def resume(self):
        """ Update the state of the thread to resume it. """
        self._update_state(self._threadState.RESUMED)

    def kill(self):
        """ Update the state of the thread to kill it. """
        self._update_state(self._threadState.KILLED)