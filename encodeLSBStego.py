from PIL import Image
import time


# ===== File reading and input =================================================


# Given an image filename, read the data and return a dictionary of filedata
def readImage(filename, getBits=False):
    # Image object's baseline parameters
    imageData = {
        "width": 0,
        "height": 0,
        "RGBData": [],  # Contains the RGB values as a list of pixel tuples
        "bitString": ""  # Contains all bits as a long string
    }

    # Construct image filepath
    imageFilepath = "./input/" + filename

    # Read the image file
    pilImage = Image.open(imageFilepath).convert("RGB")
    # Get the width and height
    imageData["width"] = pilImage.width
    imageData["height"] = pilImage.height

    # Get the RGB data
    imageData["RGBData"] = list(pilImage.getdata())

    # Get the binary data as a string
    if getBits:
        imageData["bitString"] = convertRGBListToBits(imageData["RGBData"])
    else:
        imageData["bitString"] = ""

    return imageData


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
        r = convertIntToBits(RGBObject[0])
        # Get the green value
        g = convertIntToBits(RGBObject[1])
        # Get the blue value
        b = convertIntToBits(RGBObject[2])

        # Concatenate the values
        bitString += r + g + b

    return bitString


# ===== Verification of sizing parameters ======================================


# Check that the hidden file is sufficiently smaller than the visible file
def checkFileSize(visibleImageData, hiddenImageData, encodingWH):
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

    if supportedVisibleSize > visibleFileSize:
        raise ValueError(
            f"checkFileSize(): Hidden file is too large ({hiddenFileSize}). Visible file will not support this (size needed is >={supportedVisibleSize}, current size is {visibleFileSize})")


# ===== Bit splicing ===========================================================


# Encode the hidden file bits into the visible file bits
def encodeImages(visibleFileData, hiddenFileData, encodingWH):
    # First, splice in the sizing parameters of the hidden file
    hiddenWStr = convertIntToBits(hiddenFileData["width"])
    hiddenHStr = convertIntToBits(hiddenFileData["height"])

    # Splice in the width and height at the start
    for i in range(len(hiddenWStr)):
        visibleFileData["RGBData"][i] = (
            visibleFileData["RGBData"][i][0],
            visibleFileData["RGBData"][i][1] | int(hiddenWStr[i]),
            visibleFileData["RGBData"][i][2] | int(hiddenHStr[i])
        )

    # Splice in the hidden file bits in R, G, B channels
    for i in range(len(hiddenWStr), len(hiddenFileData["bitString"])):
        # Compute the 0-start index value
        j = i - len(hiddenWStr)

        try:
            visibleFileData["RGBData"][i] = (
                visibleFileData["RGBData"][i][0] | int(
                    hiddenFileData["bitString"][3*j]),
                visibleFileData["RGBData"][i][1] | int(
                    hiddenFileData["bitString"][3*j+1]),
                visibleFileData["RGBData"][i][2] | int(
                    hiddenFileData["bitString"][3*j+2])
            )
        except IndexError:
            # If the index is out of range, just move on
            pass

    return visibleFileData


# ===== File encoding and writing ==============================================


# Given a dictionary of image data, write the data to a file
def writeImage(imageData, filename):
    # Construct image filepath
    imageFilepath = "./output/" + filename

    # Create the image file
    pilImage = Image.new(
        'RGB', (imageData["width"], imageData["height"]))

    # Iterate through the RGB data and set the pixel values
    for i in range(0, len(imageData["RGBData"])):
        pilImage.putpixel((i % imageData["width"], i // imageData["width"]),
                          (imageData["RGBData"][i][0], imageData["RGBData"][i][1], imageData["RGBData"][i][2]))

    # Write the image file
    pilImage.save(imageFilepath)


# ===== Driver code ============================================================


def main():
    encodingWH = 13  # Number of pixels to encode width/height in

    # Read the input visible file to a dictionary object of RGB tuples
    print("Reading visible image...")
    visibleFilename = "spiderverse.png"  # Do not include relative filepath
    visibleImageData = readImage(visibleFilename)

    # Read the input hidden file to a dictionary object
    print("Reading hidden image...")
    hiddenFilename = "popcat.png"  # Do not include relative filepath
    hiddenImageData = readImage(hiddenFilename, getBits=True)

    # Verify sizing parameters of hidden and input files
    print("Verifying file sizes...")
    checkFileSize(visibleImageData, hiddenImageData, encodingWH)

    # Encode the hidden file bits into the visible file bits
    print("Encoding hidden file...")
    encodedImageData = encodeImages(
        visibleImageData, hiddenImageData, encodingWH)

    # Reform this into an image and write to output directory
    print("Writing encoded image...")
    writeImage(encodedImageData, f"{visibleFilename}_encoded.png")

    print("Done.")


if __name__ == '__main__':
    startTime = time.time()
    main()
    print(f"Total time: {time.time() - startTime}")
