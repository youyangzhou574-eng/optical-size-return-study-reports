function Get-D3ReaderDisposition([bool]$ProcessExists,$SameIdentity,[bool]$RemoteUnknown) {
    if($ProcessExists -and $null -eq $SameIdentity){return 'UNKNOWN_BLOCK_NEW_REQUEST'}
    if($ProcessExists -and $SameIdentity){return 'LIVE_BLOCK_NEW_REQUEST'}
    if($RemoteUnknown){return 'REMOTE_UNKNOWN_BLOCK_NEW_REQUEST'}
    return 'MAY_START_ONE_BOUNDED_READER'
}
