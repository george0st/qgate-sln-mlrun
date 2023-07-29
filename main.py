import qgate.solution as qgate
import os.path

if __name__ == '__main__':

    sln=qgate.Solution(["qgate-mlrun-private.env", "qgate-mlrun.env"])
    sln.create(force=True)
    sln.delete()
