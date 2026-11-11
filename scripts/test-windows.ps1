# Local SOCKS-only REALITY test. Disable Happ/other VPNs before running.
$ErrorActionPreference = 'Stop'
$root = $env:VPN_TEST_ROOT
$exe = Join-Path $root '.artifacts\windows-xray\xray.exe'
foreach ($name in @('singapore', 'amsterdam')) {
    $config = Join-Path $root ('.secrets\windows-' + $name + '.json')
    $stdout = Join-Path $root ('.secrets\windows-' + $name + '.out.log')
    $stderr = Join-Path $root ('.secrets\windows-' + $name + '.err.log')
    $process = $null
    try {
        if (Get-NetTCPConnection -LocalPort 10818 -State Listen -ErrorAction SilentlyContinue) {
            throw 'Port 10818 is occupied; test did not start.'
        }
        $process = Start-Process -FilePath $exe -ArgumentList @('run', '-config', ('"' + $config + '"')) -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr
        Start-Sleep -Seconds 2
        $process.Refresh()
        if ($process.HasExited) { throw ('Xray exited; diagnostic log: ' + $stderr) }
        Write-Output ('TEST ' + $name + ' Xray 26.11.9, REALITY, SOCKS only')
        $savedNoProxy = $env:NO_PROXY
        $env:NO_PROXY = ''
        & curl.exe --proxy 'socks5h://127.0.0.1:10818' --connect-timeout 10 --max-time 25 --silent --show-error 'https://api.ipify.org'
        $curlCode = $LASTEXITCODE
        $env:NO_PROXY = $savedNoProxy
        Write-Output (' curl_exit=' + $curlCode)
    } catch {
        Write-Output ('TEST ' + $name + ' ERROR: ' + $_.Exception.Message)
    } finally {
        if ($null -ne $process) {
            $process.Refresh()
            if (-not $process.HasExited) { Stop-Process -Id $process.Id -ErrorAction SilentlyContinue }
        }
    }
}
