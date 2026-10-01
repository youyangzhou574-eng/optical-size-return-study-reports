$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'd3_runner_helpers.ps1')
$runId='F0_D3_AUTOSHUTOFF_1E8_20261001_01';$root=$PSScriptRoot
$input=Join-Path $root 'F0_D3_AUTOSHUTOFF_1E8_input.fsp'
$logPath=Join-Path $root 'F0_D3_AUTOSHUTOFF_1E8_input_p0.log'
$gate=[IO.File]::ReadAllText((Join-Path $root 'launch_gate.json'))|ConvertFrom-Json
$status=Join-Path $root 'runner_status.json'
$launch=@{slot_claimed=$false;start_call_reached=$false;process_started=$false;start_outcome='NOT_CALLED'}
$tracked=$null;$mpiCode=$null;$known=@();$start=$null;$monitorFailures=0
function Write-D3Status([string]$State,[string]$Detail,[nullable[int]]$Exit=$null) {
    [ordered]@{run_id=$runId;category='DIAGNOSTIC';state=$State;detail=$Detail;server_utc=[datetime]::UtcNow.ToString('o');runner_pid=$PID;runner_created_utc=(Get-Process -Id $PID).StartTime.ToUniversalTime().ToString('o');started_server_utc=$start;process_start_call_reached=$launch.start_call_reached;solve_request_issued=$launch.start_call_reached;mpi_process_started=$launch.process_started;mpi_pid=$launch.process_id;mpi_created_utc=$launch.process_created_utc;start_outcome=$launch.start_outcome;mpi_exit_code=$mpiCode;runner_exit=$Exit;ranks=1;threads_per_rank=1;monitor_failures=$monitorFailures;automatic_retry=$false;automatic_next_case=$false;original_input_sha256=$gate.input_sha256}|ConvertTo-Json|Set-Content -LiteralPath $status -Encoding UTF8
}
function Observe-D3Native {
    try {
        $o=Get-D3NativeObservation -KnownMembers $script:known -InputFsp $input -CaseRoot $root
        foreach($p in $o.Set.Processes) {
            if($p.CreationDate -and -not @($script:known|Where-Object {$_.ProcessId -eq $p.ProcessId -and $_.CreationDate -eq $p.CreationDate -and $_.Name -eq $p.Name}).Count) {
                $script:known+=@{ProcessId=$p.ProcessId;CreationDate=$p.CreationDate;Name=$p.Name;ParentProcessId=$p.ParentProcessId}
            }
        }
        $bytes=($o.Set.Processes|Where-Object ProcessId -ne $PID|Measure-Object WorkingSetSize -Sum).Sum
        $record=@{server_utc=[datetime]::UtcNow.ToString('o');identity_uncertain=$o.Set.IdentityUncertain;case_members=$o.Set.Processes.Count;branch_gib=$bytes/1GB;free_gib=$o.FreeBytes/1GB;alarm=($bytes -gt 64GB -or $o.FreeBytes -lt 10GB -or $o.Set.IdentityUncertain);automatic_kill=$false}
        $record|ConvertTo-Json -Compress|Set-Content -LiteralPath (Join-Path $root 'native_resource_latest.json') -Encoding UTF8
        if($record.alarm){$record|ConvertTo-Json -Compress|Add-Content -LiteralPath (Join-Path $root 'native_resource_alarm_history.jsonl') -Encoding UTF8}
        return $o
    } catch {
        $script:monitorFailures++
        @{server_utc=[datetime]::UtcNow.ToString('o');error=$_.Exception.GetType().FullName;mpi_reference_retained=($null -ne $script:tracked);automatic_kill=$false}|ConvertTo-Json -Compress|Add-Content -LiteralPath (Join-Path $root 'native_monitor_failures.jsonl') -Encoding UTF8
        return $null
    }
}
try {
    Assert-D3LaunchGate $gate
    $bindings=@{ 'run_f0_d3_once.ps1'=$gate.runner_sha256;'d3_runner_helpers.ps1'=$gate.helper_sha256;'d2_runner_helpers.ps1'=$gate.d2_helper_sha256;'d1_runner_helpers.ps1'=$gate.base_helper_sha256;'human_authorization.json'=$gate.human_authorization_sha256;'settings_numeric_preflight.json'=$gate.preflight_sha256;'PRO_PLAN_CONFIRM_20261001_05.md'=$gate.pro_review_sha256;'F0_D3_AUTOSHUTOFF_1E8_input.fsp'=$gate.input_sha256}
    foreach($n in $bindings.Keys){if((Get-FileHash -LiteralPath (Join-Path $root $n)).Hash -ne $bindings[$n]){throw 'D3_BOUND_FILE_HASH_MISMATCH'}}
    $auth=[IO.File]::ReadAllText((Join-Path $root 'human_authorization.json'))|ConvertFrom-Json
    if($auth.approved -isnot [bool] -or -not $auth.approved -or $auth.run_id -ne $runId -or -not $auth.one_start_only -or $auth.source_D2_presolve_sha256 -ne $gate.source_sha256){throw 'D3_REAL_AUTHORIZATION_MISMATCH'}
    if([Security.Principal.WindowsIdentity]::GetCurrent().User.Value -ne $gate.admin_sid){throw 'D3_RUNNER_SID_MISMATCH'}
    if((Get-Item -LiteralPath $input).IsReadOnly -or (Test-Path -LiteralPath $logPath)){throw 'D3_WRITABLE_FRESH_INPUT_GATE_FAILED'}
    $task=Get-ScheduledTask -TaskName 'YYZ_OPT_SIZE_F0_D3_20261001_01'
    $expected='-NoProfile -ExecutionPolicy Bypass -File "{0}"' -f $PSCommandPath
    if($task.Actions.Arguments -ne $expected -or $task.Actions.WorkingDirectory -ne $root -or $task.Principal.LogonType -ne 'Password' -or $task.Settings.RestartCount -or @($task.Triggers|Where-Object {$null -ne $_}).Count){throw 'D3_EXACT_TASK_ACTION_CONTEXT_FAILED'}
    $null=Assert-D3FreshResources
    $license=Test-D2LicenseChild -WorkingDirectory $root -Prefix 'launch_d3'
    $license|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $root 'launch_license_redacted.json') -Encoding UTF8
    $null=Assert-D3FreshResources
    New-D1OnceMarker (Join-Path $root 'start_once.marker');$launch.slot_claimed=$true
    Write-D3Status 'SLOT_RESERVED_NO_SOLVE_REQUEST_YET' 'Reservation is not Process.Start; never remove for retry.'
    $args='-n 1 "D:\Program Files\Lumerical\v241\bin\fdtd-engine-msmpi.exe" -t 1 "{0}"' -f $input
    $tracked=Start-D2TrackedProcess -Executable 'C:\Program Files\Microsoft MPI\Bin\mpiexec.exe' -Arguments $args -WorkingDirectory $root -LogPrefix 'mpi' -EnvironmentBindings (Get-D2LicenseBindings) -StartObservation $launch
    $start=$launch.process_created_utc
    Write-D3Status 'MPI_PROCESS_STARTED' 'One actual Process.Start; running MPI exit remains null.'
    $null=Observe-D3Native
    while(-not $tracked.Process.WaitForExit(60000)){$null=Observe-D3Native}
    $mpiCode=Complete-D2TrackedProcess $tracked;$tracked=$null
    if($mpiCode -ne 0){throw ('D3_ACTUAL_MPI_EXIT_'+$mpiCode)}
    $log=[IO.File]::ReadAllText($logPath)
    if($log -notmatch '(?m)^\s*\d+(?:\.\d+)?% complete\.' -or $log -notmatch 'Completed\s+\d+\s+iterations' -or $log -notmatch 'Simulation completed successfully' -or $log -notmatch 'Finished collecting data'){throw 'D3_FRESH_COMPLETION_LOG_INCOMPLETE'}
    if((Get-Item -LiteralPath $input).LastWriteTimeUtc -lt ([datetime]$start).ToUniversalTime()){throw 'D3_NEW_RESULT_SAVE_NOT_PROVEN'}
    $o=Observe-D3Native
    if(-not $o -or $o.Set.IdentityUncertain -or @($o.Set.Processes|Where-Object ProcessId -ne $PID).Count){throw 'D3_NO_WRITER_GATE_NOT_PROVEN_NO_FREEZE'}
    $resultHash=(Get-FileHash -LiteralPath $input).Hash
    Write-D3Status 'FRESH_SOLVE_COMPLETE_AWAITING_RESULT_AUDIT' ('result_sha256='+$resultHash) 0
    exit 0
} catch {
    $failure=$_
    if(-not $tracked -and $launch.process_started){$tracked=$launch.tracked}
    if($tracked) {
        if($null -ne $tracked.ActualExitCode){$mpiCode=$tracked.ActualExitCode}
        else {
            Write-D3Status 'RUNNER_ERROR_MPI_HELD_NO_RETRY' 'MPI retained; no assertion it stopped.'
            try {
                if(-not $tracked.OutTask){$tracked.OutTask=$tracked.Process.StandardOutput.BaseStream.CopyToAsync($tracked.Stdout)}
                if(-not $tracked.ErrTask){$tracked.ErrTask=$tracked.Process.StandardError.BaseStream.CopyToAsync($tracked.Stderr)}
                while(-not $tracked.Process.WaitForExit(60000)){$null=Observe-D3Native}
                $mpiCode=Complete-D2TrackedProcess $tracked
            } catch {if($null -ne $tracked.ActualExitCode){$mpiCode=$tracked.ActualExitCode}}
        }
    }
    Write-D3Status 'FAILED_STOP_NO_RETRY' $failure.Exception.Message -1
    exit 1
}
