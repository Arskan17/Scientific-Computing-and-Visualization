#!/usr/bin/env python3

import numpy as np
import sys

def read_file(path):
      file = open(path, "r")
      width = int(file.readline().strip())
      height = int(file.readline().strip())

      k = int(file.readline().strip())
      if k < 0 or k > width or k > height:
            raise Exception("k=" + str(k) + " out of bounds for width " + str(width) + " and height " + str(height))

      matrix_data = []
      for _ in range(height):
            row = list(map(lambda n: int(n.strip()), file.readline().split(',')))
            if len(row) != width:
                  raise Exception("Expected " + str(width) + " columns but got " + str(len(row)))
            matrix_data.append(row)

      suche = np.transpose(np.matrix(list(map(lambda n: int(n.strip()), file.readline().split(',')))))
      if suche.shape != (height,1):
            raise Exception("Invalid length of term vector")

      return (np.array(matrix_data), k, suche)

def write_output(data):
      # Wenn data keine Matrix ist, muss die folgende Zeile ggf angepasst werden
      strings = [str(x[0]) for x in data.round(3)]
      print(",".join(strings))

# Häufigkeit der Terme pro Dokument, gewünschter Rang, und Anfrage im Term-Raum
(A, k, suche) = read_file(sys.argv[1])
# Anzahl Terme und Dokumente
(terme, n) = A.shape

# Singulärwertzerlegung berechnen (lassen) ...
(full_u, full_s, full_vt) = np.linalg.svd(A, full_matrices=False)

# ... und entsprechend dem Rang zuschneiden
u = full_u[:,0:k]
s = np.diag(full_s[0:k])
vt = full_vt[0:k,:]



# Die Anfrage wird in den Topic - Raum transformiert
suche_k = np.transpose ( u ) * suche
# berechne f¨ur alle dokumente das skalarprodukt als ¨A hnlichkeitsma ß
lsi_ergebnis = np.transpose ( vt ) * suche_k



write_output(lsi_ergebnis)
