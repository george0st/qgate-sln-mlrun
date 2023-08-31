import qgate.solution as qgate
import os.path

if __name__ == '__main__':

    sln = qgate.Solution(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    try:
        sln.create(force=True)
    finally:
        sln.delete()
