# Run as Administrator: bypass ISP DNS until akademia.quietforge propagates.
# Right-click PowerShell -> Run as administrator, then:
#   Set-ExecutionPolicy -Scope Process Bypass -Force
#   & "$PSScriptRoot\fix-akademia-dns-local.ps1"

$ErrorActionPreference = 'Stop'
$hostName = 'akademia.quietforge.flexgrafik.nl'
$ip = '185.243.54.115'
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$line = "$ip`t$hostName"

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error 'Uruchom PowerShell jako Administrator.'
}

$content = Get-Content $hostsPath -Raw
if ($content -match [regex]::Escape($hostName)) {
    Write-Host "Hosts: wpis dla $hostName juz istnieje."
} else {
    Add-Content -Path $hostsPath -Value $line -Encoding ASCII
    Write-Host "Hosts: dodano $line"
}

ipconfig /flushdns | Out-Null
Resolve-DnsName $hostName | Format-Table Name, IPAddress -AutoSize
Write-Host "Otworz: https://$hostName/DASHBOARD.html"
