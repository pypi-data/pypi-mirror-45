# HHSearch (1.5) Parser module - created by Tim D.

# <editor-fold desc=" ######### IMPORTS AND REQUIREMENTS #########">
import re
import webbrowser
import __main__
import time
import os
import numpy as np
import pandas as pd
# PyMOL captures STDOUT
import sys
import pymol
from pymol import cmd, stored
from io import StringIO
from shutil import copyfile

import matplotlib.pyplot as plt
import matplotlib

from PIL import Image

from send2trash import send2trash

__main__.pymol_argv = ['pymol', '-qc']  # Pymol: quiet and no GUI
stdout = sys.stdout
pymol.finish_launching()
# recover the original STDOUT
sys.stdout = stdout
cmd.set('retain_order', 1)  # otherwise PyMOL would scramble the order of atoms


# </editor-fold>

def extract_HHSearch_data(hhs_file: str = "data/hhs/d1e0ta1.hhs") -> pd.DataFrame:
    """
    Extracts the HHSearch Statistics out of a .hhs file, storing it into a pandas DataFrame.

    Example of the data extracted:
        No Hit    Description            Prob  E-value P-value  Score   SS  Cols  Query HMM  Template HMM   length
        1 d1e0ta1 b.58.1.1 (A:70-167) Py 100.0   7E-39 2.5E-43  199.9   0.0   98    1-98      1-98          (98)
        2 d2vgba1 b.58.1.1 (A:160-261) P 100.0 6.6E-38 2.4E-42  196.6   0.0   98    1-98      1-102         (102)

    The Pandas DataFrame contains the keys:
    No, Hit, Description, Prob, E-Value, P-Value, Score, SS, Cols, Query HHM, Template HHM and length

    :param hhs_file: the path of the hhs file of interest.
    :return: Returns a Pandas DataFrame with the described columns.
    """

    with open(hhs_file) as f:
        result = f.read()

    # determine the part of the file which contains the overview of the statistics.
    search_statistics_start = re.search(r'No Hit', result).start()
    search_statistics_end = re.search(r'No 1', result).start()

    # getting rid of the two blank lines after the statistics.
    search_statistics = result[search_statistics_start:search_statistics_end - 2]

    # create a file-like class of the string, so it can be read-in by pd.read_fwf().
    # https://docs.python.org/3/library/io.html
    search_statistics = StringIO(search_statistics)

    # Define Header line No Hit Des... etc.
    header_line = 0

    # defining the widths of each cell in a line.
    widths = [3, 8, 24, 5, 8, 8, 7, 6, 5, 10, 10, 6]

    # Reads a table of fixed-width formatted lines into a Pandas DataFrame out of a file or file-like string.
    # Documentary: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_fwf.html
    dataread = pd.read_fwf(search_statistics,
                           header=header_line,
                           widths=widths)

    # alternatively to StringIO I could have evaluated the length of the string created and read directly from the file.
    # With that method, the first 8 lines would be skipped, while only the n rows would have been read by the read_fwf.
    # However, if the HHSearch format should ever change for whatever reason and the length of the informative at the
    # start would exceed 8 lines, this module would break. Hence, the first method described here was discarded and
    # StringIO was used instead to be of universal usage.
    """
    # First idea/approach, discarded. 
    # Skip the beginning lines of the Document, jumping to the stats.
    line_to_start = 8
    search_statistics = search_statistics.split("\n")
    # Read rows till the end of the summarized statistics only.
    rows_to_read = len((search_statistics)) - 1

    dataread = pd.read_fwf(hhs_file, skiprows=line_to_start,
                           nrows=rows_to_read,
                           header=header_line,
                           widths=widths)  
    """

    # Since the normal hhs file doesn't have a header for "Description", need to recreate the column's names.
    new_colnames = ["No",
                    "Hit",
                    "Description",
                    "Prob",
                    "E-Value",
                    "P-Value",
                    "Score",
                    "SS",
                    "Cols",
                    "Query HMM",
                    "Template HMM",
                    "length"]

    mappingdict = dict()

    # enumerate over the created DataFrame's headers, adding them to the new dict.
    for counter, x in enumerate(dataread):
        mappingdict[x] = new_colnames[counter]

    # Rename the columns headers.
    dataread.rename(columns=mappingdict, inplace=True)

    # dataread.set_index("No", inplace=True) # Decided against this, user can do this himself if wanted.

    return dataread


def cmdPNG(fN: str = 'tmp.png', width: int = 0, height: int = 0, dpi: float = -1.0, ray: int = 0):
    '''
    Create pymol image, wait until the file exists and display it in the notebook

    This function was kindly provided by Dr. Schmidt.

    :fN:     file name
    :width:  width of image [optional]
    :height: heigth of image [optional]
    :dpi:    resolution (dpi)
    :ray:    pymol ray trace modes available (c.f. https://pymolwiki.org/index.php/Ray)
    '''
    if os.path.exists(fN):
        os.path.os.unlink(fN)
    cmd.png(fN, width, height, dpi, ray)
    while not os.path.exists(fN) or not os.path.getsize(fN):
        time.sleep(1)


def extract_HHSearch_main(hhs_file: str = "data/hhs/d1e0ta1.hhs") -> dict:
    """
    Extracts information about the query within the .hhs file.

    As an example:

    {'Query': 'Query d1e0ta1 b.58.1.1 (A:70-167) Pyruvate kinase (PK) {Escherichia coli [TaxId: 562]}',
     'pdb_id': '1e0t',
     'alignment_term': '/1e0t//A/70-167/CA',
     'full_term': '/1e0t//A//CA',
     'file_name': 'd1e0ta1'
     }

    Notice: file_name does **not** contain the .hhm or .hhs ending, but simply the full name.

    :param hhs_file: the path of the hhs file of interest.
    :return: returns a dict() with the keys
             "Query", "pdb_id", "alignment_term", "full_term", "file_name"
    """

    with open(hhs_file) as f:
        result = f.read()

    # Getting the whole query line and getting rid of the spaces
    query = result.split("\n", 1)[0]
    query = f"{query.split(maxsplit=1)[0]} {query.split(maxsplit=1)[1]}"

    # get name, residues, as well as the chain's name out of the query line
    query_e = query.split()
    name = query_e[1]
    pdb_id = name[1:5]
    residues = query_e[3]
    filter_chain = name[-2:-1].upper()

    # extract the residue spans only
    span = re.finditer(r":[0-9]*-*[0-9]*", residues)
    filter_span = str()
    for x in span:
        filter_span = filter_span + residues[x.start():x.end()].strip(":") + ","

    # get rid of the last added comma gain
    filter_span = filter_span.strip(",")

    # create the alignment terms (with the residue span) based of the aquired information.
    alignment_term = f"/{pdb_id}//{filter_chain}/{filter_span}/CA"
    # same as alignment term, just without the filter_span value, showing the whole chain X
    full_term = f"/{pdb_id}//{filter_chain}//CA"

    # creating the returned dict()
    result_dict = {"Query": query,
                   "pdb_id": pdb_id,
                   "alignment_term": alignment_term,
                   "full_term": full_term,
                   "file_name": name}

    return result_dict


def get_alignment_term(dataread, pos: int = 1) -> dict:
    """
    Similiar to extract_HHSearch_main, it extracts information required for the alignment about the template of choice
    based on an entered position number. As input, one should use the pandas DataFrame of the function
    extract__HHSearch_data, while passing the Hit No. to get_alignment_term, to retrieve the information about
    that specific hit.

    As an example:

    {'pdb_id': '1e0t',
     'alignment_term': '/1e0t//A/70-167/CA',
     'full_term': '/1e0t//A//CA',
     'file_name': 'd1e0ta1'
     }

    Notice: file_name does **not** contain the .hhm or .hhs ending, but simply the full name.

    :param dataread: pandas DataFrame of an .hhs file, can be created with extract_HHSearch_data
    :param pos: No. of the hit of interest within the DataFrame/hhs file.
    :return: Returns a dict() with the keys:
             "pdb_id", "alignment_term", "full_term", "file_name"
    """

    # getting the name, the chain as well as the pdb_id out of the "Hit" row of the DataFrame.
    name = dataread.get("Hit").iloc[pos - 1]
    filter_chain = name[-2:-1].upper()
    pdb_id = name[1:5]

    # Sometimes the short descriptions within the .hhs files cut off at the information about the
    # chain, as well as the residues of interest. For that, this data is taken out of the actual hhm file.
    with open(f"data/hhm/{name}.hhm", "r") as f:
        target = f.read()
        target = target.splitlines()[1].split()[3]

    # search for the residue spans only.
    span = re.finditer(r":[0-9]*-*[0-9]*", target)
    filter_span = str()
    for x in span:
        filter_span = filter_span + target[x.start():x.end()].strip(":") + ","
    # getting rid of the last added ","
    filter_span = filter_span.strip(",")

    # Creating the alignment_term, taking in the residue span, and the full_term ignoring the residue span.
    alignment_term = f"/{pdb_id}//{filter_chain}/{filter_span}/CA"
    full_term = f"/{pdb_id}//{filter_chain}//CA"

    # the actual returned dict()
    result_dict = {"pdb_id": pdb_id,
                   "alignment_term": alignment_term,
                   "full_term": full_term,
                   "file_name": name}

    return result_dict


def get_full_alignment(hhs_file: str = "data/hhs/d1e0ta1.hhs",
                       no: int = 1) -> str:
    """
    Returns the detailed data of a hit within a given hhs file at a passed position as a html formatted string.

    It's also stored within a separate folder
    /alignments_highlighted/<query>/<NoX-name>.html

    Within the string, helices and sheet patterns are colorized red and blue.

    :param hhs_file: the path of the hhs file of interest.
    :param no: the hit No. within the hhs file.
    :return: returns a string, which is HTML formatted. One could use Display(HTML(description_new)) to
             load it for example within jupyter, or view the string within the separately created html file.
    """

    # framing the lines of the hit of interest only. In case of last hit, take in "Done!" as consideration too.
    start = f"No {no}"
    end = f"No {no+1}"
    end = r'(' + end + ')|(Done!)'

    with open(hhs_file) as f:
        result = f.read()

    # Get the query's name, too.
    query = result.split("\n", 1)[0]
    query = f"{query.split(maxsplit=1)[0]} {query.split(maxsplit=1)[1]}"

    # search, if the No. even exists within the presented hhs file.
    try:
        search_start = re.search(start, result).start()
        search_end = re.search(end, result).start()
    except:
        raise Exception("The description number you entered is not within the hhs_file!")

    # framing the description of the hit
    description = result[search_start:search_end].splitlines()
    description_new = str()

    # regex for later, looking for sheets/helices within the description
    sheet = re.compile(r'E+', re.I)
    helix = re.compile(r'H+', re.I)

    # check each line in the description
    for x in description:
        # get the name of the found target. Used later to create the filename.
        if x.startswith(">"):
            name = x.split()[0].strip(">")

        # Only look for ss_pred lines to colorize them.
        if x.startswith("Q ss_pred") or x.startswith("T ss_pred"):
            # offset, changing after each time something got colorized.
            offset = 0
            sheet_hits = sheet.finditer(x)

            # colorizing pattern for sheets.
            fonting_start = "<font color=blue>"
            fonting_end = "</font>"

            # colorizing sheet's entries. [1:] is just a simple workaround for the first "e" within ss_pred.
            for hit in list(sheet_hits)[1:]:
                x = f"{x[:hit.start()+offset]}{fonting_start}{x[hit.start()+offset:hit.end()+offset]}" \
                    f"{fonting_end}{x[hit.end()+offset:]}"
                offset += len(fonting_start) + len(fonting_end)

            # reset the offset to start with helices. God bless there's no "h" in the previous fonting_start/end.
            offset = 0
            helix_hits = helix.finditer(x)

            # colorizing pattern for helices.
            fonting_start = "<font color=red>"
            fonting_end = "</font>"

            # colorizing the helix's entries.
            for hit in helix_hits:
                x = f"{x[:hit.start()+offset]}{fonting_start}{x[hit.start()+offset:hit.end()+offset]}" \
                    f"{fonting_end}{x[hit.end()+offset:]}"
                offset += len(fonting_start) + len(fonting_end)

        # <pre>...</pre> secures the formatting of the html string to be presented correctly.
        # It is added to each line, securing each line's format.
        description_new = description_new + f"<pre>{x}</pre>\n"

    # last but not least, adding the query's information to the first line.
    description_new = f"<pre>{query}</pre>\n{description_new}"

    # getting the filename without the ending, needed to create subfolders for each query.
    filename = os.path.basename(hhs_file).split(".")[0]

    # just in case these folders don't exist yet.
    paths = ["lastrun", f"alignments_highlighted/{filename}"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    # storing the alignment within organized subfolders, but also into a folder holding information about the last run.
    with open(f"alignments_highlighted/{filename}/No{no}-{name}.html", "w") as f:
        f.write(description_new)

    copyfile(f"alignments_highlighted/{filename}/No{no}-{name}.html", f"lastrun/alignment.html")

    return description_new


def highlight_hhs_full(hhs_file : str = "data/hhs/d1e0ta1.hhs"):
    """
    Returns the given hhs file as a colorized html formatted string.

    It's also stored within a separate folder
    /alignments_highlighted/<query-name>_full.html

    as well as in the /lastrun folder under the filename hhs_full_colorized.html.

    The functionalities itself are straight up copies of the get_full_alignment() functionalities.

    Within the string, helices and sheet patterns are colorized red and blue.
    :param hhs_file: the path of the hhs file of interest.
    :return: returns a string, which is HTML formatted. One could use Display(HTML(description_new)) to
             load it for example within Jupyter, or view the string within the separately created html file.
    """
    start = r'No 1'
    end = r'(Done!)'

    with open(hhs_file) as f:
        result = f.read()

    try:
        search_start = re.search(start, result).start()
        search_end = re.search(end, result).end()
    except:
        raise Exception("There appears to be no hits within your hhs file???")

    header = result[0:search_start].splitlines()
    header_new = str()
    for line in header:
        header_new = f"{header_new}\n<pre>{line}</pre>"

    hits = result[search_start:search_end].splitlines()
    hits_new = str()

    # regex for later, looking for sheets/helices within the description
    sheet = re.compile(r'E+', re.I)
    helix = re.compile(r'H+', re.I)

    # check each line in the description
    for x in hits:
        # get the name of the found target. Used later to create the filename.

        # Only look for ss_pred lines to colorize them.
        if x.startswith("Q ss_pred") or x.startswith("T ss_pred"):
            # offset, changing after each time something got colorized.
            offset = 0
            sheet_hits = sheet.finditer(x)

            # colorizing pattern for sheets.
            fonting_start = "<font color=blue>"
            fonting_end = "</font>"

            # colorizing sheet's entries. [1:] is just a simple workaround for the first "e" within ss_pred.
            for hit in list(sheet_hits)[1:]:
                x = f"{x[:hit.start()+offset]}{fonting_start}{x[hit.start()+offset:hit.end()+offset]}" \
                    f"{fonting_end}{x[hit.end()+offset:]}"
                offset += len(fonting_start) + len(fonting_end)

            # reset the offset to start with helices. God bless there's no "h" in the previous fonting_start/end.
            offset = 0
            helix_hits = helix.finditer(x)

            # colorizing pattern for helices.
            fonting_start = "<font color=red>"
            fonting_end = "</font>"

            # colorizing the helix's entries.
            for hit in helix_hits:
                x = f"{x[:hit.start()+offset]}{fonting_start}{x[hit.start()+offset:hit.end()+offset]}" \
                    f"{fonting_end}{x[hit.end()+offset:]}"
                offset += len(fonting_start) + len(fonting_end)

        # <pre>...</pre> secures the formatting of the html string to be presented correctly.
        # It is added to each line, securing each line's format.
        hits_new = hits_new + f"<pre>{x}</pre>\n"

    # last but not least, adding the query's information to the first line.
    hits_new = f"{header_new}\n{hits_new}"

    # getting the filename without the ending, needed to create subfolders for each query.
    filename = os.path.basename(hhs_file).split(".")[0]

    # just in case these folders don't exist yet.
    paths = ["lastrun", f"alignments_highlighted/"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    # storing the alignment within organized subfolders, but also into a folder holding information about the last run.
    with open(f"alignments_highlighted/{filename}_full.html", "w") as f:
        f.write(hits_new)

    copyfile(f"alignments_highlighted/{filename}_full.html", f"lastrun/hhs_colorized.html")

    return hits_new


def pymol_alignment(pdb_1,
                    pdb_2,
                    aln_term_1,
                    aln_term_2,
                    full_term_1,
                    full_term_2,
                    animation: bool = False,
                    framemultiplier : int = 1) -> list:
    """
    This function creates an alignment of two proteins, defined by the aln_term_x and full_term_x.
    The alignments are stored in a separate folder PyMol_img/<pdb_1>/<pdb_1>-<pdb_2>, as well as creating a .pse file
    in a separate pse folder pse/<pdb_1>. The last runned images are also stored into the folder lastrun.

    In case the user demands an animated image, the frames are stored into a subdir "animation", while the animated gif is
    saved in the PyMol_img/<pdb_1>/<pdb_1>-<pdb_2>/ dir, as well as in the lastrun folder.

    The function itself returns information about the
    Root-mean-square deviation of atomic positions (RMSD) values as a list.

    aln_term_1 is represented as cartoon, red.
    aln_term_2 is represented as cartoon, blue.

    all remainings:

    full_term_1 is represented as ribbon, yellow.
    full_term_2 is represented as ribbon, green.

    In some cases, full_term_X/aln_term_X are equal, therefor the created files no_zoom.png as well as zoom.png are
    identical to each other.

    :param pdb_1: one of the pdb_id's of the to aligning proteins.
    :param pdb_2: second of the pdb_id's of the to aligning proteins.
    :param aln_term_1:  allignment_term of the first protein. pattern example: '/1e0t//A/70-167/CA'
    :param aln_term_2: alignment_term of the second protein. pattern example: '/1e0t//A/70-167/CA'
    :param full_term_1: full_term of the first protein. Ignoring a residue span. E.g. '/1e0t//A//CA'
    :param full_term_2: full_term of the second protein. Ignoring a residue span. E.g. '/1e0t//A//CA'
    :param animation: if set to True, a gif animation will be created, alongside with every single frame of the
                      animation. It will be stored into the lastrun folder, as well as the specific created subdir.
    :param framemultiplier: int() between 1 and 4. Multiplies the amount of frames per 360° view. 1 = 14 images, 2 = 28 images, etc.
    :return: returns the rmsd value as a float.
    """

    if framemultiplier > 4 or framemultiplier < 1:
        raise Exception("framemultiplier can only be between 1 and 4.")
        return




    # using the names instead of the pdb_id's, in case there are cases where there are multiple hits for a single
    # pdb_id, but different segments. Very unlikely, but no harm to make sure.
    name_1 = aln_term_1.split("/")[1]
    name_2 = aln_term_2.split("/")[1]

    # create the paths for the folders, in case they don't exist.
    paths = ["cif", "lastrun", f"PyMol_img/{name_1}/{name_1}-{name_2}/", f"pse/{name_1}"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    # Delete the old animation in the last run folder in case a user decides against animation for this call.
    # So there's no/less confusion.
    try:
        send2trash("lastrun/animation_frames")
        send2trash("lastrun/animation_zoom.gif")
    except:
        pass

    # just clear the cache. In case of a previous run.
    cmd.delete('all')

    # No need to double load cif files. If they already exist, continue. Enables offline usage.
    if f"{pdb_1}.cif" not in os.listdir("cif"):
        cmd.fetch(pdb_1)
        os.rename(f"{pdb_1}.cif", f"cif/{pdb_1}.cif")
    else:
        cmd.load(f"cif/{pdb_1}.cif")

    if f"{pdb_2}.cif" not in os.listdir("cif"):
        cmd.fetch(pdb_2)
        os.rename(f"{pdb_2}.cif", f"cif/{pdb_2}.cif")
    else:
        cmd.load(f"cif/{pdb_2}.cif")

    # hide all loaded cif files.
    cmd.hide('everything')

    # align the two proteins
    rmsd = cmd.align(aln_term_1, aln_term_2, object='aln')
    cmd.hide("everything")

    # showing the full_term_X protein segments  as ribbon in different colors.
    cmd.show_as('ribbon', full_term_1)
    cmd.show_as('ribbon', full_term_2)
    cmd.color('yellow', full_term_1)
    cmd.color('green', full_term_2)

    # recolor the aln_term_X segments, as well as showing them as cartoon to clearly distinguish them easier and
    # make secondary structure more visible
    cmd.color('red', aln_term_1)
    cmd.show_as('cartoon', aln_term_1)
    cmd.color('blue', aln_term_2)
    cmd.show_as('cartoon', aln_term_2)

    # cmd.show("all")

    # zoom into the queries' part and store everything as "no_zoom".
    cmd.zoom(full_term_1, complete = 1)

    # store the no-zoom in the dedicated subfolder, as well as creating a .pse file and copy the image/pse
    # into the last run folder
    cmdPNG(f'PyMol_img/{name_1}/{name_1}-{name_2}/no_zoom.png', dpi=300, ray=3)
    copyfile(f'PyMol_img/{name_1}/{name_1}-{name_2}/no_zoom.png', f'lastrun/no_zoom.png')

    cmd.save(f'pse/{name_1}/{name_1}-{name_2}-no_zoom.pse')
    copyfile(f'pse/{name_1}/{name_1}-{name_2}-no_zoom.pse', f'lastrun/no_zoom.pse')

    # zoom into the aln_term_1 area of the presentation, and also hide everything else.
    cmd.zoom(aln_term_1, complete = 1)
    cmd.hide("ribbon")
    cmd.bg_color('white')
    cmdPNG(f'PyMol_img/{name_1}/{name_1}-{name_2}/main_zoom.png', dpi=300, ray=3)
    # storing the zoomed picture into the lastrun folder, as well as a dedicated folder for each query.
    copyfile(f'PyMol_img/{name_1}/{name_1}-{name_2}/main_zoom.png', f'lastrun/main_zoom.png')

    # in case the user wants to have an animation of the alignment, rotating around the y-axis..
    if animation == True:
        paths = [f"lastrun/animation_frames/",
                 f"PyMol_img/{name_1}/{name_1}-{name_2}/animation_frames/{framemultiplier}/"]
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

        # Clean up the old animation folder in the lastrun folder, in case the user
        # switches up with the frame multipliers.
        try:
            old_animation = os.listdir(f'lastrun/animation_frames/')
            for file in old_animation:
                send2trash(f'lastrun/animation_frames/{file}')
        except:
            pass

        # create each frame for a full 360 turn.
        for x in range(1, 15*framemultiplier):
            cmdPNG(f'PyMol_img/{name_1}/{name_1}-{name_2}/animation_frames/{framemultiplier}/{x}-zoom.png', dpi=300, ray=3)
            copyfile(f'PyMol_img/{name_1}/{name_1}-{name_2}/animation_frames/{framemultiplier}/{x}-zoom.png',
                     f'lastrun/animation_frames/{x}-zoom.png')
            cmd.rotate("y", round(24/framemultiplier))

        # get the full list of the created frames and sort them by the starting number.
        files = os.listdir(f'PyMol_img/{name_1}/{name_1}-{name_2}/animation_frames/{framemultiplier}/')
        files.sort(key=lambda x: int(x.strip('-zoom.png')))
        frames = list()

        # double-check to only consider .png. theoretically not necessary, just fallback check.
        for file in files:
            if not file.endswith(".png"):
                continue
            with Image.open(f"PyMol_img/{name_1}/{name_1}-{name_2}/animation_frames/{framemultiplier}/{file}") as f:
                frame = f.convert("RGBA")
            # setting the alpha channel as mask, so the "whitened" layers in the bakcground of the protein are
            # eventually also presented as such in the gif. Gives a better visual effect & representation of depth.
            bg = Image.new("RGBA", frame.size, (255, 255, 255, 255))
            bg.paste(frame, mask=frame.getchannel("A"))
            frames.append(bg)

        # create the actual animation, with a duration of 0.2 seconds for each frame.
        frames[0].save(f'PyMol_img/{name_1}/{name_1}-{name_2}/{framemultiplier}-animation_zoom.gif',
                       save_all=True,
                       append_images=frames[1:],
                       duration=170,
                       loop=0)
        copyfile(f'PyMol_img/{name_1}/{name_1}-{name_2}/{framemultiplier}-animation_zoom.gif', f'lastrun/animation_zoom.gif')

    # return the RMSD (float()) in Angström.
    return rmsd


def read_in_frequencies(hhmfile: str = "data/hhm/d1a2oa1.hhm") -> pd.DataFrame:
    """
    Read in only the frequencies, based on the hidden markov model, of each amino acid within a .hhm file.

    The data is stored within a .csv file, where each line represents an amino acid, while each cell is separated
    by a semicolon.

    Returned is a pandas DataFrame with the information with the extracted information. The index is here the
    position within the sequence.

    Before storing the frequencies within the .csv file and the pandas DataFrame, they are actually calculated
    to represent the frequencies directly. (https://github.com/soedinglab/hh-suite/wiki)

    Frequency calculation:
        entry = -1000 * log_2(frequency)
     -> frequency = 2^(-entry/1000)

    Example for the DataFrame:

            AS  A         C         D         E         F         G         H         I         K          (...)
    Pos
    1       M1  0.030019  0.000000  0.004325  0.014670  0.037111  0.012379  0.000000  0.020847  0.013471   (...)
    (...)


    :param hhmfile: the path to the hhmfile of interest.
    :return: returns a pandas DataFrame of the frequencies only.
    """

    # creating path in case they don't exist.
    if not os.path.exists("lastrun"):
        os.makedirs("lastrun")

    with open(hhmfile) as f:
        buffer = f.read()

    # framing the frequencies only. Interesting part starts with #, ends with //.
    s_pattern = re.compile(r"^#", re.M)
    e_pattern = re.compile(r"^//", re.M)
    start = re.search(s_pattern, buffer)
    end = re.search(e_pattern, buffer)

    HHM_modeling = buffer[start.end():end.start()]
    HHM_modeling = HHM_modeling.splitlines()

    # Only take in the lines which start with an actual amino acid, ignore the HMM information in each follow up line.
    frequency_pattern = re.compile(r"[A-Z] [1-9]+", re.I)

    # iterate over the lines
    for line in HHM_modeling:
        # get the amino acids from the header line.
        # Also defining the string which later is used to store the data into a .csv file.
        if line.startswith("HMM"):
            only_frequencies = "Pos\tAS\t" + line.split(maxsplit=1)[1]
            only_frequencies = ";".join(only_frequencies.split("\t")).strip(";")

        # check if the line is actually a AS line.
        search = frequency_pattern.search(line)
        if search:
            # split up the line's cells.
            line = line.split()
            # defining the frequency cells.
            frequencies = line[2:-1]
            # store the position which is at the end of each line separate.
            pos = line[-1]
            # get rid of the space between the amino acid and the Pos.
            aminoacid = f"{line[0]}{line[1]}"

            # build up a list to calculate the frequencies
            converted_frequencies = list()

            for x in frequencies:
                # "*" are considered as 0.
                if x == "*":
                    converted_frequencies.append(0)
                else:
                    # from https://github.com/soedinglab/hh-suite/wiki
                    #    entry      = -1000 * log_2(frequency)
                    # <-> frequency = 2^(-entry/1000)
                    frequency = 2 ** (-int(x) / 1000)
                    converted_frequencies.append(frequency)

            # build up the converted line.
            converted_complete = f"{pos};{aminoacid};"
            converted_complete = converted_complete + ";".join(map(str, converted_frequencies))
            converted_complete = f"{converted_complete}"
            # append the previous created only_frequencies str()
            only_frequencies = f"{only_frequencies}\n{converted_complete}"

    # store the created string within a "frequencies.csv" file.
    with open("lastrun/frequencies.csv", "w") as f:
        total = f"{only_frequencies}".strip("\n").strip(";")
        f.write(total)

    # create a DataFrame of the created .csv file, declaring the position column as index and return this DataFrame.
    dataread = pd.read_csv("lastrun/frequencies.csv", header=0, delimiter=";", index_col=0)

    return dataread


def plot_frequencies(dataread,
                     name: str = "output",
                     threshold: float = 0.1,
                     span_start: int = 1,
                     span_end: int = 50,
                     filename: str = "barplot.png",
                     title: bool = False):
    """
    This function creates a barplot based on frequencies of a previous created pandas DataFrame based on an .hmm file.
    The DataFrame can be created using the read_in_frequencies() function of this module.

    The created barplot is stored into a separate folder barplots/<name>-<span_start>-<span_end>-<treshold>.png,
    as well as in the lastrun folder as the desired "filename" argument.

    :param dataread: a pandas DataFrame with only the amino acids' frequencies, taken out of a .hhm file.
                     This DataFrame can be created by using the read_in_frequencies() function of this module.
    :param name: The name of the query e.g. d1ka9f_. Used to properly store the file later into a subfolder.
                 barplots/<name>-<span_start>-<span_end>-<treshold>.png
    :param treshold: The treshold of the frequency, in percentage %.
    :param span_start: The start point within the residues which you like to be plotted.
    :param span_end: The end point within the residues which you like to be plotted.
    :param filename: The desired filename within the "lastrun" folder.
    :param title: In case a title is wished. Personal prefererence is not to have it.
    :return: Nothing. Creates .png files.
    """

    # creating paths, in case they don't exist yet.
    paths = ["lastrun", f"barplots/{name}"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    # create a DataFrame which only contains values exceeding the given threshold.
    # limit the comparison to only the columns which should include floats.
    # On windows this was not needed.. But when tested on MAC, it ended up in an Exception..
    column_names = list(dataread)[1:]
    criteria = dataread[dataread[column_names] > threshold]
    # reducing the DataFrame to only represent the information within the defined range.
    criteria = criteria.iloc[span_start - 1:span_end]
    # resizing fonts before then creating the plot.
    matplotlib.rcParams.update({'font.size': 8})
    plot = criteria.plot.bar(stacked=True, linewidth=1, colormap='tab20')  # figsize = [25,25], width = 1,

    # labeling the axis.
    plt.xlabel('position', fontsize=12)
    plt.ylabel('frequency', fontsize=12)

    # print a tile on the graph, in case one desires it.
    if title:
        plt.title(f"{name} - from pos. {span_start} to {span_end} - frequency treshold {round(threshold*100)}%",
                  fontsize=30)

    # resize the font for the Legend.
    matplotlib.rcParams.update({'font.size': 10})
    lgd = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                     ncol=2, mode="expand", borderaxespad=0.)

    # resize the whole graph.
    plt.gcf().set_size_inches(20, 10)

    # store the graphs into the given folders.
    plt.savefig(f"barplots/{name}/{name}-{span_start}-{span_end}-{round(threshold*100)}.png", dpi=300,
                bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.savefig(f'lastrun/{filename}', dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')

    plt.close()

    return