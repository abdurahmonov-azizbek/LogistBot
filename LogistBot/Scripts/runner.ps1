$Host = "localhost"
$Port = "5432"
$Database = "logistbotdb"
$User = "postgres"
$Password = "postgres"
$ScriptDir = "D:\PROJECTS\Logistbot\LogistBot\Scripts" # Path to your folder with SQL scripts

$Scripts = Get-ChildItem -Path $ScriptDir -Filter "*.sql"

foreach ($Script in $Scripts) {
    Write-Host "Running $($Script.FullName)..."

    # Run each script
    cmd /c "set PGPASSWORD=$Password && psql -h $Host -p $Port -d $Database -U $User -f $($Script.FullName)"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "$($Script.FullName) executed successfully!"
    } else {
        Write-Host "Error running $($Script.FullName)"
        break
    }
}
