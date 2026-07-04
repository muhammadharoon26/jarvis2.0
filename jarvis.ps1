param (
    [string]$workspaceName = "Default Workspace",
    [string]$configPath = "workspace.json",
    [string]$logPath = "jarvis.log"
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $logLine = "[$timestamp] [$Level] $Message"
    Write-Host $logLine
    Out-File -FilePath $logPath -InputObject $logLine -Append -Encoding UTF8
}

Write-Log "======================================================"
Write-Log "INITIALIZING JARVIS SEQUENCE: '$workspaceName'" "START"

if (-Not (Test-Path $configPath)) {
    Write-Log "Configuration file missing at: $configPath" "FATAL"
    exit
}

$allConfig = Get-Content $configPath -Raw | ConvertFrom-Json
$config = $allConfig.$workspaceName

if ($null -eq $config) {
    Write-Log "Configuration for workspace '$workspaceName' not found inside JSON." "FATAL"
    exit
}

Write-Log "--- Processing Folders ---"
foreach ($folder in $config.folders) {
    try {
        $cleanFolder = $folder.Trim('"')
        if (Test-Path $cleanFolder) {
            Start-Process "explorer.exe" -ArgumentList "`"$cleanFolder`"" -ErrorAction Stop
            Write-Log "Opened Folder: $cleanFolder" "SUCCESS"
        } else {
            Write-Log "Folder path does not exist: $cleanFolder" "WARN"
        }
    } catch {
        Write-Log "Failed to open folder $cleanFolder - $($_.Exception.Message)" "ERROR"
    }
}

Write-Log "--- Processing Websites ---"
foreach ($url in $config.urls) {
    try {
        $cleanUrl = $url.Trim('"')
        Start-Process $cleanUrl -ErrorAction Stop
        Write-Log "Launched URL: $cleanUrl" "SUCCESS"
    } catch {
        Write-Log "Failed to launch URL $cleanUrl - $($_.Exception.Message)" "ERROR"
    }
}

Write-Log "--- Processing Applications ---"
foreach ($app in $config.apps) {
    try {
        $cleanAppPath = $app.path.Trim('"')
        if (Test-Path $cleanAppPath) {
            $cleanArgs = if ($app.args) { $app.args.Trim('"') } else { "" }
            $psParams = @{ FilePath = $cleanAppPath; ErrorAction = "Stop" }
            
            if (-not [string]::IsNullOrWhiteSpace($cleanArgs)) {
                $psParams.ArgumentList = "`"$cleanArgs`""
            }
            if ($app.run_as_admin) {
                $psParams.Verb = "RunAs"
            }

            Write-Log "Attempting to launch: $cleanAppPath with args: '$cleanArgs' (Admin: $($app.run_as_admin))"
            Start-Process @psParams
            Write-Log "Launched App successfully: $cleanAppPath" "SUCCESS"
        } else {
            Write-Log "App executable/shortcut not found at: $cleanAppPath" "WARN"
        }
    } catch {
        Write-Log "Failed to launch App $cleanAppPath - $($_.Exception.Message)" "ERROR"
    }
}

Write-Log "--- Processing Terminal Tabs ---"
try {
    if ($config.terminals.Length -gt 0) {
        $wtArgs = ""
        for ($i = 0; $i -lt $config.terminals.Length; $i++) {
            $tab = $config.terminals[$i]
            $cleanTabPath = $tab.path.Trim('"')
            
            if (-Not (Test-Path $cleanTabPath)) {
                Write-Log "Terminal path does not exist, skipping tab: $cleanTabPath" "WARN"
                continue
            }

            if ($i -gt 0) { $wtArgs += " ; new-tab" }
            
            $wtArgs += " -p `"$($tab.profile)`" -d `"$cleanTabPath`""
            
            if ($tab.venv) {
                if ($tab.profile -match "PowerShell") {
                    $wtArgs += " powershell.exe -NoExit -Command `"if (Test-Path '.venv\Scripts\Activate.ps1') { . '.venv\Scripts\Activate.ps1' }`""
                } else {
                    $wtArgs += " cmd.exe /k `"if exist .venv\Scripts\activate.bat (call .venv\Scripts\activate.bat)`""
                }
            }
        }
        Write-Log "Executing Terminal Command: wt $wtArgs"
        Start-Process "wt.exe" -ArgumentList $wtArgs -ErrorAction Stop
        Write-Log "Terminal execution completed." "SUCCESS"
    }
} catch {
    Write-Log "Failed to execute Terminal command - $($_.Exception.Message)" "ERROR"
}

Write-Log "SEQUENCE COMPLETE" "DONE"
Write-Log "======================================================"