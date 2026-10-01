$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'd3_reader_helpers.ps1')
$case='E:\open\optical_size_return_20260928\evidence\a2_preflight_20260930\F0_D3_autoshutoff_20261001'
$root=Join-Path $case 'status_reads';New-Item -ItemType Directory -Path $root -Force|Out-Null
$lock=[IO.File]::Open((Join-Path $root 'controller.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
try {
    $pendingPath=Join-Path $root 'pending.json';$prior=$null
    if(Test-Path -LiteralPath $pendingPath) {
        $pending=[IO.File]::ReadAllText($pendingPath)|ConvertFrom-Json
        $p=Get-Process -Id $pending.worker_pid -ErrorAction SilentlyContinue
        $same=$false;if($p){try{$same=($p.StartTime.ToUniversalTime().ToString('o') -eq $pending.worker_created_utc)}catch{$same=$null}}
        $unknown=Test-Path -LiteralPath (Join-Path $pending.directory 'error.json')
        $disposition=Get-D3ReaderDisposition ([bool]$p) $same $unknown
        if($disposition -ne 'MAY_START_ONE_BOUNDED_READER'){ $disposition;exit 0 }
        $receipt=Join-Path $pending.directory 'receipt.json'
        if(-not(Test-Path -LiteralPath $receipt)){throw 'D3_PREVIOUS_READER_NO_RECEIPT_BLOCK_NEW_REQUEST'}
        $prior=[IO.File]::ReadAllText($receipt)|ConvertFrom-Json
        if(-not $prior.query_ok){'D3_PRIOR_READER_QUERY_FAILED_NO_AUTOMATIC_RETRY';exit 0}
        $elapsed=([datetime]::UtcNow-([datetime]$pending.started_client_utc).ToUniversalTime()).TotalMinutes
        if($elapsed -lt 20){'D3_RECENT_READ_NO_ADDITIONAL_REMOTE_REQUEST';exit 0}
    } else {
        $prior=[IO.File]::ReadAllText((Join-Path $case 'runtime01\launch_observation.json'))|ConvertFrom-Json
    }
    $dir=Join-Path $root ([datetime]::UtcNow.ToString('yyyyMMddTHHmmssfff')+'_'+[guid]::NewGuid().ToString('N').Substring(0,6))
    New-Item -ItemType Directory -Path $dir|Out-Null
    $info=[Diagnostics.ProcessStartInfo]::new()
    $info.FileName=Join-Path $PSHOME 'powershell.exe';$info.UseShellExecute=$false;$info.CreateNoWindow=$true
    $info.Arguments='-NoProfile -ExecutionPolicy Bypass -File "{0}" -OutputRoot "{1}" -PriorHostPid {2} -PriorHostBirth "{3}"' -f (Join-Path $PSScriptRoot 'read_f0_d3_worker.ps1'),$dir,$prior.remote_host_pid,$prior.remote_host_created_utc
    $worker=[Diagnostics.Process]::new();$worker.StartInfo=$info
    if(-not $worker.Start()){throw 'D3_LOCAL_READER_START_FAILED'}
    $null=$worker.Handle
    @{worker_pid=$worker.Id;worker_created_utc=$worker.StartTime.ToUniversalTime().ToString('o');directory=$dir;started_client_utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath $pendingPath -Encoding UTF8
    if(-not $worker.WaitForExit(25000)){'D3_READER_TIMEOUT_PENDING_PROCESS_HELD_NO_KILL_NO_NEW_REQUEST';exit 0}
    $exit=$worker.get_ExitCode()
    if($null -eq $exit -or $exit -isnot [int]){throw 'D3_LOCAL_READER_EXIT_UNKNOWN_NO_NEW_REQUEST'}
    if($exit -ne 0){'D3_READER_FAILED_SEE_PENDING_ERROR_NO_RETRY';exit 0}
    $text=[IO.File]::ReadAllText((Join-Path $dir 'receipt.json'))
    if($text.Length -gt 8192){throw 'D3_LOCAL_RECEIPT_SIZE_LIMIT_FAILED'}
    $text
} finally {$lock.Dispose()}
