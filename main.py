import qgate.solution as qgate
from qgate.nsolution import NSolution
import os.path
from qgate.uc import uc101, uc102, uc201, uc301
from qgate.uc import ucsetup, ucoutput, ucbase
import sys

def test():
    setup = ucsetup.UCSetup("0-size-100",
                         ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    output=ucoutput.UCOutput(setup)

    sln=NSolution(setup)

    usecase_fns=[uc101.UC101, uc201.UC201, uc301.UC301, uc102.UC102]
#    usecase_fns=[uc101.UC101, uc201.UC201, uc301.UC301]

    for usecase_fn in usecase_fns:
        uc=usecase_fn(sln, output)
        try:
            uc.exec()
            uc.state=ucbase.UCState.OK
        except Exception as ex:
            uc.state=ucbase.UCState.Error
            uc.logln("{0}: {1}", type(ex).__name__, str(ex))

if __name__ == '__main__':

    args = sys.argv[1:]
    if args:
        if len(args)>0:
            if args[0]=="test":
                # in-progress new solution with splitting scenarios based on use cases
                test()
                sys.exit(0)


    # old, stable solution
    sln = qgate.Solution("0-size-100",
                         ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    try:
        sln.create(force=True)
    finally:
        sln.delete()
