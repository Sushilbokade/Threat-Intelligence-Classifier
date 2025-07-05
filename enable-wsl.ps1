# Enable Windows features required for Docker Desktop and WSL2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Download the WSL2 Linux kernel update package
$wslUpdateUrl = "https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi"
$wslUpdateFile = "$env:TEMP\wsl_update_x64.msi"
Invoke-WebRequest -Uri $wslUpdateUrl -OutFile $wslUpdateFile

# Install the WSL2 Linux kernel update package
Start-Process msiexec.exe -ArgumentList "/I $wslUpdateFile /quiet" -Wait

# Set WSL2 as the default version
wsl --set-default-version 2

Write-Host "Please restart your computer to complete the setup, then try running Docker Desktop again."
