import qgate.solution as qgatesln
import os.path

if __name__ == '__main__':

    sln=qgatesln.Solution("qgate-mlrun-private.env", os.path.join("..", "qgate-fs-model"))
    try:
        sln.create(force=True)
    except Exception as ex:
        print(ex)
    finally:
        sln.delete()
