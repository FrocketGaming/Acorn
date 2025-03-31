# Version 0.3.0
## Enhancements
- Added a release notes popup, which is probably how you're reading this!
    - Now after you install a new release you get to see what's changed.
- Improved the file extension so it auto populates the file type on edit.
- Improved type sorting to ignore case sensitivity.
- Search now includes the Name of the snippet as well as the description, if an astricks is provided at the beginning of the search then content of the snippets are also considered.
    - Example: *MySearchTerm
- Search terms now maintain in the search bar instead of being cleared automatically.
- If no search results are found a message will now be displayed.
- Snippet popup window supports two additional functions:
    - While holding CTRL you can move this window.
    - While holding SHIFT + CTRL and moving your mouse you can resize it! The smallest size is the old default size.
- When the application displays using the hotkey it will now display where your mouse cursor is.
- Added a confirmation popup for deleting snippets.
- Archive implementation, this is for snippets you want to keep saved but don't need visible all the time.
    - Right click on Snippet Types and select 'Archive' to archive it.
    - Check the 'View Archived Snippets' checkbox to view all the snippets you've archived!
- Added syntax highlighting for .py and .sql files, it matches the theme chosen (which is still only Matcha at this time...)

## Bug Fixes
- Application should always be in focus when the hotkey is used to bring it back up.
- "Copied!" pop up was fixed so it occurs at the location of the copy button for better visibility.
- Added a 15 character limit to the Snippet Type, these are intended to be short category labels; not lengthy descriptions.
- Fixed some backend redundancy interactions with the database to improve performance.