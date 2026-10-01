function New-D1OnceMarker([string]$Path) {
    $stream=[IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    $stream.Dispose()
}
function Get-D1ProcessFamily($All,[int[]]$RootIds) {
    $ids=@($RootIds | Select-Object -Unique)
    do {
        $previous=$ids.Count
        $ids=@($ids + @($All | Where-Object {$_.ParentProcessId -in $ids} | ForEach-Object {[int]$_.ProcessId}) | Select-Object -Unique)
    } while($ids.Count -gt $previous)
    return $ids
}
function Start-D1TrackedProcess([string]$Executable,[string]$Arguments,[string]$WorkingDirectory,[string]$LogPrefix) {
    $info=New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName=$Executable
    $info.Arguments=$Arguments
    $info.WorkingDirectory=$WorkingDirectory
    $info.UseShellExecute=$false
    $info.CreateNoWindow=$true
    $info.RedirectStandardOutput=$true
    $info.RedirectStandardError=$true
    $stdout=[IO.File]::Open((Join-Path $WorkingDirectory ($LogPrefix+'_stdout.log')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
    $stderr=[IO.File]::Open((Join-Path $WorkingDirectory ($LogPrefix+'_stderr.log')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
    $process=New-Object System.Diagnostics.Process
    $process.StartInfo=$info
    if(-not $process.Start()){throw 'TRACKED_PROCESS_DID_NOT_START'}
    $null=$process.Handle
    $outTask=$process.StandardOutput.BaseStream.CopyToAsync($stdout)
    $errTask=$process.StandardError.BaseStream.CopyToAsync($stderr)
    [pscustomobject]@{Process=$process;Stdout=$stdout;Stderr=$stderr;OutTask=$outTask;ErrTask=$errTask}
}
function Complete-D1TrackedProcess($Tracked) {
    $Tracked.Process.WaitForExit()
    $null=$Tracked.OutTask.GetAwaiter().GetResult()
    $null=$Tracked.ErrTask.GetAwaiter().GetResult()
    $Tracked.Stdout.Flush();$Tracked.Stderr.Flush()
    $code=$Tracked.Process.ExitCode
    if($null -eq $code){throw 'ACTUAL_PROCESS_EXIT_CODE_NOT_RECORDED'}
    $Tracked.Stdout.Dispose();$Tracked.Stderr.Dispose()
    return [int]$code
}
