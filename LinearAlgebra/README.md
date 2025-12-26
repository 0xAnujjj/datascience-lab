# Linear Algebra Lab

This repository contains solutions for a lab assignment covering basic matrix operations, determinants, eigenvalues, eigenvectors and a simple car price prediction.

---

## 1. Matrix Operations

Given the matrices:

A =
[[ 2, -1 ],
 [ 0,  3 ]]

B =
[[ 1,  2 ],
 [ -3, 4 ]]

### Tasks
- Add matrices **A + B**
- Multiply matrices **A × B**
- Evaluate the expression **3A − 2B**

---

## 2. Determinant and Inverse

Using matrix **A**:

### Tasks
- Find the determinant of matrix **A**
- Check whether **A** is invertible
- If invertible, compute the inverse of **A**

---

## 3. Eigenvalues and Eigenvectors

Given the matrix:

C =
[[ 4,  1 ],
 [ -2, 1 ]]

### Task
- Compute the eigenvalues and eigenvectors of matrix **C**

---

## 4. Car Price Prediction (Linear Regression)

A dataset of cars is given with the following features:

- **x1**: Number of cylinders  
- **x2**: Engine size (liters)  
- **x3**: Horsepower  

### Given Data

| Car | Cylinders (x1) | Engine Size (x2) | Horsepower (x3) | Price |
|-----|---------------|------------------|-----------------|-------|
| Car 1 | 4 | 1.5 | 100 | 20 |
| Car 2 | 6 | 2.0 | 150 | 30 |

### Task
Using the **normal equation**, predict the price of a new car with:

- Cylinders = 8  
- Engine size = 3.0  
- Horsepower = 200  

---

## Method Used

The coefficients are calculated using the **normal equation**:

β = (XᵀX)⁻¹ Xᵀy

Where:
- **X** is the feature matrix
- **β** is the coefficient vector
- **y** is the price vector

---