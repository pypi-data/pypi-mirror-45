"""
Minesweeper generator in Python 3
Made by Steven Shrewsbury Dev. (AKA: stshrewsburyDev)
"""

import random


class MineGen():
    """
    The main class making up the generator.

    Called by setting a variable for a generation type using: MyGridGeneration = minesweeperPy.MineGen(GridSizeX, GridSizeY)
    Used bu using:
        - MyGridGeneration.GenerateGrid(MineCount)
        - MyGridGeneration.GridSizeX
        - MyGridGeneration.GridSizeY
    """
    def __init__(self, GridSizeX: int=0, GridSizeY: int=0, BlankIdentifier: str=" "):
        """
        Makes the main generator using: MyGridGeneration = minesweeperPy.MineGen(GridSizeX, GridSizeY)
        :param GridSizeX: integer above 4
        :param GridSizeY: integer above 4
        """
        if GridSizeX <= 4 or GridSizeY <= 4:
            raise ValueError("""Expected:
        - GridSizeX = 5+ got {0}
        - GridSizeY = 5+ got {1}""".format(GridSizeX, GridSizeY))
        self.GridSizeX = GridSizeX
        self.GridSizeY = GridSizeY
        self.BlankIdentifier = BlankIdentifier
        self.CellPossibilities = ["M", self.BlankIdentifier, "1", "2", "3", "4", "5", "6", "7", "8"]

    def GenerateGrid(self, MineCount: int=0):
        """
        Generate grid command

        Generates a grid on the generators size in the __init__
        Uses MineCount to make the amount of mines onto the grid

        :param MineCount: integer above 0
        :return: json library with blank identifier and grid in the form of a 2D list
            eg: [
                ["M","1"," "," "," "],
                ["1","2","1","1"," "],
                [" ","1","M","2","1"],
                ["1","2","3","M","1"],
                ["1","M","2","1","1"]
                ]
        M indicating a mine and the numbers around are the numbers
        are the in game numbers for the mine count
        """
        if MineCount <= 0:
            raise ValueError("""Expected:
                    - MineCount = 1+ got {0}""".format(MineCount))
        if MineCount >= (self.GridSizeX * self.GridSizeY)+1:
            raise ValueError("""Not enough space on the grid for that many mines:
        - Grid space = {0}""".format((self.GridSizeX * self.GridSizeY)))

        ReturnOutput = {}

        Grid = []

        TempMineLocations = []

        for mine in range(0, MineCount):
            MineSelector = False
            while MineSelector is False:
                MineLocation = [random.randint(0, self.GridSizeX-1), random.randint(0, self.GridSizeY-1)]
                if MineLocation in TempMineLocations:
                    pass
                else:
                    TempMineLocations.append(MineLocation)
                    MineSelector = True

        for row in range(0, self.GridSizeY):
            RowContents = []
            for column in range(0, self.GridSizeX):
                if [column, row] in TempMineLocations:
                    RowContents.append("M")
                    NearMineCount = None
                else:
                    NearMineCount = 0
                    if [column+1, row] in TempMineLocations:
                        NearMineCount += 1
                    if [column-1, row] in TempMineLocations:
                        NearMineCount += 1
                    if [column, row+1] in TempMineLocations:
                        NearMineCount += 1
                    if [column, row-1] in TempMineLocations:
                        NearMineCount += 1
                    if [column+1, row+1] in TempMineLocations:
                        NearMineCount += 1
                    if [column-1, row-1] in TempMineLocations:
                        NearMineCount += 1
                    if [column+1, row-1] in TempMineLocations:
                        NearMineCount += 1
                    if [column-1, row+1] in TempMineLocations:
                        NearMineCount += 1
                    if NearMineCount == 0:
                        RowContents.append(self.BlankIdentifier)
                    else:
                        RowContents.append(str(NearMineCount))
            Grid.append(RowContents)

        ReturnOutput["grid"] = Grid
        ReturnOutput["BlankIdentifier"] = self.BlankIdentifier

        return ReturnOutput


def GridInfo(GridInfo=None):
    """
    Shows the information of the grid entered (Mine total, Grid size etc...)
    :param GridInfo: JSON library generated via MineGen.GenerateGrid()
    :return: JSON library of grid information
    """
    try:
        BlankIdentifier = GridInfo["BlankIdentifier"]
        Grid = GridInfo["grid"]
        CellPossibilities = ["M", BlankIdentifier, "1", "2", "3", "4", "5", "6", "7", "8"]
    except:
        raise TypeError("""Expected:
            - GridInfo = json list, got {0}""".format(GridInfo))

    GridInformation = {
        "GridColumns": len(Grid[0]),
        "GridRows": len(Grid),
        "MineCount": 0,
        "NonMineCells": 0,
        "EmptyCells": 0,
        "NumberedCells": 0
    }

    for row in Grid:
        for cell in row:
            if cell not in CellPossibilities:
                raise TypeError("""Unknown type of cell {0}, expected one of {1}""".format(cell, CellPossibilities))
            if cell == "M":
                GridInformation["MineCount"] += 1
            elif cell == BlankIdentifier:
                GridInformation["NonMineCells"] += 1
                GridInformation["EmptyCells"] += 1
            else:
                GridInformation["NonMineCells"] += 1
                GridInformation["NumberedCells"] += 1

    return GridInformation

