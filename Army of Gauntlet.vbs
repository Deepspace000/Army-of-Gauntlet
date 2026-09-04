' ------------------------------------------------------------------
'  Army of Gauntlet launcher (double-click this, or the desktop shortcut)
'  1. Closes every Chrome process. Chrome's gamepad helper can get stuck and
'     it lives on in Chrome's background processes, so a clean kill is the
'     only way to be sure the controller is picked up.
'  2. Waits until they are really gone.
'  3. Opens the game in its own Chrome app window.
'  Runs silently - no console window. Note: this closes ALL Chrome windows;
'  Chrome's session restore brings the tabs back next time you open it.
' ------------------------------------------------------------------
Option Explicit
Dim sh, fso, wmi, procs, i, chrome, here, game
Set sh  = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
here = fso.GetParentFolderName(WScript.ScriptFullName)

sh.Run "taskkill /F /IM chrome.exe", 0, True

Set wmi = GetObject("winmgmts:\\.\root\cimv2")
For i = 1 To 20
  Set procs = wmi.ExecQuery("SELECT ProcessId FROM Win32_Process WHERE Name='chrome.exe'")
  If procs.Count = 0 Then Exit For
  WScript.Sleep 500
Next

chrome = sh.ExpandEnvironmentStrings("%ProgramFiles%") & "\Google\Chrome\Application\chrome.exe"
If Not fso.FileExists(chrome) Then chrome = sh.ExpandEnvironmentStrings("%ProgramFiles(x86)%") & "\Google\Chrome\Application\chrome.exe"

game = "file:///" & Replace(Replace(here, "\", "/"), " ", "%20") & "/army_of_gauntlet.html"

If fso.FileExists(chrome) Then
  sh.Run """" & chrome & """ --new-window --app=""" & game & """", 1, False
Else
  sh.Run """" & here & "\rmy_of_gauntlet.html""", 1, False
End If
