Just a collection of scripts to help process gaming media (screenshots, recordings, etc.)


# Screenshots organiser
Organise Steam's uncompressed screenshots into different folders based on their App Id.

Since Steam saves uncompressed screenshots into the same folder, this script allows you to organise them into different folders in one click.

### Usage
To use the script:
* Drop script into Steam's uncompressed screenshots folder 
* Run the script

It will only move loose screenshots that aren't already in folders.

Screenshot extensions recognised: `.png`, `.jpg`

### Future ideas
* Organise based on different rules (e.g. year-monthly timeline)



# Screenshots renamer
Rename screenshots based on a naming scheme using the latest modified date metadata.

### What's this for?

Example use case - i.e. the problem I was solving:
- Take screenshot with EA launcher
- Take screenshot with Ubisoft launcher
- They have different naming schemes!
- Drop the script in, and rename the screenshots with a specified naming scheme.

### Usage
To use the script:
- Drop the script into a screenshots folder
- Run the script
- Choose the output naming scheme, and finish renaming

#### Naming schemes to choose:

  - Windows: `YYYY-mm-dd (N)`
  - Steam: `AppID_YYYYmmddHHMMSS_N`

where N is the duplicate handling index (e.g Steam starts with 1)
