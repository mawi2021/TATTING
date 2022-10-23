from os.path import exists

import json

class Process():

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.configFilename = 'config/config.json'

        if exists(self.configFilename):
            with open(self.configFilename, encoding="utf-8") as f:
                data = json.load(f)
            f.close()        

            self.parent.widget.grid = data["grid"]
            self.parent.widget.node_circles = data["dots"]
            self.parent.widget.txtFilename = data["lastTxtFile"]
            self.parent.widget.svgFilename = data["lastSvgFile"]
            self.parent.widget.open()

    def onExit(self):
        data = {}
        data["grid"]          = self.parent.widget.grid
        data["dots"]          = self.parent.widget.node_circles
        data["lastTxtFile"]   = self.parent.widget.txtFilename
        data["lastSvgFile"]   = self.parent.widget.svgFilename

        with open(self.configFilename, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()

        exit(self)

    def onGrid(self):
        if self.parent.widget.grid in ('no', ''):
            self.parent.widget.grid = 'yes'
        else:
            self.parent.widget.grid = 'no'
        self.parent.widget.onRedraw()

    def onNodeCircle(self):
        if self.parent.widget.node_circles in ('no', ''):
            self.parent.widget.node_circles = 'yes'
        else:
            self.parent.widget.node_circles = 'no'
        self.parent.widget.onRedraw()        

    def onImageFrame(self):
        if self.parent.widget.image_frame in ('no', ''):
            self.parent.widget.image_frame = 'yes'
        else:
            self.parent.widget.image_frame = 'no'
        self.parent.widget.onRedraw()                

    def onPaperSize(self, format):
        if format == 'A4':
            self.parent.widget.paperwidthMM = 210
            self.parent.widget.paperheightMM = 297
        elif format == 'A3':
            self.parent.widget.paperwidthMM = 297
            self.parent.widget.paperheightMM = 420
        elif format == 'A2':
            self.parent.widget.paperwidthMM = 420
            self.parent.widget.paperheightMM = 594
        elif format == 'A1':
            self.parent.widget.paperwidthMM = 594
            self.parent.widget.paperheightMM = 840
        elif format == 'A0':
            self.parent.widget.paperwidthMM = 840
            self.parent.widget.paperheightMM = 1188

        self.parent.widget.onRedraw()                        