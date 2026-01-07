# sync.ps1
$map = @{
  "111.txt"  = "C:\Users\LOQ\Downloads\"
}

foreach ($src in $map.Keys) {
  robocopy "$PSScriptRoot\" $($map[$src]) $src /XO /R:3 /W:5
  # XO = eXclude Older
  # R:n = number of Retries
    # W:n = Wait time between retries
}
robocopy "$PSScriptRoot\minescript" "$PSScriptRoot\remote_minescript" *.* /MIR /R:3 /W:5
# MIR = MIRror (make destination exactly match source)