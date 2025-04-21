from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from os import path
import glob
import gzip
from datetime import datetime

outputFileName_fwd = "output_search_ITR-forward.txt"
outputFileName_rev = "output_search_ITR-reverse.txt"
ITR_20nt_fwd = "TCAGGTGTACAAGTATGAAA"
ITR_20nt_rev = "TTTCATACTTGTACACCTGA"

def chooseDirectory():
    dir = filedialog.askdirectory(initialdir=pathToWorkingFolder.get(),title="Choose working directory",mustexist=True)
    pathToWorkingFolder.set(dir)

def runScript():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Starting time: {current_time}")
    # Create a subdirectory called 'originalCompressedFiles' in the pathToWorkingFolder
    rootDir = pathToWorkingFolder.get()
    originalCompressedDir = os.path.join(rootDir, 'original_WGS_CompressedFiles')
    # create a subdirectory called 'originaluncompressedFiles' in the pathToWorkingFolder
    originalUncompressedDir = os.path.join(rootDir, 'original_WGS_UncompressedFiles')
    # create a subdirectory called 'temporaryFiles' in the pathToWorkingFolder
    temporaryFilesDir = os.path.join(rootDir, 'temporaryFiles')
    for directory in [temporaryFilesDir]:#originalUncompressedDir, originalCompressedDir
        if not os.path.exists(directory):
            os.makedirs(directory)
    # Move the original .gz files to the subdirectory
    gz_files = glob.glob(os.path.join(rootDir, '*.gz')) #search all gz files in the working folder
    for gz_file in gz_files:
        originalCompressedFile = os.path.join(originalCompressedDir, os.path.basename(gz_file))
        #os.rename(gz_file, originalCompressedFile) # Move the file to the new directory
        # unzip the gz file to the originalUncompressedDir
        with gzip.open(gz_file, 'rt') as gzipFile:
            with open(os.path.join(temporaryFilesDir, outputFileName_fwd), 'a') as outputFileFwd:
                with open(os.path.join(temporaryFilesDir, outputFileName_rev), 'a') as outputFileRev:
                    line_count = 0
                    for line in gzipFile:
                        if line_count % 4 == 1:  # Take only the second line every four lines
                            if ITR_20nt_fwd in line:
                                outputFileFwd.write(line)
                            if ITR_20nt_rev in line:
                                outputFileRev.write(line)
                        line_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Ending time: {current_time}")
    #fenetre.destroy()
    messagebox.showinfo('succes', 'la conversion est faite')

# On crée une fenêtre, racine de notre interface
fenetre = Tk()
fenetre.minsize(540, 1)
fenetre.title('miniMOS_WGS_analysis')
fenetre.resizable(True, False)
# initialisation des variables
pathToWorkingFolder = StringVar()
pathToWorkingFolder.set(path.expanduser("~"))
# fenetre.withdraw()
cadreFichier = LabelFrame(fenetre, borderwidth=2, text='Working directory')
cadreFichier.pack(fill=X)
labelNomFichier = Label(cadreFichier, textvariable=pathToWorkingFolder)
labelNomFichier.pack(side="left")
bouton_choixFichier = Button(cadreFichier, text='choose', command=chooseDirectory)
bouton_choixFichier.pack(side="right")
# On crée un cadre pour les boutons de la fenêtre principale
cadreBoutons = Frame(fenetre, borderwidth=2)
cadreBoutons.pack(fill=X)
bouton_conversion = Button(cadreBoutons, text="Run script", command=runScript, fg="green")
bouton_conversion.pack(fill=X)
bouton_quitter = Button(cadreBoutons, text="Exit", command=fenetre.destroy, fg="red")
bouton_quitter.pack(fill=X)

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
