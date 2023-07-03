#include <windows.h>
#include <intrin.h>
#include <stdio.h>

__declspec(dllexport) unsigned long long ReadCPUTimer(void) {
    return __rdtsc();
}

__declspec(dllexport) unsigned long long GetOSTimerFreq(void)
{
	LARGE_INTEGER Freq;
	QueryPerformanceFrequency(&Freq);
	return Freq.QuadPart;
}

// rdtsc has higher resolution
// queryperformancecounter's resolution is around 10MHz
__declspec(dllexport) unsigned long long ReadOSTimer(void)
{
	LARGE_INTEGER Value;
	QueryPerformanceCounter(&Value); // it is calling rdtscp instruction
	return Value.QuadPart;
}

__declspec(dllexport) unsigned long long GetCPUFreq(void)
{
    unsigned long long cpu_start = ReadCPUTimer();
    unsigned long long os_start = ReadOSTimer();
    while(ReadOSTimer() - os_start < GetOSTimerFreq())
        continue;
    return ReadCPUTimer() - cpu_start;
}

__declspec(dllexport) void GetRTDSCCycleCount (unsigned int doprint) {
  static unsigned long long last_t = 0;

  if (last_t == 0)
       last_t = __rdtsc();

  unsigned long long curr_t = __rdtsc();

  if (doprint > 0){
    printf("Diff is %llu cycles\n", curr_t-last_t);
    fflush(stdout);
  }

  last_t = curr_t;
}