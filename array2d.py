from pyarray import Array

class Array2D:
    def __init__(self,rows,cols):
        self.theRows=Array(rows)
        for i in range(rows):
            self.theRows[i]=Array(cols)

    def numrows(self):
        return (len(self.theRows))

    def numcols(self):
        return (len(self.theRows[0]))

    def clear(self,value):
        for i in range(self.numrows()):
            self.theRows[i].clear(value)

    def __getitem__(self,pos):
        assert len(pos)==2,"Two subscripts required."
        i=pos[0]
        j=pos[1]
        assert i>=0 and i<self.numrows()\
               and j>=0 and j<self.numcols(),\
        "Invalid element subscript"
        return self.theRows[i][j]

    def __setitem__(self,pos,value):
        assert len(pos)==2,"Two subscripts required."
        i=pos[0]
        j=pos[1]
        assert i>=0 and i<self.numrows()\
               and j>=0 and j<self.numcols(),\
        "Invalid element subscript"
        self.theRows[i][j]=value

    def traverse(self):
        x=self.numrows()
        y=self.numcols()
        for i in range(x):
            for j in range(y):
                print(self.theRows[i][j], end=" ")
            print()