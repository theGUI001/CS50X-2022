# Prompt for text and calculate text length
text = input("Text: ")
textLen = len(text)

# initialize the variables of text
words = 1
letters = 0
sentences = 0

# Loop trought text
for i in range(0, textLen, 1):
    # Count all words, letters an sentences
    if text[i].isalnum():
        letters += 1
    if text[i] == ' ':
        words += 1
    if text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

# Calculate the Coleman-Liau index
l = float(letters) / words * 100
s = float(sentences) / words * 100.0
index = round(0.0588 * l - 0.296 * s - 15.8)

# Verify grades and print them
if index < 1:
    print("Before Grade 1")
    exit()
elif index >= 16:
    print("Grade 16+")
    exit()
else:
    print(f"Grade {index}")
