' ===================================================================
' Zigbee Device Programmer Silent Launcher (VBScript)
' Runs the application without showing a console window
' Perfect for desktop shortcuts and clean user experience
' ===================================================================

Option Explicit

Dim objShell, objFSO, scriptDir, pythonCmd, result

' Create objects
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory
objShell.CurrentDirectory = scriptDir

' Check if Python is available
On Error Resume Next
result = objShell.Run("python --version", 0, True)
On Error GoTo 0

If result <> 0 Then
    ' Python not found - show error and offer installation
    MsgBox "Python is not installed or not in PATH!" & vbCrLf & vbCrLf & _
           "To install Python automatically:" & vbCrLf & _
           "• Double-click: install_python_runner.bat" & vbCrLf & vbCrLf & _
           "Or install manually from:" & vbCrLf & _
           "• https://www.python.org/downloads/" & vbCrLf & _
           "• Make sure to check 'Add Python to PATH'", _
           vbCritical, "Zigbee Device Programmer - Python Required"
    WScript.Quit 1
End If

' Check if zigbee_programmer.py exists
If Not objFSO.FileExists(objFSO.BuildPath(scriptDir, "zigbee_programmer.py")) Then
    MsgBox "zigbee_programmer.py not found!" & vbCrLf & vbCrLf & _
           "Please ensure this launcher is in the same directory as zigbee_programmer.py", _
           vbCritical, "Zigbee Device Programmer - File Not Found"
    WScript.Quit 1
End If

' Run the Python application silently (no console window)
' Use Run with window style 0 (hidden) to prevent console window
pythonCmd = "python """ & objFSO.BuildPath(scriptDir, "zigbee_programmer.py") & """"

On Error Resume Next
result = objShell.Run(pythonCmd, 0, True)
On Error GoTo 0

' Handle any errors
If result <> 0 Then
    MsgBox "The Zigbee Device Programmer exited with an error." & vbCrLf & vbCrLf & _
           "Error code: " & result & vbCrLf & vbCrLf & _
           "Possible solutions:" & vbCrLf & _
           "• Check that Simplicity Commander is installed" & vbCrLf & _
           "• Verify device connections and permissions" & vbCrLf & _
           "• Try running as Administrator" & vbCrLf & _
           "• See PERMISSION_GUIDE.md for help", _
           vbExclamation, "Zigbee Device Programmer"
End If

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing

WScript.Quit result