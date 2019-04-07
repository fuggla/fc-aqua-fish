; Aqua Fish installation script
; Requires a self-extracting 7z sfx named fc-aqua-fish-data.exe
; It should contain the following
; - Cleaned version of aqua fish (no _pycache, .idea etc)
; - python environment 3.7 in subfolder dist

SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.
datadir := A_AppData . "\aqua-fish"
mainpy := datadir . "\main.py"

; Install
if !FileExist(mainpy) {
	MsgBox, 4, Aqua Fish, Do you want to install Aqua Fish?
	IfMsgBox Yes
		{
		fileCreateDir, %datadir%
		FileInstall, fc-aqua-fish-data.exe, %datadir%\fc-aqua-fish-data.exe
		SetWorkingDir % datadir
		runWait % "fc-aqua-fish-data.exe -y -o`" datadir `""
		MsgBox, , Aqua Fish, Installation completed. Starting Aqua Fish!
	}
}

; Run
if FileExist(mainpy) {
	SetWorkingDir % datadir
	run dist\pythonw.exe main.py, %datadir%
}