import qgate.solution as qgate
import os.path
from qgate.uc.uc101 import UC101


if __name__ == '__main__':

    aa=UC101("sss")

    sln = qgate.Solution("0-size-100",
                         ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    try:
        sln.create(force=True)
    finally:
        sln.delete()
