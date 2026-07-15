[Setup]
AppName=Aero Downloader Pro
AppVersion=1.3.6
DefaultDirName={autopf}\Aero Downloader Pro
DefaultGroupName=Aero Downloader Pro
OutputBaseFilename=AeroDownloader_Setup
OutputDir=dist
Compression=lzma2
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\AeroDownloader.exe
CloseApplications=yes
RestartApplications=no
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos adicionales:"

[Files]
Source: "dist\AeroDownloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Aero Downloader Pro"; Filename: "{app}\AeroDownloader.exe"
Name: "{autodesktop}\Aero Downloader Pro"; Filename: "{app}\AeroDownloader.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AeroDownloader.exe"; Description: "Ejecutar Aero Downloader Pro"; Flags: nowait postinstall skipifsilent
