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

# Conversion methods.
def srtToTsv(text):
    regex = re.compile('(\d+)\s+(\d+:\d+\d+:\d+,\d+ --> \d+:\d+:\d+,\d+)\s+(.+\s?.+\s?.+\s?)')
    normalizedQuotes = re.sub(ur'[\u0022\u201C\u201D]+', "*quotation mark*", text)
    matches = regex.findall(normalizedQuotes)
    formattedList = []
    for match in matches:
        if match[0].isdigit(): formattedList.append("%s\t%s\t%s" % (match[0], match[1], match[2].strip().replace('\r', ' ').replace('\n', ' ').replace('  ', ' ')))
    return "\n".join(formattedList)

def tsvToSrt(fileObj):
    # Will hold final lines for the srt file.
    finalTextLines = []
    # Regex to look for timestamps, since those lines are the one we want to convert.
    regex = re.compile("(\d+:\d+\d+:\d+,\d+)")

    # Go line by line of the tsv and convert them to srt format.
    for line in fileObj:
        if regex.search(line):
            cells = line.split('\t') # Create array with each slot holding the contents of a cell in the spreadsheet.
            formattedLine = "%s\n%s\n%s" % (cells[0], cells[1], cells[3])
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
        outputFile.write(tsvToSrt(fileObj).encode('utf-8'))
    # Close the input and output files.
    outputFile.close()
    fileObj.close()
