from multiprocessing import Pool
from copy import deepcopy
import argparse

# Used to parse arguments inputted in
parser = argparse.ArgumentParser(description='Cellular Life Simulator')
parser.add_argument('-i', '--input', type=str, help='Path to input file')
parser.add_argument('-o', '--output', type=str, help='Path to output file')
parser.add_argument('-t', '--threads', type=int, nargs = '?', const = 1, help='Number of threads to spawn')
args = parser.parse_args()

# Reads matrix and saves it to a list
def readMatrix():
  print("\nReading input from", args.input)
  print("\nSimulating ....\n")
  matrx = open(args.input, 'r')
  cellArr = matrx.readlines()
  cellArr = [row.rstrip('\n') for row in cellArr]
  matrx.close
  return cellArr

# Function to simulate matrix
def simulate(arr):
  nextStep = deepcopy(arr)
  M = len(arr)
  N = len(arr[0])
  # For loops used to check neighbors and update based on how many are alive
  for i, row in enumerate(arr): 
    for j, cell in enumerate(arr[i]):
      total = 0
      # Checks neighbors for each iteration
      if arr[i % M][(j-1) % N] == 'O':
        total += 1
      if arr[i % M][(j+1) % N] == 'O':
        total += 1
      if arr[(i-1) % M][j % N] == 'O':
        total += 1
      if arr[(i+1) % M][j % N] == 'O':
        total += 1
      if arr[(i-1) % M][(j-1) % N] == 'O':
        total += 1
      if arr[(i-1) % M][(j+1) % N] == 'O':
        total += 1
      if arr[(i+1) % M][(j-1) % N] == 'O':
        total += 1
      if arr[(i+1) % M][(j+1) % N] == 'O':
        total += 1
      # apply simulation rules
      if cell == 'O':
        if (total < 2) or (total > 4): # Checks total neighbors and updates
          nextStep[i] = list(nextStep[i])
          nextStep[i].pop(j)
          nextStep[i].insert(j, '.')
      elif cell == '.':
        if total > 0 and total%2 == 0: # Checks total neighbors and updates
          nextStep[i] = list(nextStep[i])
          nextStep[i].pop(j)
          nextStep[i].insert(j, 'O')

  arr[:] = convertToString(nextStep[1])
  return arr

#converts matrix back to string to save in output file
def convertToString(org_list, seperator=''):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)

# Writes matrix to output file as a string
def writeMatrix(cellArr):
  outputMatrix = open(args.output, 'w')
  for i in range(len(cellArr)):
    for j in range(len(cellArr[i])):
      outputMatrix.write(convertToString(cellArr[i][j]))
    outputMatrix.write('\n')
  outputMatrix.close

# Driver function 
def main():
  print("Project :: R11565427")
  cellArr = readMatrix()
  processPool = Pool(processes=args.threads) # Creates process pool for multiprocessing
  poolData = list()
  matrixData = []
  for i in range(100):
    poolData.clear()
    for rowNum in range(len(cellArr)):
      # Packs matrixData into poolData to use for processes
      matrixData.append(cellArr[rowNum - 1])
      matrixData.append(cellArr[rowNum])
      matrixData.append(cellArr[(rowNum+1) % len(cellArr)])
      poolData.append(matrixData)
      matrixData = []
    finalMatrx = processPool.map(simulate, poolData) # Calls simulate function with processes ready to go
    cellArr = deepcopy(finalMatrx) # Saves updated data to final matrix
  writeMatrix(cellArr)

if __name__ == "__main__":
  main()
  print("Input is:           %s" % args.input)
  print("Output is:          %s" % args.output)
  print("Threads spawned:    %s" % args.threads)