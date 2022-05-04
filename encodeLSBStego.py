from PIL import Image


# ===== File reading and input =================================================


# Given an image filename, read the data and return a dictionary of filedata
def readImage(filename):
    # Image object's baseline parameters
    imageData = {
        "width": 0,
        "height": 0,
        "RGBData": [],  # Contains the RGB values as a list of objects
        "bitString": ""  # Contains all bits as a long string
    }

    # Construct image filepath
    imageFilepath = "./input/" + filename

    # Read the image file
    pilImage = Image.open(imageFilepath)
    # Get the width and height
    imageData["width"] = pilImage.width
    imageData["height"] = pilImage.height

    # Get the RGB data
    imageData["RGBData"] = convertRGBListToJSON(list(pilImage.getdata()))

    # Get the binary data as a string
    imageData["bitString"] = convertRGBListToBits(imageData["RGBData"])

    return imageData


# Convert a list of RGB values to a list of JSON RGB value objects
def convertRGBListToJSON(RGBList):
    # Sanity check: List length is a multiple of 3
    if len(RGBList) % 3 != 0:
        raise ValueError(
            "convertRGBListToJSON(): RGBList length is not a multiple of 3")

    RGBJSONList = []

    for i in range(0, len(RGBList), 3):
        # Create a JSON object
        RGBJson = {
            'r': RGBList[i],
            'g': RGBList[i + 1],
            'b': RGBList[i + 2]
        }

        # Append the JSON object to the list
        RGBJSONList.append(RGBJson)

    return RGBJSONList


# Convert an integer into a string of bits
def convertIntToBits(intValue):
    # Convert the integer to a binary string
    binString = bin(intValue)[2:]

    # Pad the binary string with 0's to make it 8 bit multiples
    binString = binString.zfill(8)

    # Return the binary string as a string of bits
    return binString


# Given a list of RGB objects, return a string of bits
def convertRGBListToBits(RGBList):
    bitString = ""

    # Iterate through each object
    for RGBObject in RGBList:
        # Get the red value
        r = convertIntToBits(RGBObject["r"])
        # Get the green value
        g = convertIntToBits(RGBObject["g"])
        # Get the blue value
        b = convertIntToBits(RGBObject["b"])

        # Concatenate the values
        bitString += r + g + b

    return bitString


# ===== Verification of sizing parameters ======================================


# Check that the hidden file is sufficiently smaller than the visible file
def checkFileSize(visibleImageData, hiddenImageData, encodingWH):
    # Sanity check: Both items are multiples of 3
    if len(visibleImageData["RGBData"]) % 3 != 0:
        raise ValueError(
            "checkFileSize(): Visible file is not a multiple of 3")
    if len(hiddenImageData["RGBData"]) % 3 != 0:
        raise ValueError("checkFileSize(): Hidden file is not a multiple of 3")

    # Encoding width and height in the last 2*encodingWH pixels of the visible image
    maxSize = pow(2, encodingWH) - 1
    # Sanity check - Hidden file must be smaller than 8192x8192
    if hiddenImageData["width"] > maxSize or hiddenImageData["height"] > maxSize:
        raise ValueError(
            f"checkFileSize(): Hidden file is too large. Encoding bitdata will not support this (max is {maxSize}x{maxSize}")

    # Check if hidden file is smaller than visible file by a factor
    hiddenFileSize = hiddenImageData["width"] * hiddenImageData["height"] \
        + (encodingWH * 2)  # Append the width and height encoding
    supportedVisibleSize = hiddenFileSize * 8  # 8 bits per pixel
    visibleFileSize = visibleImageData["width"] * visibleImageData["height"]

    if supportedVisibleSize < visibleFileSize:
        raise ValueError(
            f"checkFileSize(): Hidden file is too large. Visible file will not support this (size needed is >={supportedVisibleSize})")


# ===== Bit splicing ===========================================================


# Encode the hidden file bits into the visible file bits
def encodeImages(visibleFileData, hiddenFileData, encodingWH):
    # First, splice in the sizing parameters of the hidden file
    hiddenWStr = convertIntToBits(hiddenFileData["width"])
    hiddenHStr = convertIntToBits(hiddenFileData["height"])

    # Iterate through the last encodingWH bits and replace with width/height
    for i in range(0, encodingWH):
        visibleFileData["bitString"][-i - 1] = hiddenWStr[i]
        visibleFileData["bitString"][-i - 1 - encodingWH] = hiddenHStr[i]

    # Now iterate through all bits in the hidden file and splice them into the visible file
    for i in range(0, len(hiddenFileData["bitString"])):
        # Modify the RGB values of the visible file
        visibleFileData["RGBData"][i]["r"] = int(
            visibleFileData["RGBData"][i]["r"]) | int(hiddenFileData["bitString"][i])
        visibleFileData["RGBData"][i]["g"] = int(
            visibleFileData["RGBData"][i]["g"]) | int(hiddenFileData["bitString"][i])
        visibleFileData["RGBData"][i]["b"] = int(
            visibleFileData["RGBData"][i]["b"]) | int(hiddenFileData["bitString"][i])

    return visibleFileData


# ===== File encoding and writing ==============================================


# ===== Driver code ============================================================


def main():
    encodingWH = 13  # Number of pixels to encode width/height in

    # Read the input visible file to a dictionary object of RGB tuples
    visibleFilename = "spiderverse.png"  # Do not include relative filepath
    visibleImageData = readImage(visibleFilename)

    # Read the input hidden file to a dictionary object
    hiddenFilename = "popcat.png"  # Do not include relative filepath
    hiddenImageData = readImage(hiddenFilename)

    # Verify sizing parameters of hidden and input files
    checkFileSize(visibleImageData, hiddenImageData, encodingWH)

    # Encode the hidden file bits into the visible file bits
    encodedImageData = encodeImages(
        visibleImageData, hiddenImageData, encodingWH)

    # Reform this into an image and write to output directory


if __name__ == '__main__':
    main()
