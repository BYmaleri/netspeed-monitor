; NetSpeed Monitor - Inno Setup Script
; Inno Setup 6+ gerektirir: https://jrsoftware.org/isinfo.php

#define AppName    "NetSpeed Monitor"
#define AppVersion "1.0.0"
#define AppPublisher "NetSpeed Monitor"
#define AppURL     "https://github.com/KULLANICI_ADINIZ/netspeed-monitor"
#define AppExe     "NetSpeedMonitor.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}/releases
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=installer\output
OutputBaseFilename=NetSpeedMonitor_Setup_v{#AppVersion}
SetupIconFile=assets\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#AppExe}
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=none

[Languages]
Name: "turkish";   MessagesFile: "compiler:Languages\Turkish.isl"
Name: "english";   MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaüstüne kısayol oluştur"; GroupDescription: "Ek kısayollar:"; Flags: unchecked
Name: "startuprun";  Description: "Windows başlangıcında otomatik çalıştır"; GroupDescription: "Başlangıç:"; Flags: unchecked

[Files]
Source: "dist\{#AppExe}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}";       Filename: "{app}\{#AppExe}"
Name: "{group}\Kaldır";           Filename: "{uninstallexe}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Registry]
; Başlangıçta otomatik çalıştır (kullanıcı seçtiyse)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
  ValueType: string; ValueName: "NetSpeedMonitor"; \
  ValueData: """{app}\{#AppExe}"""; \
  Tasks: startuprun; Flags: uninsdeletevalue

[Run]
; Kurulum bittikten sonra başlat
Filename: "{app}\{#AppExe}"; Description: "NetSpeed Monitor'ı şimdi başlat"; \
  Flags: nowait postinstall skipifsilent

[UninstallRun]
; Kaldırırken çalışan uygulamayı kapat
Filename: "taskkill.exe"; Parameters: "/f /im {#AppExe}"; Flags: runhidden; \
  RunOnceId: "KillApp"
