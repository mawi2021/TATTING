#from curses.ascii import isdigit
from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QHBoxLayout, QFileDialog, QScrollArea
from PyQt5 import QtWidgets
from PyQt5 import QtSvg
from PyQt5.QtCore import Qt
from os.path import exists
import re  # regular expressions)"/> 
import math
import ctypes # for messages
import json

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # ----- Constants ----------------------------------------------------------------------- #
        # TODO: read values from config file
        self.elems = []
        self.picot = {}
        self.scale = 20    # realistic view with A4 paper in background an 5mm grid lines
        self.grid  = 'yes' # String!
        self.svg   = ''    # Content of SVG data
        self.paperwidthMM = 3000
        self.paperheightMM = 3000
        self.pix_x = self.paperwidthMM * 10
        self.pix_y = self.paperheightMM * 10
        self.kast = 50 # => 5mm = 1 Kästchen (when ViewBox has 10 times pixel as mm of "paper" size)
        self.defaultColor = 'black'

        # Instruction as Text #
        self.textWidget = QTextEdit()
        self.txtFilename = ''

        # Instruction as SVG Image #
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50,50,759,668)
        self.svgWidget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
        self.svgWidget.setSizePolicy(QtWidgets.QSizePolicy(0,0))
        self.svgFilename = ''

        self.scrollArea = QScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.svgWidget)

        # Combine Instructions with Splitter
        designSplitter = QSplitter(Qt.Horizontal)
        designSplitter.addWidget(self.textWidget)
        designSplitter.addWidget(self.scrollArea)
        designSplitter.setSizes([50,150])

        hbox = QHBoxLayout()
        hbox.addWidget(designSplitter)
        self.layout = hbox
        self.setLayout(self.layout)

    # ===== PUBLIC METHODS ====================================================================== #
    def onNew(self):
        fileDlg = QFileDialog()
        fileStruc = fileDlg.getSaveFileName( 
                        self.parent, 'Choose a directory and enter a new filename (text)', 
                        "samples/"
                    )

        # Stop if nothing chosen #
        if fileStruc[0] == "":
            return

        # Set filenames #
        self.txtFilename = fileStruc[0]
        pos = self.txtFilename.rfind('.')
        if pos >= 0:
            self.svgFilename = self.txtFilename[:pos+1] + 'svg'
        else:
            self.svgFilename = self.txtFilename + '.svg'

        # Start with empty panes #
        self.textWidget.clear()
        self.onRedraw()
    def onOpen(self):
        # Reguest filename #
        fileDlg = QFileDialog()
        fileStruc = fileDlg.getOpenFileName( 
                        self.parent, 'Choose a file with instructions (text)', "samples/"
                    )

        # Stop if nothing chosen #
        if fileStruc[0] == "":
            return

        # Set filenames #
        self.txtFilename = fileStruc[0]
        pos = self.txtFilename.rfind('.')
        if pos >= 0:
            self.svgFilename = self.txtFilename[:pos+1] + 'svg'
        else:
            self.svgFilename = self.txtFilename + '.svg'

        self.open()
    def onRedraw(self):
        # Read plain text instructions #
        content = self.textWidget.toPlainText()
        lines = content.split('\n')
        self.svg = ''
        self.elems = []
        self.picot = {}

        # Recalculate svg string #
        self._create_meta(lines)
        for line in lines:
            self._add(line)
        self.svg = self.svg + '</svg>'

        # Show SVG string #
        self.svgWidget.load(bytearray(self.svg, encoding='utf-8'))
        self.svgWidget.resize(round(self.paperwidthMM * 10), round(self.paperheightMM * 10))
    def onSave(self):
        content = self.textWidget.toPlainText()
        
        with open(self.txtFilename, 'w', encoding="utf-8") as f:
            f.write(content)
        f.close() 

        with open(self.svgFilename, 'w', encoding="utf-8") as f:
            f.write(self.svg)
        f.close() 
    def onSaveAs(self):
        fileDlg = QFileDialog()
        fileStruc = fileDlg.getSaveFileName( 
                        self.parent, 'Choose a directory and enter a new filename (text)',
                        "samples/"
                    )

        # Stop if nothing chosen #
        if fileStruc[0] == "":
            return

        # Set filenames #
        self.txtFilename = fileStruc[0]
        pos = self.txtFilename.rfind('.')
        if pos >= 0:
            self.svgFilename = self.txtFilename[:pos+1] + 'svg'
        else:
            self.svgFilename = self.txtFilename + '.svg'

        # Save current content #
        content = self.textWidget.toPlainText()
        
        with open(self.txtFilename, 'w', encoding="utf-8") as f:
            f.write(content)
        f.close() 

        with open(self.svgFilename, 'w', encoding="utf-8") as f:
            f.write(self.svg)
        f.close() 
    def onZoomIn(self):
        self.kast          = self.kast * 1.1
        self.scale         = self.scale / 1.1
        self.onRedraw()
    def onZoomOut(self):
        self.kast          = self.kast / 1.1
        self.scale         = self.scale * 1.1
        self.onRedraw()

    def open(self):
        # Read text file and assign content #
        if exists(self.txtFilename):
            with open(self.txtFilename, encoding="utf-8") as f:
                instr = ''
                for line in f.readlines():
                    instr = instr + line
                self.textWidget.setPlainText(instr)
            f.close()
        else:
            self.txtFilename = ''
            self.svgFilename = ''

        # Show SVG file #
        self.onRedraw()

    # ===== PRIVATE PART OF CLASS =============================================================== #
    def _create_meta(self, lines):
        self.svg = self.svg + '<?xml version="1.0" encoding="UTF-8"?>\n' \
                + '<svg xmlns="http://www.w3.org/2000/svg"\n' \
                + '    xmlns:xlink="http://www.w3.org/1999/xlink"\n' \
                + '    version="1.1" baseProfile="full"\n' \
                + '    width="%dmm" height="%dmm"\n' % (self.paperwidthMM,self.paperheightMM) \
                + '    viewBox="0 0 ' + str(self.pix_x) + ' ' + str(self.pix_y) + '">\n' \
                + '    <rect width="' + str(self.pix_x) + '" height="' + str(self.pix_y) \
                + '" style="fill:white;stroke-width:1;stroke:rgb(0,0,0)"/>\n' \
                + '\n<!-- File Content -->\n'

        # Draw Grid in whole "paper area" #
        if self.grid == 'yes':
            self.svg = self.svg + '\n<!-- Grid -->\n'
            i = 0
            while i <= self.pix_x:
                self.svg = self.svg + '<line x1="' + str(i) + '" y1="0" x2="' + str(i) + '" y2="' \
                    + str(self.pix_y) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + self.kast
            i = 0
            while i <= self.pix_y:
                self.svg = self.svg + '<line y1="' + str(i) + '" x1="0" y2="' + str(i) + '" x2="' \
                    + str(self.pix_x) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + self.kast

        # Read basic elements from /config/basic_elements.svg file and replace it here
        found = False
        next_is_coord = False
        fig_id = ''
        self.svg = self.svg + '<!-- Basic Elements -->\n'
        with open('config/basic_elements.svg', 'r', encoding="utf-8") as fr:                
            for line in fr.readlines():
                if line == '' or line == '\n':
                    continue

                if next_is_coord:
                    line = line[+4:-4]
                    coord_arr = line.split(' ')
                    self.picot[fig_id] = []
                    first = True
                    for coord in coord_arr:
                        coord = json.loads(coord)
                        if first:
                            dx = coord[0]
                            dy = coord[1]
                            element = {}
                            element["id"] = fig_id
                            element["dx"] = dx
                            element["dy"] = dy
                            element["nodes"] = 1
                            self.elems.append(element)
                            first = False
                            continue
                        self.picot[fig_id].append(coord)
                    next_is_coord = False
                    continue

                if line.startswith('<!-- ### START PART TO BE COPIED ### -->'):
                    found = True
                    continue
                if line.startswith('<!-- ### END PART TO BE COPIED ### -->'):
                    found = False
                    continue
                if not found: continue
                self.svg = self.svg + line
                reg = re.search('id=\"[^\"]*\"', line)
                if reg == None: continue
                fig_id = reg.group(0)
                fig_id = fig_id[4:-1]
                next_is_coord = True

            self.svg = self.svg + '\n<!-- Individual Part -->\n'
    def _add(self,line):
        if len(line) == 0: return
        if line[0] == '#': return

        # Parse line
        element = {}
        regexp = '\{[-]*[0-9]+\}'
        coord_x = coord_y = -1

        # Initial values
        element["color"] = ''

        # Get identifier (name) of this object => element["id"]
        pos = line.find(':')
        if pos == -1:
            ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                '\nNo ":" in this line', 'Error', 0)
            return
        element["id"] = line[:pos].strip()

        # Degree of "opening angle" in a ring or ratio of a chain length:height in [..] 
        # => element["degree"] or element["ratio"]
        pos1 = element["id"].find('[')
        pos2 = element["id"].find(']')

        if pos1 >= 0 and pos2 >= 0:
            if element["id"][0] == 'R':
                element["degree"] = element["id"][pos1+1:pos2]
            elif element["id"][0] == 'C':
                element["ratio"] = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]

        else: # Default Values
            if element["id"][0] == 'R':
                element["degree"] = '60'
            elif element["id"][0] == 'C':
                element["ratio"] = '5'

        # Definition of element (everything after ":" => element["def"]
        element["def"] = line[pos+1:].strip()

        # Additional Instructions such as coloring in {..}
        pos1 = element["id"].find('{')
        pos2 = element["id"].find('}')
        if pos1 >= 0 and pos2 >= 0:
            instr = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
            instrList = instr.split(',')
            for instrTxt in instrList:
                pos3 = instrTxt.find('=')
                if pos3 >= 0:
                    key = instrTxt[:pos3]
                    val = instrTxt[pos3+1:]
                    if key == 'color':
                        element["color"] = val          

        # Output coordinates if available in (..) => coord_x, coord_y
        pos1 = element["id"].find('(')
        pos2 = element["id"].find(')')
        if pos1 >= 0 and pos2 >= 0:
            coords = element["id"][pos1+1:pos2]
            element["id"] = element["id"][:pos1]
            pos = coords.find(',')
            coord_x = int(coords[:pos])
            coord_y = int(coords[pos+1:])
        
        # How many nodes (including picots)? => element["nodes"]
        seq = element["def"]
        seq = seq.replace("p","1")
        seq = seq.replace("P","1")
        seq = seq.replace(" ","+")
        for e in self.elems:
            seq = seq.replace(e["id"],str(e["nodes"]))
        seq = re.sub(regexp, '', seq, 0, 0)
        try:
            element["nodes"] = eval(seq)
        except NameError:
            ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                '\nAn expression in this line is not yet defined', 'Error', 0)
            return
        except SyntaxError:
            ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                '\nSyntax error, e.g. check space, colons and brackets', 'Error', 0)
            return
       
        # Ring (start + end on top) or Chain with mid on top (start left) #
        # Size of Rings and Chains must be scaled according to the number of nodes
        # elements consisting of such scaled rings and chains do not need to be scaled
        scale = 500 * element["nodes"] / self.scale          # figure scale factor

        if element["id"][0] == 'R':
            if element["degree"].isdigit():
                winkel_grad = int(element["degree"])
                winkel_rad = math.radians(winkel_grad)
                element["dx"] = 0
                element["dy"] = 0
                b = scale

                # no clue why factor 500 :-( #
                # len_straight = 500 * scale / (2 * (1 + math.pi \
                #                 * math.tan(winkel_rad/2) * (0.5 - winkel_rad/360)))
                # r  = len_straight * math.tan(winkel_rad/2)
                # umfang_circle = 2 * math.pi * r * ((math.pi + winkel_rad) / (2 * math.pi) )
                r = b / (math.pi * (1 + winkel_grad/180) + 2/math.tan(winkel_rad/2))
                len_straight = r / math.tan(winkel_rad/2)
                x1 = -len_straight * math.sin(winkel_rad/2)
                y1 =  len_straight * math.cos(winkel_rad/2)
                ym = r / math.sin(winkel_rad/2)
                umfang_circle = math.pi * r * (1 + (winkel_grad / 180) )
                umfang = 2 * len_straight + umfang_circle

                self.svg = self.svg + '<g id="' + element["id"] + '" fill="none" stroke-linecap="round" stroke-width="2">\n' \
                                    + '   <path d="M 0,0   L ' + str(x1) + ',' + str(y1) \
                                    + '   A ' + str(r) + ',' + str(r) + ' 0, 1, 0 ' + str(-x1) + ',' + str(y1) \
                                    + '   Z" />\n'

                # Picots?
                seq = element["def"].split(' ')
                pos = 0
                for el in seq:
                    if el.isdigit():
                        #pos = pos + int(el)
                        for i in range(int(el)):
                            pos = pos + 0.5
                            verhaeltnis = pos / element["nodes"]
                            part = umfang * verhaeltnis

                            if part < len_straight:
                                # Picot in first, straight part of ring #
                                x = x1 * part / len_straight
                                y = y1 * part / len_straight
                                # winkel_picot = 90 + winkel_grad / 2
                            elif umfang - part < len_straight:
                                # Picot in second, straight part of ring #
                                x = -x1 * (umfang - part) / len_straight
                                y =  y1 * (umfang - part) / len_straight
                                # winkel_picot = 270 - winkel_grad / 2
                            else:
                                # Picot in circle part of ring #
                                part_circle = part - len_straight
                                beta_grad = (180 + winkel_grad) * part_circle / umfang_circle
                                x =      r * math.cos(math.radians((winkel_grad/2) - beta_grad))
                                y = ym - r * math.sin(math.radians((winkel_grad/2) - beta_grad))
                                # winkel_picot = 270 - winkel_grad/2 + beta_grad
                            pos = pos + 0.5
                            self.svg = self.svg + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="5" />\n'
                    else:
                        # calculate coords, where to add
                        pos = pos + 0.5
                        if el == 'P':
                            scale_picot = 40 / self.scale 
                        elif el == 'p':
                            scale_picot = 40 / (self.scale * 3)
                            
                        verhaeltnis = pos / element["nodes"]
                        part = umfang * verhaeltnis

                        if part < len_straight:
                            # Picot in first, straight part of ring #
                            x = x1 * part / len_straight
                            y = y1 * part / len_straight
                            winkel_picot = 90 + winkel_grad / 2
                        elif umfang - part < len_straight:
                            # Picot in second, straight part of ring #
                            x = -x1 * (umfang - part) / len_straight
                            y =  y1 * (umfang - part) / len_straight
                            winkel_picot = 270 - winkel_grad / 2
                        else:
                            # Picot in circle part of ring #
                            part_circle = part - len_straight
                            beta_grad = (180 + winkel_grad) * part_circle / umfang_circle
                            x =      r * math.cos(math.radians((winkel_grad/2) - beta_grad))
                            y = ym - r * math.sin(math.radians((winkel_grad/2) - beta_grad))
                            winkel_picot = 270 - winkel_grad/2 + beta_grad
                        pos = pos + 0.5

                        self.svg = self.svg + '   <use  xlink:href="#picot" ' \
                                    + 'transform="translate(' + str(x) + ' ' + str(y) + ') '\
                                    + 'rotate(' + str(winkel_picot) + ') ' \
                                    + 'scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')"/>\n'

                self.svg = self.svg + '</g>\n'  

            else:                      
                ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                    '\nOpening degree in [..] is not a digit', 'Error', 0)
                return

        # Chains C => 
        elif element["id"][0] == 'C':
            if element["ratio"].isdigit():
                ratio = int(element["ratio"])
                alpha_rad = math.acos( 1 - ( 8 / ( ratio * ratio + 4 ) ) )
                b = scale 
                r = b / ( 2 * alpha_rad )
                x1 = 2 * r * math.sin(alpha_rad)
                y1 = 0
                element["dx"] = x1
                element["dy"] = y1

                self.svg = self.svg + '<g id="' + element["id"] + '" fill="none" stroke-linecap="round" stroke-width="2">\n' \
                                    + '   <path d="M 0,0' \
                                    + '   A ' + str(r) + ',' + str(r) + ' 0, 0, 1 ' + str(x1) + ',' + str(y1) + '" />\n'

                # Picots?
                seq = element["def"].split(' ')
                pos = 0
                gamma_rad = math.pi / 2 - alpha_rad # angle between horizontal diameter and start of chain
                for el in seq:
                    if el.isdigit():
                        # for each node add a little circle
                        for i in range(int(el)):
                            pos = pos + 0.5
                            verhaeltnis = pos / element["nodes"]
                            beta_rad = 2 * alpha_rad * verhaeltnis
                            x = x1 / 2 - r * math.cos(beta_rad + gamma_rad)
                            y = -r * ( math.sin(beta_rad + gamma_rad) - math.cos(alpha_rad) )

                            pos = pos + 0.5
                            self.svg = self.svg + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="5" />\n'
                    else:
                        # calculate coords, where to add
                        pos = pos + 0.5
                        if el == 'P':
                            scale_picot = 40 / self.scale 
                        elif el == 'p':
                            scale_picot = 40 / (self.scale * 3)
                            
                        verhaeltnis = pos / element["nodes"]
                        beta_rad = 2 * alpha_rad * verhaeltnis
                        x = x1 / 2 - r * math.cos(beta_rad + gamma_rad)
                        y = -r * ( math.sin(beta_rad + gamma_rad) - math.cos(alpha_rad) )
                        alpha_picot = 180 - math.degrees(alpha_rad/2) + math.degrees(beta_rad)

                        pos = pos + 0.5
                        # self.svg = self.svg + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="15" />\n'
                        self.svg = self.svg + '   <use  xlink:href="#picot" ' \
                                    + 'transform="translate(' + str(x) + ' ' + str(y) + ') '\
                                    + 'rotate(' + str(alpha_picot) + ') ' \
                                    + 'scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')"/>\n'

                self.svg = self.svg + '</g>\n'  

            else:
                ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                    '\nRatio of chains length : height in [..] is not a digit', 'Error', 0)
                return

        # Figures #
        else:
            # Starting point for next element of the figure; in the end this is the end coordinate
            dx = 0
            dy = 0

            # Start of figure
            self.svg = self.svg + '<g id="' + element["id"] + '" fill="none" stroke-linecap="round">\n'

            lst = element["def"].split(" ")
            for figure in lst:
                # Angle in form: {..} as degree-value >> if available, recalculate to radiant #
                grad = 0
                rad = 0
                regex = re.search(regexp, figure)
                if regex:
                    grad = float(regex.group(0)[1:-1])
                    rad = math.radians(grad)

                # Get figure = Name of element without angle in form: {..} #
                figure = re.sub(regexp, '', figure, 0, 0)

                # Draw element #
                self.svg = self.svg + '   <use xlink:href="#' + figure + '" ' \
                            + 'transform="translate(' + str(dx) + ' ' + str(dy) + ') '\
                            + 'rotate(' + str(grad) + ')"/>\n'

                # Calculate dx and dy for figure #
                for el in self.elems:
                    if el["id"] == figure:
                        dx = dx + el["dx"] * math.cos(rad) - el["dy"] * math.sin(rad)
                        dy = dy + el["dx"] * math.sin(rad) + el["dy"] * math.cos(rad)

            # End of figure and end coordinate
            self.svg = self.svg + '</g>\n'
            element["dx"] = dx
            element["dy"] = dy

        # Output of figure #
        if coord_x >= 0 and coord_y >= 0:
            if element["color"] == '':
                element["color"] = self.defaultColor
            self.svg = self.svg + '<!-- Output -->\n'
            self.svg = self.svg + '<g stroke="' + element["color"] + '" fill="none" stroke-width="1" stroke-linecap="round">\n'
            self.svg = self.svg + '   <use xlink:href="#' + element["id"] \
                                + '" transform="translate(' + str(coord_x*20/self.scale) + ' ' + str(coord_y*20/self.scale) + ')"/>\n'
            self.svg = self.svg + '</g>\n'
            #self.svg = self.svg + '<circle cx="' + str(coord_x*20/self.scale) + '" cy="' + str(coord_y*20/self.scale) + '"  r="10" style="fill:red" />\n'

        self.elems.append(element)