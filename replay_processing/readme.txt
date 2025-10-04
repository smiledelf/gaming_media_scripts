LosslessCut-win.exe : quickly cut video clips
Openshot Video Editor : stitch clips together w/ transitions
https://cdn.openshot.org/static/files/user-guide/profiles.html#custom-profile


Workflow:
- Most recordings are replays --> use Python script to rename them to YYYY.MM.DD-HH.MM.mp4
  This script removes the game's name from the start
- Cut with LosslessCut
- Rename again with Python script to remove seconds from the name