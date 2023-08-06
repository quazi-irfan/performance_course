# check if the dll and python version compiled for the same architecture
# dumpbin /exports perf.dll
# cl.exe /LD <files-to-compile>
# cl.exe /LD perf.c

# https://github.com/cmuratori/computer_enhance/blob/main/perfaware/part2/listing_0070_platform_metrics.cpp
# https://github.com/cmuratori/computer_enhance/blob/main/perfaware/part2/listing_0074_platform_metrics.cpp

import ctypes
import pathlib

c_lib = ctypes.cdll.LoadLibrary(str(pathlib.Path().absolute()) + "\\perf.dll")

c_lib.ReadCPUTimer.restype = ctypes.c_ulonglong
c_lib.GetOSTimerFreq.restype = ctypes.c_ulonglong
c_lib.ReadOSTimer.restype = ctypes.c_ulonglong
c_lib.GetCPUFreq.restype = ctypes.c_ulonglong
c_lib.GetRTDSCCycleCount.argtypes = [ctypes.c_uint]

# used by other modules; perf.get_cpu_tick()
get_cpu_freq = c_lib.GetCPUFreq
get_cpu_tick = c_lib.ReadCPUTimer

class Profiler:
    def __init__(self):
        self.cpu_freq = get_cpu_freq()
        self.blocks = {}

    def result(self):
        total_ticks = 0
        for block_name, block_measurements in self.blocks.items():
            block_ticks = (block_measurements[1] - block_measurements[0])
            block_measurements.append(block_ticks)
            total_ticks += block_ticks

        for block_name, block_measurements in self.blocks.items():
            print(block_name, str(round(block_measurements[-1]/self.cpu_freq * 1000, 2)) + ' ms; ', str(round(block_measurements[-1]/total_ticks,3)) + '%')


class ProfileBlock:
    def __init__(self, name, profiler):
        self.name = name
        self.profiler = profiler
        self.profiler.blocks[name] = []

    def __enter__(self):
        block_start = get_cpu_tick()
        self.profiler.blocks[self.name].append(block_start)

    def __exit__(self, exc_type, exc_val, exc_tb):
        block_end = get_cpu_tick()
        self.profiler.blocks[self.name].append(block_end)

if __name__ == '__main__':
    print('#1')
    for i in range(1, 50):
        last_t = c_lib.ReadCPUTimer()
        curr_t = c_lib.ReadCPUTimer()
        if not i % 5:
            print('Diff is ' + str(curr_t - last_t) + ' cycles')
        last_t = curr_t

    print('#2')
    for i in range(1, 50):
        if not i % 5:
            c_lib.GetRTDSCCycleCount(1)
        else:
            c_lib.GetRTDSCCycleCount(0)

    print('#3')
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)

    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)

    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)

    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)

    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(0)
    c_lib.GetRTDSCCycleCount(1)

    exit()

# Each CPU core see different clock speed
# rdtsc represented number of clocks elapsed
# rdtsc is not invarient tsd(time stamp counter)
# it still counts up, but it is invariant of the individual cpu clock
# All core sees the same rdtsc even if some of them are sleeping
# problem is rdtsc do not count cycles anymore
# rdtsc is counting up the base frequency of the processor; so it is in the order of cycle
# right now it is very precise wall clock; goes up by at a constant rate

# We can use other instruction to count actual cycles; but those instructions are not always available in all chips, and all OS

# rtdsc is a counter going up at constant time, but we needs to be converted to wall clock
# There is no way to obtain the cpu frequency from an instruction
# wmic cpu get name, maxclockspeed, currentclockspeed
# 2304               2304           Intel(R) Core(TM) i5-8300H CPU @ 2.30GHz
# systeminfo | findstr "Intel64"

# We count number of elapsed rtdsc cycles in a known duration to find the cpu frequency
# os timer can procide known duration
# queryperformancecounter - high resolution known wall clock counter

# https://learn.microsoft.com/en-us/windows/win32/api/profileapi/
# get the frequency of the OS Timer;
# it could just be a constant if you know the resolution of the OS time; Linux returns a microsecond OS counter;
#   So this function can return 1_000_000 constant
# print(c_lib.GetOSTimerFreq()) # performance counter frequency per second
#
# # read the current value of OS Timer
# print(c_lib.ReadOSTimer())
#
# print(c_lib.ReadCPUTimer()) # return the number of clock cycle since CPU startup

# timer_freq = c_lib.GetOSTimerFreq()
# cpu_start = c_lib.ReadCPUTimer()
# os_start = c_lib.ReadOSTimer()
#
# os_elapsed = 0
# # while os_elapsed < timer_freq:
# #     os_elapsed = c_lib.ReadOSTimer() - os_start
#
#
# while os_elapsed < timer_freq:
#     os_elapsed += c_lib.ReadOSTimer() - os_start
#     os_start = c_lib.ReadOSTimer()
#
# # while c_lib.ReadOSTimer() - os_start < timer_freq:
# #     pass
#
# cpu_elapsed = c_lib.ReadCPUTimer() - cpu_start
# print(cpu_elapsed)
