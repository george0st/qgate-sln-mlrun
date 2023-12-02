from qgate.solution import Solution
from qgate.uc import uc101, uc102, uc201, uc301, uc401, uc501, uc601
from qgate.uc import ucbase
from qgate import output, setup
import sys


if __name__ == '__main__':

    setup = setup.Setup("0-size-100",
                          ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    output = output.Output(setup, ['./assets/templates/qgt-mlrun.txt'])
    sln = Solution(setup)

    usecase_fns = [uc101.UC101, uc201.UC201, uc301.UC301, uc401.UC401, uc501.UC501]
    usecase_test = uc601.UC601
    NoDelete=False

    # support parametr 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s)
    if len(sys.argv)>1:
        for arg in sys.argv[1:]:
            arg=arg.lower()
            if arg=="nodelete":
                NoDelete=True
            elif arg=="test":
                usecase_fns.append(usecase_test)
    if not NoDelete:
        usecase_fns.append(uc102.UC102)

    for usecase_fn in usecase_fns:
        if usecase_fn:
            uc = usecase_fn(sln, output)
        try:
            uc.exec()
            uc.state = ucbase.UCState.OK
        except Exception as ex:
            uc.state = ucbase.UCState.Error
            #uc.logln("{0}: {1}", type(ex).__name__, str(ex))
            uc.usecase_detail(f"{type(ex).__name__}: {str(ex)}")
            uc.usecase_state("Error")
    output.Close()