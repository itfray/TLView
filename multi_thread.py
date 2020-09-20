import psutil
import threading

class MultiThread:
    """ Provides functionality for parallelizing the work of methods of other classes. """
    __MAX_COUNT_THREADS = psutil.cpu_count() - 1 if psutil.cpu_count() else 1       # calculate count logical cpus
    def __init__(self):
        self.__threads = []             # list of active threads

    def max_count_threads(self)-> int:
        return self.__MAX_COUNT_THREADS

    def remove_dead_threads(self):
        """ Removes all thread that finished work """
        dead_threads = [thread for thread in self.__threads if not thread.is_alive()]
        for thread in dead_threads:
            self.__threads.remove(thread)

    def run_thread(self, func, *args)-> bool:
        """ Runs a function on a new thread.
            return:
               False - cannot be started since the number
                       of threads is equal to the number of logical cores
               True - function run in new thread"""
        if len(self.__threads) < self.max_count_threads():
            thread = threading.Thread(target=func, args=args, daemon=True)
            thread.work_function = func
            thread.work_args = args
            self.__threads.append(thread)
            thread.start()
            return True
        return False

    def find_args_not_in_threads(self, func, *args)-> list:
        """ The function looks for arguments that
            are not currently calculated by other threads."""
        not_in_work = []         # arguments not involved in settlement
        # prepare list threads that work with func
        threads = [thread for thread in self.__threads if thread.work_function == func]
        for arg in args:
            flag = True
            for thread in threads:
                if arg in thread.work_args:
                    flag = False
                    break
            if flag:
                not_in_work.append(arg)
        return not_in_work