#Autogenerated by ReportLab guiedit do not edit
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.spider import SpiderChart
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.samples.excelcolors import *

class FilledRadarChart(_DrawingEditorMixin,Drawing):
    def __init__(self,width=200,height=150,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        self._add(self,SpiderChart(),name='chart',validate=None,desc="The main chart")
        self.chart.width      = 90
        self.chart.height     = 90
        self.chart.x          = 45
        self.chart.y          = 25
        self.chart.strands[0].fillColor  = color01
        self.chart.strands[1].fillColor  = color02
        self.chart.strands[2].fillColor  = color03
        self.chart.strands[3].fillColor  = color04
        self.chart.strands[4].fillColor  = color05
        self.chart.strands[5].fillColor  = color06
        self.chart.strands[6].fillColor  = color07
        self.chart.strands[7].fillColor  = color08
        self.chart.strands[8].fillColor  = color09
        self.chart.strands[9].fillColor  = color10
        self.chart.strandLabels.fontName = 'Helvetica'
        self.chart.strandLabels.fontSize = 6
        self.chart.fillColor             = backgroundGrey
        self.chart.data                  = [(125, 180, 200), (100, 150, 180)]
        self.chart.labels                = ['North', 'South', 'Central']
        self._add(self,Label(),name='Title',validate=None,desc="The title at the top of the chart")
        self.Title.fontName   = 'Helvetica-Bold'
        self.Title.fontSize   = 7
        self.Title.x          = 100
        self.Title.y          = 135
        self.Title._text      = 'Chart Title'
        self.Title.maxWidth   = 180
        self.Title.height     = 20
        self.Title.textAnchor ='middle'
        self._add(self,Legend(),name='Legend',validate=None,desc="The legend or key for the chart")
        self.Legend.colorNamePairs = [(color01, 'Widgets'), (color02, 'Sprockets')]
        self.Legend.fontName       = 'Helvetica'
        self.Legend.fontSize       = 7
        self.Legend.x              = 153
        self.Legend.y              = 85
        self.Legend.dxTextSpace    = 5
        self.Legend.dy             = 5
        self.Legend.dx             = 5
        self.Legend.deltay         = 5
        self.Legend.alignment      ='right'
        self._add(self,0,name='preview',validate=None,desc=None)

if __name__=="__main__": #NORUNTESTS
    FilledRadarChart().save(formats=['pdf'],outDir=None,fnRoot='filled_radar')
