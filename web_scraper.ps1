$FILES_FOLDER = "C:\Users\lecca\Downloads\LinateRunwayRunWebpages\"
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Ensure the output directory exists
if (-not (Test-Path -Path $FILES_FOLDER)) {
    New-Item -ItemType Directory -Force -Path $FILES_FOLDER
}

$start = 2568
$end = 2572

for ($i = $start; $i -le $end; $i++) {
    $url = "https://www.endu.net/en/events/milano-linate-runway-run/results/2024/92161/$i"
    $outputFile = Join-Path -Path $FILES_FOLDER -ChildPath "$i.html"
    
    # Start Chrome in headless mode and redirect output
    Start-Process -FilePath $chromePath -ArgumentList "--headless", "--disable-gpu", "--dump-dom", $url -RedirectStandardOutput $outputFile -NoNewWindow -Wait
    
    if (Test-Path -Path $outputFile) {
        Write-Host "Downloaded page $i"
    } else {
        Write-Host "Failed to download page $i"
    }
}