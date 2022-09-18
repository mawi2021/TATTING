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
            self.parent.widget.txtFilename = data["lastTxtFile"]
            self.parent.widget.svgFilename = data["lastSvgFile"]
            self.parent.widget.open()

    def onExit(self):
        data = {}
        data["grid"]          = self.parent.widget.grid
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