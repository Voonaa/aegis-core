; Inno Setup Script for Aegis Core Platform Installation Package
; Compile this script using Inno Setup Compiler (ISCC.exe)

[Setup]
AppName=Aegis Core Platform
AppVersion=1.0.0-rc5
AppPublisher=Aegis Platform Open Source
DefaultDirName={autopf}\AegisCore
DefaultGroupName=Aegis Core Platform
UninstallDisplayIcon={app}\Aegis.bat
Compression=lzma2
SolidCompression=yes
OutputDir=..\reports\release
OutputBaseFilename=Aegis_Setup_v1.0.0-rc5
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\reports\release\aegis_v1.0.0_portable\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Aegis Core Platform"; Filename: "{app}\Aegis.bat"; IconFilename: "{app}\apps\desktop\ui\assets\icon.ico"; Flags: runminimized
Name: "{group}\{cm:UninstallProgram,Aegis Core Platform}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Aegis Core Platform"; Filename: "{app}\Aegis.bat"; IconFilename: "{app}\apps\desktop\ui\assets\icon.ico"; Tasks: desktopicon; Flags: runminimized

[Run]
Description: "{cm:LaunchProgram,Aegis Core Platform}"; Filename: "{app}\Aegis.bat"; Flags: shellexec postinstall nowait runminimized
