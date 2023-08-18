$src = Read-Host -Prompt 'Source? > '
$dst = Read-Host -Prompt 'Destination? > '

Write-Output "This is a very stripped down script! Use the rsync script if at all possible."
Write-Output "Check excluded files & directories"
Write-Output "$src   to   $dst"
pause

robocopy "$src" "$dst" /bytes /ETA /V /TS /MIR /Z /MT:16 /R:2 /W:2 /XF '.Trash-1000' '.Trashes' '.fseventsd' '.Spotlight-V100' '.DS_Store' /XD 'System Volume Information' '$RECYCLE.BIN' 'venv'
