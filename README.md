Script to convert srt files to tsv files that can be uploaded 
to Google Drive for translation and vice versa. 

Instructions:

SRT to Google Drive

1) Download the relevant SRT file from our lovely friends at CRTranscript found here: 
https://drive.google.com/drive/folders/0B5QJULzu8Dw7RHVwVS1yeDczVzg

2) Save the file as a .tsv file. This is the format that will be used to import to 
Google Drive.

3) Run the script as follows:
python CRTranslateConversionScript.py -i input.srt -o output.tsv

4) Copy the file for a previous episode and move it to the relevant folder. 
There is a folder for each language. 
Top level folder: https://drive.google.com/drive/folders/0B9a0T4tmFR5aLVRJQXF1MkxQZ28. 
Example episode:  https://docs.google.com/spreadsheets/d/1ZT9SLKKL3CHYpPJ6ItfHBwPgDMSRGylUJDnRwGZDVqM/edit#gid=1152439721.

5) On the Work-sheet tab, put your cursor in A2 (the first line number) in the File menu:
    - Click Import. 
    - Select the file from your computer.
    - Choose Replace data at selected cell, separator is tab,
      select don’t convert text into numbers and dates.
    - Click Import.
    
6) Do a find and replace: 
    - Find *quotation mark* Replace "
    
Note: This needs to be done because the import to Google Drive has issues with quotation
marks. The script replaces all quotation marks with the text *quotation mark*. The find
and replace in this step reverses that so they display as actual quotation marks in
Google Drive. 

7) Go down the Language column and combine any data in this column with the Original column.

8) Fix any formatting on the Worksheet page.

9) Fix the Sign-up page to have the correct number of 5 min chunks.

10) Link the new file on the Master Link-List: 
https://docs.google.com/spreadsheets/d/1kcDEJJKaECJaeFVZH1ltmtmXYBr9MCJ8UI9tjDDWPSM/edit#gid=1830730900




Google Drive to SRT

1) Export the translation sheet as a TSV.

2) Run the script as follows: python CRTranslateConversionScript.py -i input.tsv -o output.srt

Note: This will split any long lines to display as two lines in the final subtitles.
If you do not want this to happen add "-s n" to the command. It will look like 
python CRTranslateConversionScript.py -i input.tsv -o output.srt -s n

3) Upload the completed file to the relevant folder in this folder: 
https://drive.google.com/drive/folders/0B0poUi6msyADYlhHLV9tNjhGbkU

4) Let @bills know on Slack that the file has been uploaded so he can send it to 
CRTranscript who then send it to G&S.


