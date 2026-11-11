# Read-only checks. Disconnect VPNs before running. No credentials are used.
param([string]$ReferenceIP = "")
$targets = @(
    @{ Name = 'Singapore'; IP = '45.130.165.105' },
    @{ Name = 'Amsterdam'; IP = '185.247.117.108' }
)
if ($ReferenceIP) { $targets += @{ Name = "Reference"; IP = $ReferenceIP } }
foreach ($target in $targets) {
    $tcp = New-Object System.Net.Sockets.TcpClient
    try {
        $pending = $tcp.BeginConnect($target.IP, 443, $null, $null)
        if (-not $pending.AsyncWaitHandle.WaitOne(5000)) { throw 'TCP timeout' }
        $tcp.EndConnect($pending)
        Write-Output ($target.Name + ' TCP=OK')
    } catch {
        Write-Output ($target.Name + ' TCP=FAILED ' + $_.Exception.Message)
    } finally {
        $tcp.Dispose()
    }
    # Ordinary verified HTTPS using the same SNI, without VLESS authentication.
    & curl.exe --noproxy '*' --connect-timeout 5 --max-time 12 --silent --show-error --head --resolve ('mirror.init7.net:443:' + $target.IP) --output NUL --write-out ($target.Name + ' HTTP=%{http_code} TLSverify=%{ssl_verify_result} time=%{time_total}s\n') 'https://mirror.init7.net/'
    Write-Output ($target.Name + ' curl_exit=' + $LASTEXITCODE)
}
