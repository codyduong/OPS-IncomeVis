"""originally intended to rewrite directory, but due to filewriting limitations, doesn't work, so instead this doesn't
do anything... oops."""

if __name__ == "__main__":
    content = []
    with open("directory.mhtml") as f:
        lines = f.readlines()
        stored = ''
        for line in lines:
            lineS = line.strip()
            if stored == '':
                if lineS != '' and lineS[-1] == "=":
                    stored = lineS.strip('=')
                else:
                    content.append('%s\n' % lineS)
            else:
                lineS = stored+lineS + '\n'
                stored = ''
                content.append(lineS)
        
    for each in content:
        print(each)

    with open("directoryFormatted.txt", "w") as f:
        f.writelines(content)