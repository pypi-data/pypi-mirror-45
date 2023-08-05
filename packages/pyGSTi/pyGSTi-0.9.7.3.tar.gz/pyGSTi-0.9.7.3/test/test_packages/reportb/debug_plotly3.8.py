import pygsti
from pygsti.construction import std1Q_XYI as std

w = pygsti.report.Workspace()
prepStrs = std.prepStrs
effectStrs = std.effectStrs
        
w.BoxKeyPlot(prepStrs, effectStrs)
print w
