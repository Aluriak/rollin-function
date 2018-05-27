"""Generation of graphics about Rollin function
with matplotlib/pandas/seaborn.

Graphics will be generated and saved in out/ directory.

"""

import os
import seaborn as sbn
import pandas as pd
import matplotlib.pyplot as plt
from rollin import rollin

# Une palette commune sympa.
sbn.set()
sbn.set_palette('husl', 10)


def makefigs(bounds:(int, int)=(1922, 2005), outdir:str='.'):
    "Construit et enregistre les visualisations graphiques de la fonction Rollin"
    """Build and save the graphics of Rollin function"""
    makepath = lambda path: os.path.join(outdir, path)
    if not os.path.isdir(outdir):
        raise RuntimeError("Given output directory is not valid: " + str(outdir))

    # Build the data
    ANNEES = tuple(range(bounds[0], bounds[1]+1))
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

    # Simple plot de la fonction
    nb_par_annee = pd.DataFrame({
        'année': ANNEES,
        'nombre de Rollin': list(rollin(annee) for annee in ANNEES)
    }).set_index('année')
    ax = nb_par_annee.plot(legend=False)
    ax.set_title("Nombre de Rollin en fonction de l'année ({}-{})".format(*bounds))
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de Rollin")
    plt.savefig(makepath('trace-{}-{}.png'.format(*bounds)))
    plt.close()

    # Plot de l'évolution du nombre de Rollin
    nb_par_annee = pd.DataFrame({
        'année': ANNEES,
        'nombre de Rollin': EVOLUTION,
    }).set_index('année')
    ax = nb_par_annee.plot(legend=False)
    ax.set_title("Évolution du nombre de Rollin d'une année à l'autre ({}-{})".format(*bounds))
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de Rollin")
    plt.savefig(makepath('evolution-{}-{}.png'.format(*bounds)))
    plt.close()

    # Association nombre de Rollin -> années
    annee_par_nb = {}  # nombre de rollin -> {années}
    for annee, nb_rollin in zip(ANNEES, ROLLIN):
        annee_par_nb.setdefault(nb_rollin, []).append(annee)

    # Nombre d'années pour chaque nombre de Rollin
    nb_annee_par_nb = {"nombre d'années": [], 'nombre de Rollin': []}
    for nb, annees in annee_par_nb.items():
        nb_annee_par_nb["nombre d'années"].append(len(annees))
        nb_annee_par_nb["nombre de Rollin"].append(nb)
    nb_annee_par_nb = pd.DataFrame(nb_annee_par_nb).set_index('nombre de Rollin').sort_index()
    ax = nb_annee_par_nb.plot.bar(y="nombre d'années", rot=0, legend=False)
    ax.set_title("Dénombrement des années {}-{} selon leur nombre de Rollin".format(*bounds))
    ax.set_xlabel("Nombre de Rollin")
    ax.set_ylabel("Nombre d'années")
    for patch in ax.patches:  # show the total count above each bar
        b = patch.get_bbox()
        ax.annotate(str(int(b.y1)).rjust(3), (patch.get_x() - 0.04, b.y1 * 1.01))  # MAGIC
    plt.savefig(makepath('comptage-{}-{}.png'.format(*bounds)))
    plt.close()

    # Boxplot, pour avoir une idée de la distribution des années
    df_annee_par_nb = pd.DataFrame(
        {k: pd.Series(v) for k, v in annee_par_nb.items()},
        columns=sorted(tuple(annee_par_nb.keys())),
    )
    ax = df_annee_par_nb.boxplot(rot=0)
    ax.set_title("Distribution des années {}-{} selon leur nombre de Rollin".format(*bounds))
    ax.set_xlabel("Nombre de Rollin")
    ax.set_ylabel("Distribution des années")
    plt.savefig(makepath('distribution-{}-{}.png'.format(*bounds)))
    plt.close()


if __name__ == '__main__':
    makefigs((1, 2018), outdir='out/')
    makefigs(outdir='out/')
