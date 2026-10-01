param([Parameter(Mandatory=$true)][string]$OutputRoot,[int]$PriorHostPid,[string]$PriorHostBirth)
$ErrorActionPreference='Stop';$ss=$null;$r=$null
$bootstrap=(Get-Content -LiteralPath 'E:\open\tmp\probe_existing_winrm_20260928.ps1' -TotalCount 8)-join [Environment]::NewLine
. ([scriptblock]::Create($bootstrap));$credentialText=$null;$password=$null
try {
    $ss=New-PSSession -ComputerName $serverAddress -Credential $credential -SessionOption (New-PSSessionOption -ProxyAccessType NoProxyServer -OpenTimeout 10000 -OperationTimeout 20000)
    $json=Invoke-Command -Session $ss -ArgumentList $PriorHostPid,$PriorHostBirth -ScriptBlock {
        param($priorPid,$priorBirth)
        $ErrorActionPreference='Stop'
        $result=@{operation='D3_PRIMITIVE_STATUS_READ';server_utc=[datetime]::UtcNow.ToString('o');remote_host_pid=$PID;remote_host_created_utc=(Get-Process -Id $PID).StartTime.ToUniversalTime().ToString('o');query_ok=$false;error=$null;new_solver_starts=0;active_code_modified=$false;native_case_scope_record_invalid=$true}
        function Read-SharedText([string]$Path,[int]$Limit) {
            $stream=[IO.File]::Open($Path,[IO.FileMode]::Open,[IO.FileAccess]::Read,([IO.FileShare]::ReadWrite -bor [IO.FileShare]::Delete))
            $reader=$null
            try{$reader=[IO.StreamReader]::new($stream);$buf=New-Object char[] $Limit;$n=$reader.Read($buf,0,$Limit);return [string]::new($buf,0,$n)}finally{if($reader){$reader.Dispose()}else{$stream.Dispose()}}
        }
        try {
            $prior=Get-CimInstance Win32_Process -Filter ('ProcessId='+[int]$priorPid) -OperationTimeoutSec 5
            if($prior -and $prior.CreationDate.ToUniversalTime().ToString('o') -eq $priorBirth){throw 'D3_PRIOR_SHORT_REMOTE_HOST_NOT_GONE_NO_NEXT_READ'}
            $result.prior_host_gone=$true
            $root='D:\yyz\optical_size_return_20260928\A2\F0_D3_AUTOSHUTOFF_TEST\run01'
            $inputFsp=Join-Path $root 'F0_D3_AUTOSHUTOFF_1E8_input.fsp'
            $result.runner=(Read-SharedText (Join-Path $root 'runner_status.json') 8192)|ConvertFrom-Json
            $task=Get-ScheduledTask -TaskName 'YYZ_OPT_SIZE_F0_D3_20261001_01'
            $result.task_state=[string]$task.State;$result.task_result=(Get-ScheduledTaskInfo -TaskName $task.TaskName).LastTaskResult
            $engines=@(Get-CimInstance Win32_Process -Filter "Name='fdtd-engine-msmpi.exe'" -OperationTimeoutSec 5)
            $exact=@();foreach($engine in $engines) {
                if($engine.CommandLine -and $engine.CommandLine -match ([regex]::Escape($inputFsp)+'(?=["\s]|$)')) {
                    $exact+=@{pid=[int]$engine.ProcessId;parent_pid=[int]$engine.ParentProcessId;created_utc=$engine.CreationDate.ToUniversalTime().ToString('o');cpu_seconds=([double]$engine.KernelModeTime+[double]$engine.UserModeTime)/1e7;engine_memory_gib=[double]$engine.WorkingSetSize/1GB;exact_input_argument_matched=$true}
                }
            }
            $result.exact_d3_engine_count=$exact.Count;$result.exact_d3_engines=$exact;$result.other_fdtd_engine_count=$engines.Count-$exact.Count
            $log=Join-Path $root 'F0_D3_AUTOSHUTOFF_1E8_input_p0.log';$result.latest_progress=$null
            if(Test-Path -LiteralPath $log){$text=Read-SharedText $log 65536;foreach($line in ($text -split '\r?\n')){if($line -match '^\s*\d+(\.\d+)?% complete\.'){ $result.latest_progress=[string]$line }};$result.log_bytes=(Get-Item -LiteralPath $log).Length}
            $result.stderr_bytes=(Get-Item -LiteralPath (Join-Path $root 'mpi_stderr.log')).Length
            $result.query_ok=$true
        } catch {$result.error=$_.Exception.Message}
        $json=$result|ConvertTo-Json -Depth 6 -Compress
        if($json.Length -gt 8192){throw 'D3_READER_PRIMITIVE_RESPONSE_EXCEEDS_LIMIT'}
        $json
    }
    if($json -isnot [string] -or $json.Length -gt 8192){throw 'D3_READER_NON_PRIMITIVE_RESPONSE'}
    $r=$json|ConvertFrom-Json
    [IO.File]::WriteAllText((Join-Path $OutputRoot 'receipt.json'),$json,[Text.UTF8Encoding]::new($false))
} catch {
    @{client_utc=[datetime]::UtcNow.ToString('o');error=$_.Exception.Message;remote_host_identity_unknown=$true;automatic_retry=$false;new_solver_starts=0}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $OutputRoot 'error.json') -Encoding UTF8
    exit 1
} finally {
    if($ss){Remove-PSSession $ss}
    @{client_utc=[datetime]::UtcNow.ToString('o');local_session_closed=($null -eq $ss -or $ss.State.ToString() -eq 'Closed');remote_host_pid=if($r){$r.remote_host_pid}else{$null};remote_host_created_utc=if($r){$r.remote_host_created_utc}else{$null};remote_exit_independently_verified=$false}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $OutputRoot 'session_closed.json') -Encoding UTF8
}
