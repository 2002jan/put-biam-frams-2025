rem To learn about all available options of the .py algorithm below, add "-h" to its parameters.
rem Use the source code of the examples as a starting point for your customizations.
rem Example usage:

set DIR_WITH_FRAMS_LIBRARY="C:\Users\2002j\Desktop\pliki\MastersPUT\sem1\BIAM\Framsticks52"

for %%M in (0,005,010,020,030,040,050) do (
    for /L %%N in (1,1,10) do (
rem        python FramsticksEvolution.py -sim "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-%%M.sim" -path %DIR_WITH_FRAMS_LIBRARY% -opt vertpos -max_numparts 30 -max_numgenochars 50 -initialgenotype /*9*/BLU -popsize 50 -generations 20 -hof_size 1 -hof_savefile HoF-f9-%%M-%%N.gen
        python FramsticksEvolution.py -sim "eval-allcriteria.sim;deterministic.sim;sample-period-2.sim;f9-mut-%%M.sim" -path %DIR_WITH_FRAMS_LIBRARY% -opt vertpos -max_numparts 30 -max_numgenochars 50 -initialgenotype /*9*/BLU -popsize 50 -generations 150 -hof_size 1
    )
)
