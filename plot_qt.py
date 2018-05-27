"""Generation of graphics about Rollin function
with pyqtgraph.

Graphics will be shown on screen using Qt.

"""
import os
import sys
import statistics
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from rollin import rollin


__qtapp__ = QtGui.QApplication([])
pg.setConfigOptions(antialias=True)
def init(title):
    win = pg.GraphicsWindow(title=title)
    # win.show = lambda: QtGui.QApplication.instance().exec_()
    plot = win.addPlot(title=title)
    plot.win = win
    plot.show = lambda: QtGui.QApplication.instance().exec_()
    return plot
def init_base(title):
    win = pg.plot()
    win.setWindowTitle(title)
    win.show = lambda: QtGui.QApplication.instance().exec_()
    return win



def makefigs(bounds:(int, int)=(1922, 2005), outdir:str='.'):
    "Construit et enregistre les visualisations graphiques de la fonction Rollin"
    makepath = lambda path: os.path.join(outdir, path)
    if not os.path.isdir(outdir):
        raise RuntimeError("Given output directory is not valid: " + str(outdir))
    # Build the data
    ANNEES = tuple(range(*bounds))
    NOMBRES_ROLLIN = range(1, 10)
    ROLLIN = tuple(rollin(annee) for annee in ANNEES)
    assert min(ROLLIN) == 1 and max(ROLLIN) == 9, (min(ROLLIN), max(ROLLIN))
    def evolution(nbs:[int], start:int) -> [int]:
        prev = start
        for nb in nbs:
            nb, prev = nb - prev, nb
            yield nb
    EVOLUTION = tuple(evolution(ROLLIN, rollin(bounds[0] - 1)))
    GREEN = (119,172,48)
    RED = (200,12,48)

    # Association nombre de Rollin -> années
    ANNEE_PAR_NB = {}  # nombre de rollin -> {années}
    for annee, nb_rollin in zip(ANNEES, ROLLIN):
        ANNEE_PAR_NB.setdefault(nb_rollin, []).append(annee)
    COMPTAGE_ANNEES = tuple(len(ANNEE_PAR_NB[nb]) for nb in NOMBRES_ROLLIN)

    # Simple plot de la fonction
    plot = init("Nombre de Rollin et son évolution en fonction de l'année ({}-{})".format(*bounds))
    # plot = win.addPlot(title="Plotting with symbols")
    plot.addLegend()
    plot.plot(ANNEES, ROLLIN, pen=GREEN, symbolBrush=GREEN, symbolPen='w', symbol='d', symbolSize=14, name="Nombre de Rollin")
    # Plot de l'évolution du nombre de Rollin
    plot.plot(ANNEES, EVOLUTION, pen=RED, symbolBrush=RED, symbolPen='w', symbol='t2', symbolSize=14, name="Évolution du nombre de Rollin")
    # plot.setXRange(bounds[0]-10, bounds[1]+1)
    plot.setYRange(min(EVOLUTION + ROLLIN), max(EVOLUTION + ROLLIN) + 2)
    plot.show()

    # Nombre d'années pour chaque nombre de Rollin
    win = init_base("Dénombrement des années {}-{} selon leur nombre de Rollin".format(*bounds))
    # help(pg.BarGraphItem)
    win.addItem(pg.BarGraphItem(x=NOMBRES_ROLLIN, height=COMPTAGE_ANNEES, width=0.3))
    # for nb_rollin in NOMBRES_ROLLIN:
        # win.addItem(pg.BarGraphItem(x=[nb_rollin], height=[ANNEE_PAR_NB[nb_rollin]], width=0.3))
    win.show()

    # Boxplot, pour avoir une idée de la distribution des années
    #  does not exists in pyqtgraph ; building it myself…
    win = init_base("Dénombrement des années {}-{} selon leur nombre de Rollin".format(*bounds))
    for nb_rollin in NOMBRES_ROLLIN:
        annees = ANNEE_PAR_NB[nb_rollin]
        win.plot(x=[nb_rollin], y=annees, pen=None, symbol='o', symbolBrush=pg.intColor(nb_rollin,6))
        mean, median, stdev = statistics.mean(annees), statistics.median(annees), statistics.stdev(annees)
        maxi, mini = max(annees), min(annees)
        limits_amplitude = (maxi - mini) / 2
        middle = limits_amplitude + mini
        boxes = (
            (middle, limits_amplitude*2, 0.8, 'b', 1.2),
            (mean, stdev, 0.5, 'w', 3),
            (mean, 0, 0.5, 'w', 3),
            (median, 0, 0.5, 'r', 4),
        )
        for center, amplitude, beam, color, width in boxes:
            win.addItem(pg.ErrorBarItem(x=np.array([nb_rollin]), y=np.array([center]), height=np.array([amplitude]), beam=beam, pen={'color': color, 'width': width}))
    win.show()

makefigs()
