from pickle import FALSE, TRUE
from PyQt5.QtWidgets import QWidget, QSplitter, QTextEdit, QHBoxLayout, QFileDialog, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from os.path import exists
import re  # regular expressions)"/> 
import math
import ctypes # for messages

# Info-Messages: self.parent.statusBar().showMessage("Hallo Welt")

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.titleConst = 'TaDes (Tatting Design Studio)'

        # ----- Constants ----------------------------------------------------------------------- #
        # TODO: read values from config file
        self.elems = []
        self.svg   = ''    # Content of SVG data
        self.paperwidthMM = 210
        self.paperheightMM = 297
        self.defaultColor = '#4287f5'
        self.manualColor = '#fa6b05'
        self.textline = 1
        
        # Values, that can be toggled via Menu
        self.grid         = 'yes' # String!
        self.node_circles = 'yes' # String!
        self.image_frame  = 'yes' # String!

        # Instruction as Text #
        self.textWidget = QTextEdit()
        self.txtFilename = ''

        # Instruction as SVG Image #
        self.svgWidget = QWebEngineView()
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
        self.textline = 1

        self._create_meta(lines)

        # Recalculate svg string #
        for line in lines:
            self._add(line)
        self.textline = self.textline + 0.5
        self.svg = self.svg \
                 + '<text x="100" y="' + str(150 + self.textline * 70) \
                 + '" style="font-size:50px" text-decoration="underline">Image Manual:</text>\n' \
                 + '</svg>'

        # Show SVG string #
        self.svgWidget.setHtml(self.svg, QUrl('file://'))
        self.svgWidget.resize(round(self.paperwidthMM * 10), round(self.paperheightMM * 10))
        self.parent.setWindowTitle(self.titleConst + ' - ' + self.svgFilename)
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
    def _drawGrid(self):
        if self.grid == 'yes':
            self.svg = self.svg + '\n<!-- Grid -->\n'

            # vertical lines
            i = 0
            while i <= self.paperwidthMM * 10:
                self.svg = self.svg + '<line x1="' + str(i) + '" y1="0" x2="' + str(i) + '" y2="' \
                    + str(self.paperheightMM * 10) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + 50 # 50 pixel = 5 mm = 1 box on paper

            # horizontal lines
            i = 0
            while i <= self.paperheightMM * 10:
                self.svg = self.svg + '<line y1="' + str(i) + '" x1="0" y2="' + str(i) + '" x2="' \
                    + str(self.paperwidthMM * 10) + '" stroke="lightgrey" stroke-width="1px" />\n'
                i = i + 50 # 50 pixel = 5 mm = 1 box on paper
        
    def _create_meta(self, lines):
        # Header Part #
        self.svg = self.svg + '<?xml version="1.0" encoding="UTF-8"?>\n' \
                + '<svg xmlns="http://www.w3.org/2000/svg"\n' \
                + '    xmlns:xlink="http://www.w3.org/1999/xlink"\n' \
                + '    version="1.1" baseProfile="full"\n' \
                + '    width="%dmm" height="%dmm"\n' % (self.paperwidthMM,self.paperheightMM) \
                + '    viewBox="0 0 ' + str(self.paperwidthMM * 10) + ' ' + str(self.paperheightMM * 10) + '">\n' \
                + '    <rect width="' + str(self.paperwidthMM * 10) + '" height="' + str(self.paperheightMM * 10) \
                + '" style="stroke:rgb(0,0,0)" fill="#f5fdff"/>\n' \
                + '\n<!-- File Content -->\n' \
                + '<text id="TEXT" x="100" y="100" ' \
                       + 'style="font-size:42;font-weight:bold;fill:#c0c0c0' \
                       + '">Manual created with TADES, see https://github.com/mawi2021/TATTING</text>\n'

        # Draw Grid in whole "paper area" #
        self._drawGrid()

        # Read basic elements from /config/basic_elements.svg file and replace it here
        fig_id = ''
        self.svg = self.svg + '<!-- Basic Elements -->\n'
        with open('config/basic_elements.svg', 'r', encoding="utf-8") as fr:                
            for line in fr.readlines():
                if line == '' or line == '\n':
                    continue

                self.svg = self.svg + line
                reg = re.search('id=\"[^\"]*\"', line)
                if reg == None: continue
                fig_id = reg.group(0)
                fig_id = fig_id[4:-1]

        self.svg = self.svg \
                 + '<text x="100" y="' + str(150 + self.textline * 70) \
                 + '" style="font-size:50px" text-decoration="underline">Text Manual:</text>\n' \
                 + '\n<!-- Individual Part -->\n'
        self.textline = self.textline + 1

    def _add(self,line):
        if len(line) == 0: return
        if line[0] == '#': return

        # Parse line
        element = {}
        regexp = '\{[-]*[0-9]+\}'
        coord_x = coord_y = -1

        # Initial values
        element["color"] = ''
        font_size   = '50px'
        font_size_half = 20
        font_width_half = 10
        font_style  = ''
        font_weight = ''
        fill        = ''
        img_height  = ''
        img_width   = ''
        text_decoration = ''

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
                    element[key] = instrTxt[pos3+1:]

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
        if element["id"][0] in ('R', 'C'):
            seq = element["def"]
            seq = seq.replace("p","1")
            seq = seq.replace("P","1")
            seq = seq.replace(" ","+")
            for e in self.elems:
                if "nodes" in e:
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
            scale = 25 * element["nodes"]   # one node is 25px wide

        # ========================= #
        # =====    T E X T    ===== #
        # ========================= #
        if element["id"] == 'TEXT':
            if 'font-size' in element: font_size = element["font-size"]
            if coord_x < 0: coord_x = 100
            if coord_y < 0: coord_y = 100
            if 'font-style'  in element: font_style  = 'font-style:' + element["font-style"] + ';'                     
            if 'font-weight' in element: font_weight = 'font-weight:' + element["font-weight"] + ';'
            if 'fill'        in element: fill        = 'fill:' + element["fill"] + ';'
            if 'text-decoration' in element: 
                text_decoration = 'text-decoration="' + element["text-decoration"] + '" '

            self.svg = self.svg + '<text id="TEXT" x="' + str(coord_x) + '" y="' + str(coord_y) + '" ' \
                       + 'style="font-size:' + font_size + ';' + font_style + font_weight + fill \
                       + '" ' + text_decoration + '>' + element["def"] + '</text>\n'
            return

        # ========================= #
        # =====   I M A G E   ===== #
        # ========================= #
        elif element["id"] == 'IMAGE':
            if 'height' in element: 
                img_height = ' height="' + element["height"] + '"'
            else: 
                img_height = ' height="500"'
            if 'width'  in element: 
                img_width  = ' width="'  + element["width"]  + '"'
            else: 
                img_width  = ' width="500"'

            # Frame
            if self.image_frame == 'yes':
                self.svg = self.svg + '<!-- Image with Frame -->\n' \
                        + '<svg>\n<filter id="dropshadow"><feDropShadow dx="20" dy="20" stdDeviation="3" flood-opacity="0.3" /></filter>' \
                        + '<rect ' \
                        + 'x="' + str(coord_x) + '" y="' + str(coord_y) + '"' + img_height + img_width \
                        + ' style="fill:white;stroke-width:1;stroke:black;filter:url(#dropshadow)" /></svg>\n'
            # Embedded Image
            self.svg = self.svg + '<image xlink:href="' + element["def"] \
                     + '" x="' + str(coord_x) + '" y="' + str(coord_y) + '"' \
                     + img_height + img_width + '/>\n'
            return

        # ========================= #
        # =====    R I N G    ===== #
        # ========================= #
        elif element["id"][0] == 'R':
            if element["degree"].isdigit():
                winkel_grad = int(element["degree"])
                winkel_rad = math.radians(winkel_grad)
                element["dx"] = 0
                element["dy"] = 0

                r = scale / (math.pi * (1 + winkel_grad/180) + 2/math.tan(winkel_rad/2))
                len_straight = r / math.tan(winkel_rad/2)
                x1 = -len_straight * math.sin(winkel_rad/2)
                y1 =  len_straight * math.cos(winkel_rad/2)
                ym = r / math.sin(winkel_rad/2)
                umfang_circle = math.pi * r * (1 + (winkel_grad / 180) )
                umfang = 2 * len_straight + umfang_circle

                text_figure = '" fill="none" stroke-linecap="round">\n' \
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
                                x = -x1 * part / len_straight
                                y =  y1 * part / len_straight
                            elif umfang - part < len_straight:
                                # Picot in second, straight part of ring #
                                x = x1 * (umfang - part) / len_straight
                                y = y1 * (umfang - part) / len_straight
                            else:
                                # Picot in circle part of ring #
                                part_circle = part - len_straight
                                beta_grad = (180 + winkel_grad) * part_circle / umfang_circle
                                x =      r * math.cos(math.radians((winkel_grad/2) - beta_grad))
                                y = ym - r * math.sin(math.radians((winkel_grad/2) - beta_grad))
                            pos = pos + 0.5
                            if self.node_circles == "yes":
                                text_figure = text_figure + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="5" />\n'
                    else:
                        # calculate coords, where to add
                        pos = pos + 0.5
                        if el == 'P':
                            scale_picot = 1
                        elif el == 'p':
                            scale_picot = 0.5
                            
                        verhaeltnis = pos / element["nodes"]
                        part = umfang * verhaeltnis

                        if part < len_straight:
                            # Picot in first, straight part of ring #
                            x = -x1 * part / len_straight
                            y =  y1 * part / len_straight
                            winkel_picot = 270 - winkel_grad / 2
                        elif umfang - part < len_straight:
                            # Picot in second, straight part of ring #
                            x = x1 * (umfang - part) / len_straight
                            y = y1 * (umfang - part) / len_straight
                            winkel_picot = 90 + winkel_grad / 2
                        else:
                            # Picot in circle part of ring #
                            part_circle = part - len_straight
                            beta_grad = (180 + winkel_grad) * part_circle / umfang_circle
                            x =      r * math.cos(math.radians((winkel_grad/2) - beta_grad))
                            y = ym - r * math.sin(math.radians((winkel_grad/2) - beta_grad))
                            winkel_picot = 270 - winkel_grad/2 + beta_grad
                        pos = pos + 0.5

                        text_figure = text_figure + '   <use  xlink:href="#picot" ' \
                                    + 'transform="translate(' + str(x) + ' ' + str(y) + ') '\
                                    + 'rotate(' + str(winkel_picot) + ') ' \
                                    + 'scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')"/>\n'

                self.svg = self.svg + '<g id="' + element["id"] + text_figure + '</g>\n'

                # Output preparation for text: ring name inside the ring #
                element2 = {}
                for key in element:
                    element2[key] = element[key]
                element2["id"] = 'OUT' + element["id"]
                element2["def"] = element2["def"].replace(' ', ' - ')
                self.elems.append(element2)

                self.svg = self.svg + '<g id="' + element2["id"] + text_figure \
                           + '   <text x="' + str(-font_width_half) + '" y="' + str(ym) + '" ' \
                           + 'style="font-size:' + font_size + ';' + font_style + font_weight + fill \
                           + '">' + element["id"][1:] + '</text>\n' \
                           + '</g>\n' \
                           + '<text x="150" y="' + str(150 + self.textline * 70) + '" ' \
                           + 'style="font-size:' + font_size + ';' + font_style + font_weight + fill \
                           + '">' + element["id"][1:] + ': ' + element2["def"] + ' (Ring)</text>\n'
                self.textline = self.textline + 1

            else:                      
                ctypes.windll.user32.MessageBoxW(0, 'Error in line:\n   ' + line + 
                    '\nOpening degree in [..] is not a digit', 'Error', 0)
                return

        # ========================= #
        # =====   C H A I N   ===== #
        # ========================= #
        elif element["id"][0] == 'C':
            if element["ratio"].isdigit():
                ratio = int(element["ratio"])
                alpha_rad = math.acos( 1 - ( 8 / ( ratio * ratio + 4 ) ) )
                r = scale / ( 2 * alpha_rad )
                x1 = 2 * r * math.sin(alpha_rad)
                y1 = 0
                element["dx"] = x1
                element["dy"] = y1

                text_figure = '" fill="none" stroke-linecap="round">\n' \
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

                            if self.node_circles == "yes":
                                text_figure = text_figure + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="5" />\n'
                    else:
                        # calculate coords, where to add
                        if el == 'P':
                            scale_picot = 1
                        elif el == 'p':
                            scale_picot = 0.5
                            
                        pos = pos + 0.5
                        verhaeltnis = pos / element["nodes"]
                        beta_rad = 2 * alpha_rad * verhaeltnis
                        x = x1 / 2 - r * math.cos(beta_rad + gamma_rad)
                        y = -r * ( math.sin(beta_rad + gamma_rad) - math.cos(alpha_rad) )
                        alpha_picot = 180 + math.degrees(beta_rad) - math.degrees(alpha_rad)
                        pos = pos + 0.5

                        # self.svg = self.svg + '   <circle cx="' + str(x) + '" cy="' + str(y) + '"  r="15" />\n'
                        text_figure = text_figure + '   <use  xlink:href="#picot" ' \
                                    + 'transform="translate(' + str(x) + ' ' + str(y) + ') '\
                                    + 'rotate(' + str(alpha_picot) + ') ' \
                                    + 'scale(' + str(scale_picot) + ' ' + str(scale_picot) + ')"/>\n'

                self.svg = self.svg + '<g id="' + element["id"] + text_figure + '</g>\n'  

                # Output preparation for text: chain name besides the chain #
                element2 = {}
                for key in element:
                    element2[key] = element[key]
                element2["id"] = 'OUT' + element["id"]
                element2["def"] = element2["def"].replace(' ', ' - ')
                self.elems.append(element2)

                self.svg = self.svg + '<g id="' + element2["id"] + text_figure \
                           + '   <text x="' + str(element["dx"]/2) + '" y="' + str(element["dy"]/2 - font_size_half) + '" ' \
                           + 'style="font-size:' + font_size + ';' + font_style + font_weight + fill \
                           + '">' + element["id"][1:] + '</text>\n' \
                           + '</g>\n' \
                           + '<text x="150" y="' + str(150 + self.textline * 70) + '" ' \
                           + 'style="font-size:' + font_size + ';' + font_style + font_weight + fill \
                           + '">' + element["id"][1:] + ': ' + element2["def"] + ' (Chain)</text>\n'
                self.textline = self.textline + 1

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
            text_figure1 = '<g id="'    + element["id"] + '" fill="none" stroke-linecap="round">\n'
            text_figure2 = '<g id="OUT' + element["id"] + '" fill="none" stroke-linecap="round">\n'

            lst = element["def"].split(" ")
            first = TRUE
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
                figure2 = 'OUT' + figure

                # Draw element #
                text_figure1 = text_figure1 + '   <use xlink:href="#' + figure + '" ' \
                            + 'transform="translate(' + str(dx) + ' ' + str(dy) + ') '\
                            + 'rotate(' + str(grad) + ')"/>\n'

                if first == TRUE:
                    text_figure2 = text_figure2 + '   <use xlink:href="#' + figure2 + '" ' \
                                + 'transform="translate(' + str(dx) + ' ' + str(dy) + ') '\
                                + 'rotate(' + str(grad) + ')"/>\n'
                    if coord_x >= 0 and coord_y >= 0:
                        first = FALSE

                # Calculate dx and dy for figure #
                for el in self.elems:
                    if el["id"] == figure:
                        dx = dx + el["dx"] * math.cos(rad) - el["dy"] * math.sin(rad)
                        dy = dy + el["dx"] * math.sin(rad) + el["dy"] * math.cos(rad)

            # End of figure and end coordinate
            self.svg = self.svg + text_figure1 + '</g>\n'
            element["dx"] = dx
            element["dy"] = dy

            # Output preparation for text: figure name besides it #
            if element["id"][:3] != 'OUT': 
                self.svg = self.svg + text_figure2 + '</g>\n'
                element2 = {}
                for key in element:
                    element2[key] = element[key]
                element2["id"] = 'OUT' + element["id"]
                element2["def"] = element2["def"].replace(' R', ' OUT')
                element2["def"] = element2["def"].replace(':R', ' OUT')
                self.elems.append(element2)


        # Output of figure #
        if coord_x >= 0 and coord_y >= 0:
            if element["color"] == '':
                element["color"] = self.defaultColor

            self.svg = self.svg \
                        + '<!-- Output -->\n' \
                        + '<g stroke="' + element["color"] \
                        + '" fill="none" stroke-width="3" stroke-linecap="round">\n' \
                        + '   <use xlink:href="#' + element["id"] \
                        + '" transform="translate(' + str(coord_x) \
                        + ' ' + str(coord_y) + ')"/>\n' \
                        + '</g>\n'
            
            # OUT.. figure output, first element in cycle only
            self.svg = self.svg \
                        + '<g stroke="' + self.manualColor \
                        + '" fill="none" stroke-width="4" stroke-linecap="round">\n' \
                        + '   <use xlink:href="#OUT' + element["id"] \
                        + '" transform="translate(' + str(coord_x) + ' ' \
                        + str(coord_y) + ')"/>\n' \
                        + '</g>\n'

        self.elems.append(element)