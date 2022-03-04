import os

def takeNotes(filename, notes):
    filename = filename+".txt"
    path1 = "D:\\Py projects\\jarvis-3\\"+str(filename)  # project file location
    path2 = "D:\\Py projects\\jarvis-3\\notes\\"+str(filename)  # store location

    with open(filename, 'w') as file:
        file.write(notes)

    os.rename(path1, path2)  # os.rename(src, dst)
    #os.startfile(path2)  # to open file