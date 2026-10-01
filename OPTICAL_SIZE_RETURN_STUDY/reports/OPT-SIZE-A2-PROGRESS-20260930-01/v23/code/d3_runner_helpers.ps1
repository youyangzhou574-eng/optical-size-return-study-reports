. (Join-Path $PSScriptRoot 'd2_runner_helpers.ps1')
function Assert-D3LaunchGate($Gate) {
    foreach($name in @('technical_preflight_passed','human_approved','pro_preparation_review_passed','human_conditions_satisfied','effective_solve_gate_open')) {
        if($Gate.$name -isnot [bool] -or $Gate.$name -ne $true){throw ('D3_BOOLEAN_GATE_NOT_TRUE:'+ $name)}
    }
    if($Gate.run_id -ne 'F0_D3_AUTOSHUTOFF_1E8_20261001_01' -or $Gate.source_sha256 -ne '0C21BE1CA258FE6018EA5619E5F53E6CA1A441EECF2F495BA75B9A5404BBDD3C' -or $Gate.ranks -ne 1 -or $Gate.threads_per_rank -ne 1 -or $Gate.auto_shutoff_min -ne 1e-8 -or $Gate.maximum_time_fs -ne 2900 -or $Gate.budget_total_before -ne 4 -or $Gate.budget_diagnostic_before -ne 3 -or $Gate.pro_agent -ne '2bc88425-7a9a-41fd-ac8e-9798960c91d8'){throw 'D3_EXACT_CONFIGURATION_OR_AUTHORITY_FAILED'}
    foreach($name in @('input_sha256','runner_sha256','helper_sha256','d2_helper_sha256','base_helper_sha256','human_authorization_sha256','preflight_sha256','pro_review_sha256')) {
        if($Gate.$name -isnot [string] -or $Gate.$name -notmatch '^[A-Fa-f0-9]{64}$'){throw ('D3_BOUND_HASH_MISSING:'+ $name)}
    }
}
function Get-D3NativeObservation($KnownMembers,[string]$InputFsp,[string]$CaseRoot) {
    # CIM stays inside this dedicated native task; only primitive status goes to disk.
    $all=@(Get-CimInstance Win32_Process -OperationTimeoutSec 10|Select-Object ProcessId,ParentProcessId,CreationDate,Name,CommandLine,WorkingSetSize)
    $set=Get-D2CaseProcessSet -All $all -KnownMembers $KnownMembers -InputFsp $InputFsp -CaseRoot $CaseRoot
    $free=[double](Get-CimInstance Win32_OperatingSystem -OperationTimeoutSec 10).FreePhysicalMemory*1KB
    return @{Set=$set;FreeBytes=$free}
}
function Assert-D3FreshResources {
    $all=@(Get-CimInstance Win32_Process -Filter "Name='mpiexec.exe' OR Name='fdtd-engine-msmpi.exe' OR Name='fdtd-solutions.exe'" -OperationTimeoutSec 10)
    if($all.Count){throw 'D3_PRESTART_IDENTITY_OR_WRITER_CONFLICT'}
    $free=[double](Get-CimInstance Win32_OperatingSystem -OperationTimeoutSec 10).FreePhysicalMemory*1KB
    $disk=[double](Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='D:'" -OperationTimeoutSec 10).FreeSpace
    if(32GB -gt .7*$free -or $disk -lt 54GB){throw 'D3_PRESTART_RESOURCE_GATE_FAILED'}
    return @{free_memory_gib=$free/1GB;free_disk_gib=$disk/1GB;estimated_memory_gib=32;estimate_inherited_from_D1=$true;identity_uncertain=$false;other_optical_or_mpi_count=0}
}
