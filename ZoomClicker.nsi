; BFMWAconverter.nsi
;
; This script is based on example2.nsi. It remembers the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install BFMWAconverter.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "ZoomClicker"

; The file to write
OutFile "install_ZoomClicker.exe"

; The default installation directory
InstallDir $PROGRAMFILES\ZoomClicker

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\ZoomClicker" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "ZoomClicker"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put files there
  File /nonfatal /a /r "dist\ZoomClicker\"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\BFMWAconverter "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ZoomClicker" "DisplayName" "ZoomClicker"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ZoomClicker" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ZoomClicker" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ZoomClicker" "NoRepair" 1
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"
  SetShellVarContext all
  CreateDirectory "$SMPROGRAMS\ZoomClicker"
  CreateShortcut "$SMPROGRAMS\ZoomClicker\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortcut "$SMPROGRAMS\ZoomClicker\ZoomClicker.lnk" "$INSTDIR\ZoomClicker.exe" "" "$INSTDIR\ZoomClicker.exe" 0 
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  SetShellVarContext all
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ZoomClicker"
  DeleteRegKey HKLM SOFTWARE\ZoomClicker

  ; Remove files and uninstaller
  Delete "$INSTDIR\*.*"
  RMDir /r "$INSTDIR\docx\"
  RMDir /r "$INSTDIR\include\"
  RMDir /r "$INSTDIR\lib2to3\"
  RMDir /r "$INSTDIR\lxml\"
  RMDir /r "$INSTDIR\numpy\"
  RMDir /r "$INSTDIR\pandas\"
  RMDir /r "$INSTDIR\PyQt5\" 
  RMDir /r "$INSTDIR\pytz\"
  
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\ZoomClicker\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\ZoomClicker\"
  RMDir "$INSTDIR"

SectionEnd
