import qgate.solution as qgatesln
import os.path

if __name__ == '__main__':

    sln=qgatesln.Solution("mlrun-nonprod.env", os.path.join("..","qgate-fs-model"))
    try:
        sln.create(force=True)
    finally:
        sln.delete()
