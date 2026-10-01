$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'd3_runner_helpers.ps1')
$g=@{run_id='F0_D3_AUTOSHUTOFF_1E8_20261001_01';technical_preflight_passed=$true;human_approved=$true;pro_preparation_review_passed=$true;human_conditions_satisfied=$true;effective_solve_gate_open=$true;source_sha256='0C21BE1CA258FE6018EA5619E5F53E6CA1A441EECF2F495BA75B9A5404BBDD3C';input_sha256=('A'*64);runner_sha256=('B'*64);helper_sha256=('C'*64);d2_helper_sha256=('D'*64);base_helper_sha256=('E'*64);human_authorization_sha256=('F'*64);preflight_sha256=('1'*64);pro_review_sha256=('2'*64);ranks=1;threads_per_rank=1;auto_shutoff_min=1e-8;maximum_time_fs=2900;budget_total_before=4;budget_diagnostic_before=3;pro_agent='2bc88425-7a9a-41fd-ac8e-9798960c91d8'}
Assert-D3LaunchGate $g
$tests=1
foreach($name in @('technical_preflight_passed','human_approved','pro_preparation_review_passed','human_conditions_satisfied','effective_solve_gate_open')) {
    foreach($invalid in @($false,$null,'true',1)) {$copy=$g.Clone();$copy[$name]=$invalid;$rejected=$false;try{Assert-D3LaunchGate $copy}catch{$rejected=$true};if(-not $rejected){throw 'D3_FALSE_OR_NONBOOL_ACCEPTED'};$tests++}
}
foreach($change in @(@{ranks=2},@{maximum_time_fs=5800},@{auto_shutoff_min=1e-7},@{budget_total_before=5},@{input_sha256=''},@{source_sha256=('0'*64)},@{pro_agent='old-confirmation'})) {
    $copy=$g.Clone();foreach($k in $change.Keys){$copy[$k]=$change[$k]};$rejected=$false;try{Assert-D3LaunchGate $copy}catch{$rejected=$true};if(-not $rejected){throw 'D3_CONFIGURATION_MISMATCH_ACCEPTED'};$tests++
}
'D3_LAUNCH_GUARD_TESTS_PASSED='+$tests
