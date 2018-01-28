$bin_path = "bin"
$filename = "colour-challenge_windows64.exe"
if (Test-Path "$bin_path/$filename")
{
    Remove-Item "$bin_path/$filename"

}
pyinstaller gui.spec --noconsole --onefile --noconfirm --distpath "$bin_path"
Move-Item "$bin_path/gui.exe" "$bin_path/$filename"
