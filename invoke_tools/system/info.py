"""
invoke_tools.system.info
"""
import cpuinfo
import psutil
import platform


class Info:
    """
    Info
    """

    def __init__(self):
        """
        """
        pass

    @staticmethod
    def print_all():
        """

        :return:
        """
        info = cpuinfo.get_cpu_info()
        kernel_info = platform.uname()
        memory_info = psutil.virtual_memory()

        output = "\n\n# System information  \n" \
                 "-------------------------------------------\n" \
                 "  Hostname :\t{0}\n" \
                 "  Processor:\t{1}\n" \
                 "  System   :\t{2}\n" \
                 "  Kernel   :\t{3} {4}\n" \
                 "  CPU Usage:\t{5}%\n" \
                 "  RAM Usage:\t{6}% of {7:.2f} GB\n" \
                 "-------------------------------------------\n\n".format(
            platform.node(),
            info['brand'],
            platform.system(),
            kernel_info.release,
            kernel_info.version,
            psutil.cpu_percent(),
            memory_info.percent,
            memory_info.total / 1073741824
        )

        print(output)
