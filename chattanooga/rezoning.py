from pypdf import PdfReader

reader = PdfReader("minutes/01_10_2023.pdf")
pages = len(reader.pages)
# text = page.extract_text()
linebreak = '\n'
rezone = "REZONE"

def findOccurrences(s, ch):
    print([i for i, letter in enumerate(s) if letter == ch])

# print(len(text))
# print(text.find('\n'))

# print([pos for pos, char in enumerate(text) if char == linebreak])
# print(text)

i = 0
while i < pages:
    page = reader.pages[i].extract_text()
    pageLength = len(page)
    print(pageLength)
    rezonePos = page.find(rezone)
    if rezonePos > 0:
        print(rezonePos)
    i += 1

# for page in reader.pages:
#     page = page.extract_text()
#     length = len(page)


#     # findOccurrences(page, linebreak)

#     rezones = []

#     rezonePos = page.find(rezone)

#     # print(rezonePos)

#     # if rezonePos > 0:
#     rezones.append(rezonePos)

# print(rezones)

    # i = 0
    # while i < 10:
    #     page = page[rezones:]
    #     print(page.find(rezone), length)
    #     i += 1


    # print(text)