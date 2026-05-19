Set objFSO = CreateObject("Scripting.FileSystemObject")
strDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run Chr(34) & strDir & "\.venv\Scripts\pythonw.exe" & Chr(34) & " " & Chr(34) & strDir & "\main.py" & Chr(34), 0, False
