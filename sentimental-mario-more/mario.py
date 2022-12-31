# Prompt user for height:
while True:
    try:
        height = int(input("Height: "))
        # Verify if height is >= 1 and <= 8
        if height >= 1 and height <= 8:
            break
    # Print error if input is not an int
    except:
        print("Not a valid height")

# Loop through lines and columns and print #
for i in range(0, height, 1):
    for j in range(0, height + i + 3, 1):
        if j == height or j == height + 1 or i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print()
