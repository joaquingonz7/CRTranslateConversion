import argparse
import os.path
import re
import io

# Method to determine whether the file passed in exists.
def isValidFile(parser, arg, type):
    if not os.path.exists(arg) and type != "output":
        parser.error("The file %s does not exist!" % arg)
    elif not arg.endswith(".srt") and not arg.endswith(".tsv"):
        parser.error("The file %s is not a .srt or .tsv file!" % arg)
    else:
        return arg 

# Method used to split long lines
def splitLongLine(longLine):
    # Regex used to find the places where we can split the string.
    splitLinesRegex = re.compile(ur". | [ ,:;?!\u3001\u3002\uff61\ufe12]")

    finalText = longLine
    # If the line is too long, split it into 2.
    if len(longLine)  >= 60 and "\n" not in longLine: 
        # Find integer positions in the string where it can be split.
        # Store as a dictionary, key=position and value=current char
        splitPtsDict = { m.start():m.group() for m in splitLinesRegex.finditer(longLine)}
        # Find if there are logical places to split like the end of a 
        # sentence or a comma near the middle of the string to split at.
        strMidwayPt = len(longLine) / 2
        nonSpacePositions = [x for x in splitPtsDict if splitPtsDict[x] != ' ' and x >= strMidwayPt - 10 and x <= strMidwayPt + 10]
                
        ptToSplitAt = 0
        # Case where there is more than one place to split. 
        if len(nonSpacePositions) > 1:
            # Find the closest one and split on that.
            ptToSplitAt = min(nonSpacePositions, key=lambda x:abs(x-strMidwayPt)) + 1
        # Case where there is only one place to split.
        elif len(nonSpacePositions) == 1:
            # Split immediately on the one place to split. 
            ptToSplitAt = nonSpacePositions[0] + 1
        # Case where there is no obvious place to split.
        else:
            # Split on the closest space after the midway point or on the closest punctuation
            # outside of the 10 characters nearest the midway point.
            ptToSplitAt = min([x for x in splitPtsDict if x > strMidwayPt], key=lambda x:x-strMidwayPt)
            # If we split on punctionation, the split point should be at the space after the 
            # punctuation.
            if splitPtsDict[ptToSplitAt] != ' ':
                if longLine[ptToSplitAt+1] == ' ': ptToSplitAt += 1

        finalText = longLine[:ptToSplitAt] + "\n" + longLine[ptToSplitAt:]
    return finalText.replace("\n ", "\n")

# Conversion methods.
def srtToTsv(text):
    regex = re.compile('(\d+)\s+(\d+:\d+\d+:\d+,\d+ --> \d+:\d+:\d+,\d+)\s+(.+\s?.+\s?.+\s?)')
    normalizedQuotes = re.sub(ur'[\u0022\u201C\u201D]+', "*quotation mark*", text)
    matches = regex.findall(normalizedQuotes)
    formattedList = []
    for match in matches:
        if match[0].isdigit(): 
            formattedList.append("%s\t%s\t%s" % (match[0], match[1], 
            match[2].strip().replace('\r', ' ').replace('\n', ' ').replace('  ', ' ')))
    return "\n".join(formattedList)

def tsvToSrt(fileObj, performSplit):
    # Will hold final lines for the srt file.
    finalTextLines = []
    # Regex to look for timestamps, since those lines are the one we want to convert.
    regex = re.compile("(\d+:\d+\d+:\d+,\d+)")

    # Go line by line of the tsv and convert them to srt format.
    for line in fileObj:
        if regex.search(line):
            # Create array with each slot representing a cell in the spreadsheet.
            cells = line.split('\t') 
            # Split the line if it is too long. 
            if performSplit: translatedText = splitLongLine(cells[3])
            else: translatedText = cells[3]
            formattedLine = "%s\n%s\n%s" % (cells[0], cells[1], translatedText)
            finalTextLines.append(formattedLine)
    # Convert the final lines array into a string to write to the file.
    fullText = "\n\n".join(finalTextLines)
    return re.sub(r'\n\s*\n', '\n\n', fullText) # Remove duplicate newlines

# Main
# Set up the filename arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="inputFilename", required=True,
                    help="A tsv or srt file to convert.", metavar="FILE",
                    type=lambda x: isValidFile(parser, x, "input"))
parser.add_argument("-o", dest="outputFilename", required=True,
                    help="File to save the output to.", metavar="FILE",
                    type=lambda x: isValidFile(parser, x, "output"))
parser.add_argument("-s", dest="splitLines", default='y',
                    help="Pass in 'y' to split long lines or 'n' to leave as is",
                    choices=['y','n','Y','n'])
args = parser.parse_args()

# Read the file's text.
if args.inputFilename.endswith(".srt"):
    fileObj = io.open(args.inputFilename, mode="r", encoding="utf-8")
    # Perform the conversion and save it.
    with open(args.outputFilename, 'w') as outputFile:
        outputFile.write(srtToTsv(fileObj.read()).encode('utf-8'))
    # Close the input and output files.
    outputFile.close()
    fileObj.close()
if args.inputFilename.endswith(".tsv"):
    fileObj = io.open(args.inputFilename, mode="r", encoding="utf-8")
    # Perform the conversion and save it.
    with open(args.outputFilename, 'w') as outputFile:
        split = True if args.splitLines.lower() == 'y' else False
        outputFile.write(tsvToSrt(fileObj, split).encode('utf-8'))
    # Close the input and output files.
    outputFile.close()
    fileObj.close()