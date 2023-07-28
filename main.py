import qgate.solution as sln

if __name__ == '__main__':
    aa=sln.Solution("mlrun-nonprod.env")
    try:
        aa.create(force=True)
    finally:
        aa.delete()
