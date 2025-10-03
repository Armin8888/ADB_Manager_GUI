;--------------------------------
; نصب‌کننده ADB Manager GUI
;--------------------------------

!include "MUI2.nsh"

!define APP_NAME "ADB Manager GUI"
!define EXE_NAME "ADB_Manager_GUI.exe"
!define INSTALL_DIR "$PROGRAMFILES\${APP_NAME}"

;--------------------------------
; اطلاعات پایه
;--------------------------------
Name "${APP_NAME}"
OutFile "ADB_Manager_GUI_Installer.exe"
InstallDir "${INSTALL_DIR}"
ShowInstDetails show
ShowUninstDetails show

;--------------------------------
; صفحات نصب
;--------------------------------
Page directory
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------
; بخش نصب
;--------------------------------
Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\${EXE_NAME}"

  ; شورتکات روی دسکتاپ
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"

  ; شورتکات در منوی استارت
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${EXE_NAME}"

  ; فایل Uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

;--------------------------------
; بخش حذف نصب
;--------------------------------
Section "Uninstall"
  Delete "$INSTDIR\${EXE_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  RMDir  "$SMPROGRAMS\${APP_NAME}"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir  "$INSTDIR"
SectionEnd
