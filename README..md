# Linear Algebra
This repository contains solutions to a set of problems covering matrix operations, determinants, eigenvalues, and eigenvectors task.

---

## 1. Matrix Operations

Perform the following operations on the given matrices:

\[
A = \begin{bmatrix}
2 & -1 \\
0 & 3
\end{bmatrix}
\quad
B = \begin{bmatrix}
1 & 2 \\
-3 & 4
\end{bmatrix}
\]

### Tasks
- **a.** Compute \( A + B \)
- **b.** Compute \( AB \)
- **c.** Compute \( 3A - 2B \)

---

## 2. Determinants and Inverses

Using matrix \( A \):

### Tasks
- Find the **determinant** of matrix \( A \)
- Determine whether matrix \( A \) is **invertible**
- If invertible, compute \( A^{-1} \)

---

## 3. Eigenvalues and Eigenvectors

Given the matrix:

\[
C = \begin{bmatrix}
4 & 1 \\
-2 & 1
\end{bmatrix}
\]

### Task
- Compute the **eigenvalues** and **eigenvectors** of matrix \( C \)

---

## 4. Car Price Prediction

You are given a dataset of cars with the following features:

- \( x_1 \): Number of cylinders  
- \( x_2 \): Engine size (in liters)  
- \( x_3 \): Horsepower  

### Dataset

| Car | Cylinders (\(x_1\)) | Engine Size (\(x_2\)) | Horsepower (\(x_3\)) | Price |
|-----|------------------|---------------------|---------------------|-------|
| Car 1 | 4 | 1.5 | 100 | 20 |
| Car 2 | 6 | 2.0 | 150 | 30 |

### Task
Using the **normal equation**, predict the price of a car with the following features:

- \( x_1 = 8 \)
- \( x_2 = 3.0 \)
- \( x_3 = 200 \)

### Hint
Represent the dataset as a matrix equation:

\[
X^T \beta = y
\]

Where:
- \( X \) is the feature matrix  
- \( \beta \) is the coefficient vector  
- \( y \) is the price vector  

Compute the coefficients using the normal equation:

\[
\beta = (X^T X)^{-1} X^T y
\]

---

## Tools Used
- Python
- NumPy
