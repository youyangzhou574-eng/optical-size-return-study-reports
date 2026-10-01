. (Join-Path $PSScriptRoot 'd1_runner_helpers.ps1')
function Assert-D2LaunchGate($Gate) {
    foreach($name in @('technical_preflight_passed','human_approved','pro_preparation_review_passed','human_conditions_satisfied')) {
        if($Gate.$name -isnot [bool] -or $Gate.$name -ne $true){throw ('D2_BOOLEAN_GATE_NOT_TRUE:'+ $name)}
    }
    if($Gate.run_id -ne 'F0_D2_BOUNDARY_PAD_1CELL_20260930_01' -or $Gate.decision_id -ne 'OPT-SIZE-PRO-V11-TEXT-REVIEW-D2-PREP-20260930-20' -or $Gate.human_authorization_run_id -ne $Gate.run_id -or $Gate.ranks -ne 1 -or $Gate.threads_per_rank -ne 1 -or $Gate.input_sha256 -ne '0C21BE1CA258FE6018EA5619E5F53E6CA1A441EECF2F495BA75B9A5404BBDD3C'){throw 'D2_EXACT_RUN_TECHNICAL_OR_HUMAN_GATE_MISSING'}
    foreach($name in @('runner_sha256','helper_sha256','base_helper_sha256','human_authorization_record_sha256')) {
        if($Gate.$name -isnot [string] -or $Gate.$name -notmatch '^[A-Fa-f0-9]{64}$'){throw ('D2_BOUND_HASH_MISSING:'+ $name)}
    }
}
function New-D2ProcessInfo([string]$Executable,[string]$Arguments,[string]$WorkingDirectory,[hashtable]$EnvironmentBindings) {
    $info=New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName=$Executable;$info.Arguments=$Arguments;$info.WorkingDirectory=$WorkingDirectory
    $info.UseShellExecute=$false;$info.CreateNoWindow=$true
    $info.RedirectStandardOutput=$true;$info.RedirectStandardError=$true
    foreach($name in $EnvironmentBindings.Keys) {
        if(-not $EnvironmentBindings[$name]){throw 'EMPTY_APPROVED_ENVIRONMENT_BINDING'}
        $info.EnvironmentVariables[$name]=[string]$EnvironmentBindings[$name]
    }
    return $info
}
function Get-D2LicenseBindings {
    $route=[Environment]::GetEnvironmentVariable('ANSYSLMD_LICENSE_FILE','Machine')
    if(-not $route){throw 'EXISTING_APPROVED_LICENSE_SOURCE_MISSING'}
    return @{ANSYSLMD_LICENSE_FILE=$route}
}
function Start-D2TrackedProcess([string]$Executable,[string]$Arguments,[string]$WorkingDirectory,[string]$LogPrefix,[hashtable]$EnvironmentBindings,[hashtable]$StartObservation=@{}) {
    $info=New-D2ProcessInfo $Executable $Arguments $WorkingDirectory $EnvironmentBindings
    $StartObservation.start_call_reached=$false;$StartObservation.process_started=$false
    $StartObservation.start_outcome='NOT_CALLED'
    $stdout=$null;$stderr=$null;$process=$null
    try {
        $stdout=[IO.File]::Open((Join-Path $WorkingDirectory ($LogPrefix+'_stdout.log')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
        $stderr=[IO.File]::Open((Join-Path $WorkingDirectory ($LogPrefix+'_stderr.log')),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
        $process=New-Object System.Diagnostics.Process;$process.StartInfo=$info
        $tracked=[pscustomobject]@{Process=$process;Stdout=$stdout;Stderr=$stderr;OutTask=$null;ErrTask=$null;ActualExitCode=$null;OutputCollectionSucceeded=$false}
        $StartObservation.tracked=$tracked
        $StartObservation.start_call_reached=$true;$StartObservation.start_outcome='UNKNOWN'
        $StartObservation.start_call_utc=[datetime]::UtcNow.ToString('o')
        if(-not $process.Start()){$StartObservation.start_outcome='RETURNED_FALSE';throw 'TRACKED_PROCESS_DID_NOT_START'}
        $StartObservation.process_started=$true;$StartObservation.start_outcome='STARTED'
        $null=$process.Handle
        $StartObservation.process_id=$process.Id;$StartObservation.process_created_utc=$process.StartTime.ToUniversalTime().ToString('o')
        $tracked.OutTask=$process.StandardOutput.BaseStream.CopyToAsync($stdout)
        $tracked.ErrTask=$process.StandardError.BaseStream.CopyToAsync($stderr)
        return $tracked
    } catch {
        if(-not $StartObservation.process_started) {
            if($stdout){$stdout.Dispose()};if($stderr){$stderr.Dispose()};if($process){$process.Dispose()}
        }
        # A started process and its streams remain reachable by the caller on setup failure.
        throw
    }
}
function Complete-D2TrackedProcess($Tracked) {
    $Tracked.Process.WaitForExit()
    $rawExitCode=$Tracked.Process.get_ExitCode()
    if($null -eq $rawExitCode -or $rawExitCode -isnot [int]){throw 'ACTUAL_PROCESS_EXIT_CODE_NOT_RECORDED'}
    $Tracked.ActualExitCode=$rawExitCode
    try {
        if(-not $Tracked.OutTask -or -not $Tracked.ErrTask){throw 'D2_OUTPUT_COLLECTION_SETUP_INCOMPLETE'}
        $collectionFailure=$null
        foreach($task in @($Tracked.OutTask,$Tracked.ErrTask)) {
            try {$null=$task.GetAwaiter().GetResult()}catch{if(-not $collectionFailure){$collectionFailure=$_}}
        }
        if($collectionFailure){throw $collectionFailure}
        $Tracked.Stdout.Flush();$Tracked.Stderr.Flush()
        $Tracked.OutputCollectionSucceeded=$true
        return $Tracked.ActualExitCode
    } finally {
        $Tracked.Stdout.Dispose();$Tracked.Stderr.Dispose();$Tracked.Process.Dispose()
    }
}
function Get-D2CaseProcessSet($All,$KnownMembers,[string]$InputFsp,[string]$CaseRoot) {
    $selected=@{};$uncertain=$false
    $casePattern=[regex]::Escape($CaseRoot.TrimEnd('\'))+'(?=\\|["\s]|$)'
    foreach($p in $All) {
        $same=@($KnownMembers|Where-Object {$_.ProcessId -eq $p.ProcessId -and $_.CreationDate -and $p.CreationDate -and ([datetime]$_.CreationDate).ToUniversalTime().Ticks -eq ([datetime]$p.CreationDate).ToUniversalTime().Ticks -and $_.Name -eq $p.Name}).Count -gt 0
        if($same -or ($p.CommandLine -and ($p.CommandLine -match $casePattern -or $p.CommandLine -match ([regex]::Escape($InputFsp)+'(?=["\s]|$)')))){$selected[[int]$p.ProcessId]=$p}
    }
    do {
        $changed=$false
        foreach($p in $All) {
            $parent=$selected[[int]$p.ParentProcessId]
            if(-not $selected.ContainsKey([int]$p.ProcessId) -and $parent -and $parent.CreationDate -and $p.CreationDate -and ([datetime]$parent.CreationDate) -le ([datetime]$p.CreationDate)) {
                $selected[[int]$p.ProcessId]=$p;$changed=$true
            }
        }
    } while($changed)
    foreach($p in $All) {
        if($selected.ContainsKey([int]$p.ProcessId) -and -not $p.CreationDate){$uncertain=$true}
        if($p.Name -in @('fdtd-engine-msmpi.exe','fdtd-solutions.exe','mpiexec.exe') -and -not $selected.ContainsKey([int]$p.ProcessId)) {
            if(-not $p.CommandLine -or -not $p.CreationDate -or $p.CommandLine -notmatch '\.fsp(?=["\s]|$)'){$uncertain=$true}
        }
    }
    [pscustomobject]@{Processes=@($selected.Values);IdentityUncertain=$uncertain}
}
function Get-D2ResourceObservation($KnownMembers,[string]$InputFsp,[string]$CaseRoot,[scriptblock]$QueryProcesses={Get-CimInstance Win32_Process},[scriptblock]$QueryFreeMemory={[double](Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory*1KB}) {
    try {
        $all=@(& $QueryProcesses)
        $set=Get-D2CaseProcessSet -All $all -KnownMembers $KnownMembers -InputFsp $InputFsp -CaseRoot $CaseRoot
        $free=& $QueryFreeMemory
        [pscustomobject]@{Succeeded=$true;Set=$set;FreeBytes=$free;Error=$null}
    } catch {
        [pscustomobject]@{Succeeded=$false;Set=$null;FreeBytes=$null;Error=$_.Exception.Message}
    }
}
function Test-D2LicenseChild([string]$WorkingDirectory,[string]$Prefix) {
    $bindings=Get-D2LicenseBindings
    $code='[pscustomobject]@{present=[bool]$env:ANSYSLMD_LICENSE_FILE;matches_approved_source=($env:ANSYSLMD_LICENSE_FILE -eq [Environment]::GetEnvironmentVariable("ANSYSLMD_LICENSE_FILE","Machine"))}|ConvertTo-Json -Compress'
    $encoded=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($code))
    $p=Start-D2TrackedProcess -Executable (Join-Path $PSHOME 'powershell.exe') -Arguments ('-NoProfile -EncodedCommand '+$encoded) -WorkingDirectory $WorkingDirectory -LogPrefix ($Prefix+'_inheritance') -EnvironmentBindings $bindings
    $inheritCode=Complete-D2TrackedProcess $p
    $inherit=Get-Content -Raw -LiteralPath (Join-Path $WorkingDirectory ($Prefix+'_inheritance_stdout.log'))|ConvertFrom-Json
    if($inheritCode -ne 0 -or -not $inherit.present -or -not $inherit.matches_approved_source){throw 'D2_LICENSE_CHILD_INHERITANCE_FAILED'}
    $lmutil='D:\Program Files\Lumerical\v241\licensingclient\winx64\lmutil.exe'
    $arguments='lmstat -c "{0}" -f lumerical_solve' -f $bindings.ANSYSLMD_LICENSE_FILE
    $p=Start-D2TrackedProcess -Executable $lmutil -Arguments $arguments -WorkingDirectory $WorkingDirectory -LogPrefix ($Prefix+'_license_private') -EnvironmentBindings $bindings
    $queryCode=Complete-D2TrackedProcess $p
    $raw=Get-Content -Raw -LiteralPath (Join-Path $WorkingDirectory ($Prefix+'_license_private_stdout.log'))
    $match=[regex]::Match($raw,'Users of lumerical_solve:.*?Total of (\d+) licenses? issued;\s*Total of (\d+) licenses? in use')
    if($queryCode -ne 0 -or -not $match.Success -or ([int]$match.Groups[1].Value-[int]$match.Groups[2].Value) -lt 1){throw 'D2_LICENSE_QUERY_OR_FREE_ENTITLEMENT_FAILED'}
    [pscustomobject]@{child_variable_present=$inherit.present;child_matches_approved_source=$inherit.matches_approved_source;license_query_exit=$queryCode;licenses_issued=[int]$match.Groups[1].Value;licenses_in_use=[int]$match.Groups[2].Value;actual_solve_checkout_verified=$false;license_route_disclosed=$false}
}
