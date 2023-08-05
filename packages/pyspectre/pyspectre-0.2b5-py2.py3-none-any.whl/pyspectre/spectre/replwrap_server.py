import multiprocessing as mp
import threading
import sys
import time
import os

if sys.version_info.major == 3:
    import queue as queue
elif sys.version_info.major ==2:
    import Queue as queue


class REPLWrapper_client(object):

    def __init__(self,
                 cmd_or_spawn,
                 orig_prompt,
                 prompt_change=None,
                 server_process=False,
                 verbosity=1,
                 shutdown_event=None,
                 ):

        if shutdown_event is not None and shutdown_event.is_set():
            return

        if not server_process:
            self.inqueue = queue.Queue(1)
            self.outqueue = queue.Queue(1)
            self.shutdown = shutdown_event if shutdown_event else threading.Event()
            self.server = threading.Thread(
                target=REPLWrapper_server_fn,
                args=(
                    self.inqueue,
                    self.outqueue,
                    cmd_or_spawn,
                    orig_prompt,
                    prompt_change,
                    verbosity,
                    self.shutdown),
                daemon=True,
            )

        else:
            self.inqueue = mp.Queue(1)
            self.outqueue = mp.Queue(1)
            self.shutdown = shutdown_event if shutdown_event else mp.Event()
            self.server = mp.Process(
                target=REPLWrapper_server_fn,
                args=(
                    self.inqueue,
                    self.outqueue,
                    cmd_or_spawn,
                    orig_prompt,
                    prompt_change,
                    verbosity,
                    self.shutdown),
                daemon=True,
            )

        self.verbosity = verbosity
        self.server.start()
        self.pid = int(self.server.pid) if server_process else int(self._interact(('get_pid', (None,))))
        self.spectre_pid = int(self.run_command('sclGetPid()'))
        self.threadName = self.server.name if not server_process else None
        self.child = self

    def isalive(self):
        return self.server.is_alive()

    is_alive = isalive
    isAlive = isalive

    def run_command(self, *args, **kwargs):
        return self._eval_remote_method('run_command', args, kwargs)

    def notify_server(self):
        print('[REPLWrapper_client] notify_server()') if self.verbosity >= 4 else None
        while not self.inqueue.empty():
            _ = self.inqueue.get_nowait()
        self.inqueue.put('terminate')

    def terminate(self):
        # graceful exit
        print('[REPLWrapper_client] received terminate() request') if self.verbosity >= 4 else None
        self.notify_server()
        print('[REPLWrapper_client] joining server_thread') if self.verbosity >= 4 else None
        self.server.join()
        print('[REPLWrapper_client] joined server_thread') if self.verbosity >= 4 else None

    def kill(self):
        # ungraceful exit
        print('[REPLWrapper_client] received kill() request') if self.verbosity >= 4 else None
        try:
            os.kill(self.spectre_pid, 2)
            dead = False
        except:
            dead = True

        while not dead:
            time.sleep(1e-3)
            try:
                os.kill(self.spectre_pid, 2)
                os.kill(self.spectre_pid, 15)
                dead = False
            except:
                dead = True
        print('[REPLWrapper_client] killed spectre') if self.verbosity >= 4 else None
        print('[REPLWrapper_client] joining server thread') if self.verbosity >= 4 else None
        self.server.join()
        print('[REPLWrapper_client] joined server thread') if self.verbosity >= 4 else None

    def _eval_remote_method(self, method_name, args, kwargs):
            payload = ('eval_method', (method_name, args, kwargs))
            return self._interact(payload)

    def _interact(self, payload):
        if not self.shutdown.is_set() and self.isalive():

            while not self.shutdown.is_set():
                if not self.server.is_alive():
                    self.server.join()
                    break

                try:
                    self.inqueue.put(payload, block=False)
                    print('[REPLWrapper_client] sending payload: {}'.format(payload)) if self.verbosity >= 5 else None
                    break
                except queue.Full:
                    self.shutdown.wait(0.1e-3)

            while not self.shutdown.is_set():
                if not self.server.is_alive():
                    self.server.join()
                    break

                try:
                    result = self.outqueue.get(block=False)
                    break
                except queue.Empty:
                    self.shutdown.wait(0.1e-3)

            if self.shutdown.is_set():
                print('[REPLWrapper_client] received shutdown signal') if self.verbosity >= 2 else None
                self.kill()
                raise KeyboardInterrupt

            if not self.server.is_alive():
                print('[REPLWrapper_client] server died during call') if self.verbosity >= 3 else None
                self.kill()
                raise RuntimeError

            print('[REPLWrapper_client] returning result: {}'.format(result)) if self.verbosity >= 5 else None
            return result
        else:
            self.server.join()


def REPLWrapper_server_fn(inqueue, outqueue,
                       cmd_or_spawn,
                       orig_prompt,
                       prompt_change=None,
                       verbosity=1,
                       shutdown_event=None):

    from pexpect.replwrap import REPLWrapper
    # from pexpect.exceptions import EOF, TIMEOUT

    def kill_pid(pid):
        try:
            os.kill(pid, 0)
        except:
            return

        dead = False
        while not dead:
            try:
                os.kill(pid, 9)
                print('[REPLWrapper_server_fn] sent SIGKILL {}'.format(pid)) if verbosity >= 4 else None
            except:
                dead = True
            time.sleep(0.5e-3)
        print('[REPLWrapper_server_fn] killed {}'.format(pid)) if verbosity >= 4 else None

    if shutdown_event is not None and shutdown_event.is_set():
        return

    try:
        spectre = REPLWrapper(
            cmd_or_spawn,
            orig_prompt,
            prompt_change)
        spectre_pid = int(spectre.run_command('sclGetPid()'))
        bash_pid = int(spectre.child.pid)

        def try_kill():
            kill_pid(spectre_pid)
            if spectre.child.isalive():
                spectre.child.close()
                # # wait will wait indefinitely if there are unread characters in the buffer:
                # while True:
                #     try:
                #         spectre.child.read_nonblocking(size=1, timeout=0)
                #     except TIMEOUT:
                #         break
                #     except EOF:
                #         break
            #print('[REPLWrapper_server_fn] waiting to join repl process') if verbosity >= 3 else None
            # spectre.child.wait()
            #print('[REPLWrapper_server_fn] joined repl process') if verbosity >= 3 else None

        print('[REPLWrapper_server_fn] started') if verbosity >= 3 else None
        print('[REPLWrapper_server_fn] spectre PID: {}'.format(spectre_pid)) if verbosity >= 3 else None
        print('[REPLWrapper_server_fn] bash PID: {}'.format(bash_pid)) if verbosity >= 3 else None
        spectre.child.delayafterclose = 0.0
        spectre.child.delaybeforesend = 0.0
        spectre.child.delayafterread = 0.0
        spectre.child.delayafterterminate = 0.0

        for payload in iter(inqueue.get, 'terminate'):

            if not spectre.child.isalive():
                raise RuntimeError('[REPLWrapper_server_fn] you asked for something from a dead spectre')

            # pull out fn from args
            assert isinstance(payload, tuple) and len(payload) == 2
            fnselect = payload[0]
            fnargs = payload[1]

            # define functions:
            if fnselect == 'eval_method':
                command = fnargs[0]
                args = fnargs[1]
                kwargs = fnargs[2]

                outqueue.put(getattr(spectre, command)(*args, **kwargs), block=True, timeout=None)

            if fnselect == 'get_pid':
                outqueue.put(spectre.child.pid)

        print('[REPLWrapper_server_fn] received \'terminate\' in queue') if verbosity >= 3 else None
        raise EOFError

    except EOFError:
        pass

    except Exception as e:

        exception_handled = False

        print('[REPLWrapper_server_fn] exception raised in replServer') if verbosity >= 3 else None

        def handle_msg(exception_type):
            print('[REPLWrapper_server_fn] exception \'{}\' handled by replServer'.format(exception_type)) if verbosity >= 3 else None

        if 'command' in locals() and command == 'run_command':
            if 'args' in locals() and args[0] == 'sclQuit()':
                handle_msg('sclQuit')
                exception_handled = True

        elif shutdown_event.is_set():
            handle_msg('shutdown_event')
            exception_handled = True

        elif not inqueue.empty() and inqueue.get_nowait() == 'terminate':
            handle_msg('terminate in queue')
            exception_handled = True

        if not exception_handled:
            print('[REPLWrapper_server_fn] exception not handled') if verbosity >= 3 else None
            try:
                print('[REPLWrapper_server_fn] {}'.format(spectre.child.before)) if verbosity >= 4 else None
            except:
                pass
            try:
                print('[REPLWrapper_server_fn] unhandled exc: {}'.format(e)) if verbosity >= 4 else None
            except:
                pass
            raise e

    finally:
        if 'try_kill' in locals():
            try_kill()
