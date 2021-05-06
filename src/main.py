import random
from multiprocessing import Pool

# Note this time we are using Pool, not Process


def main():
    matrix = genMatrix(100, 50)
    MAX_PROCESSES = 10
    finalSum = 0

    processPool = Pool(processes=MAX_PROCESSES)
    poolData = list()
    #A process pool allows us to create a pool of worker processes.
    #  Each process will accept

    for rowNum in range(len(matrix)):
        #Pack each matrixData list and append it to the aggregate list
        matrixData = [matrix, rowNum]
        poolData.append(matrixData)

        #poolData will (by the end of this) contain the following:
        #   A list of lists, with each sublist containing a full copy of the matrix and a rowNum integer.

        #Uncomment the following lines to see it debug serially
        print(matrix[rowNum])
        print(addMatrixRow(matrixData))
        print()

    #poolData now holds all the data for each process to use.
    #   Next we use the map function to perform a scatter/gather
    #     operation.
    #   processPool.map() takes 2 arguments.
    #     The first is the name of our target function "addMatrixRow"
    #     The second is the list containing all of our data "poolData"
    #       By default, this will send each member to a separate
    #       process.  This will only allow MAX_PROCESSES total
    #       processes to be running at a time.
    finalData = processPool.map(addMatrixRow, poolData)

    #processPool.map is a blocking function call!
    # So reaching this point ensures all the processes have completed.
    # As such we don't need poolData - so we delete it to save memory.
    del (poolData)

    #finalData contains the results from each process. So we need to sum them up.
    for num in finalData:
        finalSum += num

    print("The final sum for the matrix is %d." % finalSum)


# This function will take a 2D matrix and then solve for 1 row,
#   returning the sum of that row.
# matrixData -> List containing:
#     The entire matrix in index 0.
#     The rowNum integer in index 1.
def addMatrixRow(matrixData):
    matrix = matrixData[0]
    rowNum = matrixData[1]
    del (matrixData)  #clear it out of memory.
    rowSum = 0
    #For each column number in the Nth row of the matrix
    for colNum in range(len(matrix[rowNum])):
        rowSum += matrix[rowNum][colNum]

    return rowSum


#Takes a number of rows and columns, returns a randomly
#   generated matrix of size row x col
def genMatrix(row, col):
    matrix = list()
    for i in range(row):
        matrix.append(list())  #Inject a new row.
        for j in range(col):
            matrix[i].append(random.randint(0, 10))
    return matrix


if __name__ == '__main__':
    main()
