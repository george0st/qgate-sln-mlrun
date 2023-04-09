import qgate.project as prj


if __name__ == '__main__':
    aa=prj.Project("mlrun-nonprod.env")
    aa.createProject("gate",force=True)
    aa.delete()
