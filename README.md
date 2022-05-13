# ApexTracker
Personal Project using [EasyOCR](https://github.com/JaidedAI/EasyOCR) and dependencies. [Python 3.10.4](https://www.python.org/downloads/release/python-3104/)

## What's new
- May 12, 2022 - Version 2.1
  - Refactored Py and VBA code.
    - Python code reworked for readability/documentation
    - Both reworked to handle multiple imports at once
  - Now functions with non-definitive Python installation location, uses PATH
  - Installs dependencies when initial program directory set upon Excel first-time startup (shows shell so user can see progress)
  - Python script uses Tkinter to display errors if they occur during import.
  - Excel VBA waits until shell finishes running Python script
    - Observed import times (note the non-linear time taken) (CPU used for OCR)
      - 1 Import: ~4 seconds
      - 4 Imports: ~6 seconds
      - 42 Imports: ~48 seconds
  - The Python script now uses multiple sample-locations and uses the highest-confidence value for the character recognition. Drastic improvement to accuracy. Still use caution and check the imports for inaccuracies.
  - 1920x1080 support

## Installation
<details>
  <summary>Details</summary>
  
  ### Step 1
  Download [Python 3.10.4](https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe)
  Ensure pip is installed and Python is added to enviornment variables
  <details>
  <summary>Images</summary>
    <img src="https://user-images.githubusercontent.com/70485276/168204310-b8845f07-05ac-4ebd-a1e1-399102a7e419.JPG" alt="">
    <img src="https://user-images.githubusercontent.com/70485276/168204318-098a69d6-1287-47d2-9748-503c25cded8e.JPG" alt="">
  </details>
  
  ### Step 2
  Download the individual files (config.txt, requirements.txt, summaryToText.py, and ApexTrackerS13.xlsm)
  
  or
  
  Download the [SFX Archive](https://github.com/djs0065/ApexTracker/blob/main/ApexTrackerV2.1.exe)
  
  ### Step 3
  Edit the config.txt file with your screenshot directory for Apex Legends (Ex. D:\Steam\userdata\###\###\remote\###\screenshots)
  <details>
  <summary>Image</summary>
    <img src="https://user-images.githubusercontent.com/70485276/168205358-7c68474a-de09-4917-97e2-8153103de5ae.JPG" alt="">
  </details>
  
  ### Step 4
  Open the Excel file (ApexTrackerS13.xlsm) and enter the directory housing the downloaded/extracted files. Press "Submit" and you will see the Shell downloading the dependencies.
  <details>
  <summary>Images</summary>
    <img src="https://user-images.githubusercontent.com/70485276/168205793-984aa03d-b501-48ac-a62b-5daa83386309.JPG" alt="">
    <img src="https://user-images.githubusercontent.com/70485276/168205896-537a3f09-6bcb-4372-857d-8257a13b98a4.JPG" alt="">
  </details>
  
  ### Completed Installation

</details>

  ## Operation
  <details>
  <summary>Details</summary>
  
  ### Starting RP
  The blue box on the main sheet is unlocked and you should enter your current RP (before you play any new games/import any new data)
  
  ### Import Files
  Press the "Import Data" button to run the program and automatically import the game data from the screenshots within the directory in "config.txt"
  Once the program finishes loading, you will see your data loaded into the sheet. Wait times are proportional to the amount of data imported. If importing more than one game (2 screenshots) then expect to wait at least 5 seconds.
  
  ### Remove Data
  Press the "Remove Entry" button to remove the last line of data within the table. This can not be un-done and will be permanently removed. Consider moving your screenshot back into the directory and import again if necessary.
  
  ### Change Path
  Press the "Change Path" button to change the directory which Excel looks for the program (Python file, config.txt, etc.)
  
  ### Begin New Day
  On the "Graphs" sheet, press "Begin New Day" to insert a vertical line on the current game number. You can now see where you left off/began each day. Do this at the end of each day, or the beginning of each day before importing new games.
  
  ### Remove New Day
  On the "Graphs" sheet, press "Undo" to remove a vertical line (LIFO based). This can not be undone and will require the "Begin New Day" button the be pressed again.
</details>

## Known Bugs
 - If a damage value can not be read, the value will default to "0". Damage values that are "0" generally can not be read for some reason, and this was the route I took to handle those cases. If a damage value that shouldn't be "0" is recorded, please report the bug!
 - Many edge cases have not been able to be tested. Double digits within the K/A/D fields may be improperly read. Please report this!
 - Excel will give you Range errors before importing data as the graphs have nothing to read. Once you import at least 1 game, the error should stop appearing.

## Other Information
 - Report bugs directly to me via Discord: Piggy#5744. Please provide the screenshots which are providing an error in 1920x1080 (or other 16:9 aspect ratio) .jpg format. Advise me as to what the issue is.
 - Excel sheet protection password is "edit"
   - I do not suggest unprotecting the sheets unless you know what you are doing. Movement in the columns/rows will affect the macros/VBA code. Only unprotect the sheets if you are prepared for this to happen from your edit.
    


