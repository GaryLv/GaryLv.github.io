---
layout: post
title:  "Python 数组的基本操作"
date:   2016-02-15
author: Run.D.Guan
category: Python
tags: [python]
---


> 向量化计算在数据分析中很常用，与数学公式最为相近，又可简化代码。Numpy是Python的一个扩展库，支持高阶维度数组和矩阵运算，Numpy的array 类称为ndarray，也被称为array。这里对其运算进行简单的介绍做为学习与查询之用。 

```python
import numpy as np
```

### 一维数组


```python
lst = [3, 1, 4, 1, 5, 9, 2]  # list
vec = np.array([3, 1, 4, 1, 5, 9, 2], dtype='float64')
```


```python
>>> lst
```




    [3, 1, 4, 1, 5, 9, 2]




```python
>>> vec
```




    array([ 3.,  1.,  4.,  1.,  5.,  9.,  2.])



另一种来使得array为浮点型的方法是在一个或多个数字后加一个小数点'.'。

下面来看看 **list** 和 **array** 之间的差别


```python
>>> lst + lst
```




    [3, 1, 4, 1, 5, 9, 2, 3, 1, 4, 1, 5, 9, 2]




```python
>>> vec + vec
```




    array([  6.,   2.,   8.,   2.,  10.,  18.,   4.])




```python
>>> # lst ** 2
```


```python
>>> vec ** 2
```




    array([  9.,   1.,  16.,   1.,  25.,  81.,   4.])



对于 array，对于大多数的操作（+，-，\*，/，\*\*，等）和函数（exp, log, sin, 等）都是逐个计算的，矩阵乘法用 dot() 函数


```python
>>> lst[0], lst[-1], lst[3:5]
```




    (3, 2, [1, 5])




```python
>>> vec[0], vec[-1], vec[3:5]
```




    (3.0, 2.0, array([ 1.,  5.]))



list 和 array 都支持从0开始的索引和切片，array 还支持按列表索引，但普通的 list 却不行


```python
>>> vec[[0, 3, 5, 3]]
```




    array([ 3.,  1.,  9.,  1.])




```python
>>> # lst[[0, 3, 5, 3]]
```

### 二维数组（矩阵）

**numpy** 虽然提供了 "matrix" 类型，但是这里不建议用它，而是都使用  arrays，arrays 应用的范围更广，这样会减少困惑和更少的 bugs。


```python
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12],
              [13, 14, 15]], dtype='float64')
```


```python
print("Here is the whole test array:")
print(A)
print('A is a numpy array with shape ' + repr(A.shape))
print('That means A has %d row' % A.shape[0], 'and %d columns.' % A.shape[1])
```

    Here is the whole test array:
    [[  1.   2.   3.]
     [  4.   5.   6.]
     [  7.   8.   9.]
     [ 10.  11.  12.]
     [ 13.  14.  15.]]
    A is a numpy array with shape (5, 3)
    That means A has 5 row and 3 columns.
    


```python
print("跟普通的list一样，我们可以按行索引")
print("A[0] = ")
print(A[0])
print("A[0:3] = ")
print(A[0:3])
```

    跟普通的list一样，我们可以按行索引
    A[0] = 
    [ 1.  2.  3.]
    A[0:3] = 
    [[ 1.  2.  3.]
     [ 4.  5.  6.]
     [ 7.  8.  9.]]
    


```python
print("我们可以笨拙的提取一行第一个元素：")
print("A[0][0] = ")
print(A[0][0])
print("但是一种更简洁的方式为：")
print("A[0,0] = ")
print(A[0, 0])
```

    我们可以笨拙的提取一行第一个元素：
    A[0][0] = 
    1.0
    但是一种更简洁的方式为：
    A[0,0] = 
    1.0
    


```python
print("Rows and columns can be sliced like Python lists:")
print("A[0:2,:] = ")
print(A[0:2, :])
```

    Rows and columns can be sliced like Python lists:
    A[0:2,:] = 
    [[ 1.  2.  3.]
     [ 4.  5.  6.]]
    


```python
print("Extracting multiple desired rows and columns:")
print(A[np.ix_([0, 3, 4], [0, 2])])
# Another version is "A[[0,3,4]][:,[0,2]]", but that can't be assigned to.
```

    Extracting multiple desired rows and columns:
    [[  1.   3.]
     [ 10.  12.]
     [ 13.  15.]]
    

### Work with arrays

计算 array 每列的均值


```python
I, J = A.shape
mu = np.zeros(J)  #记录结果
for i in range(I):
    for j in range(J):
        mu[j] += A[i,j]
mu = mu / I
print('Mean: ' + repr(mu))
```

    Mean: array([ 7.,  8.,  9.])
    

可以采用 "mean" 函数来完成上述的工作


```python
mu = np.mean(A, 0)  # 0 means sum over the 0th dimension of the array (the rows)
print('Mean: ', repr(mu))
```

    Mean:  array([ 7.,  8.,  9.])
    

令每列0均值化，即每列都减去均值


```python
A_shift = np.copy(A)  # without copy, would modify A when modify A_shift
for i in range(I):
    for j in range(J):
        A_shift[i,j] -= mu[j]
print('Cols centered:\n' + repr(A_shift))
```

    Cols centered:
    array([[-6., -6., -6.],
           [-3., -3., -3.],
           [ 0.,  0.,  0.],
           [ 3.,  3.,  3.],
           [ 6.,  6.,  6.]])
    

该过程可以按行减去均值


```python
A_shift = np.copy(A)
for i in range(I):
    A_shift[i] -= mu
print('Cols centered:\n' + repr(A_shift))
```

    Cols centered:
    array([[-6., -6., -6.],
           [-3., -3., -3.],
           [ 0.,  0.,  0.],
           [ 3.,  3.,  3.],
           [ 6.,  6.,  6.]])
    

来使每行的均值为0


```python
row_mu = np.mean(A, 1)
row_mu.shape == (5,)  #行向量
```




    True



但我们想要的 5x1 的列向量，可以通过 row_mu[:,newaxis] 实现列向量的转换，该向量可以从任何 5xD array 中以每列的方式减去


```python
A_shift = A - row_mu[:, np.newaxis]
```

### 查询与排序


```python
people = ['Jim', 'alice', 'ali', 'bob']
height_cm = np.array([180, 165, 165, 178])
```


```python
# The laborious, procedural programming way:
largest_height = -np.Inf
tallest_person = ''
for (i, h) in enumerate(height_cm):
    if h > largest_height:
        largest_height = h
        tallest_person = people[i]
print('largest_height = %g' % largest_height)
print('tallest_person = %s' % tallest_person)
```

    largest_height = 180
    tallest_person = Jim
    

当然啦，这么典型的问题肯定有内建函数来解决


```python
largest_height = max(height_cm)
print('largest_height = %g' % largest_height)
```

    largest_height = 180
    


```python
#alternatively we can ask for the location of the largest element:
idx = np.argmax(height_cm)
largest_height = height_cm[idx]
tallest_person = people[idx]
print('largest_height = %g' % largest_height)
print('tallest_person = %s' % tallest_person)
```

    largest_height = 180
    tallest_person = Jim
    


```python
# What about the shortest person?
smallest_height = min(height_cm)
idx = np.argmin(height_cm)
smallest_person = people[idx]
```


```python
# 对于最小的有两个，如何将其都显示出来:
#ids = nonzero(height_cm == smallest_height)[0]
ids = np.where(height_cm == smallest_height)[0]
smallest_people = [people[i] for i in ids]  #list
print('smallest_people: ' + repr(smallest_people))
```

    smallest_people: ['alice', 'ali']
    

**sort (height_cm)** sorts the list. Again, a second argument will give the indexes of the corresponding items.


```python
sorted_heights = np.sort(height_cm)
print('sorted_heights: ' + repr(sorted_heights))
ids = np.argsort(height_cm)
sorted_heights = height_cm[ids]
```

    sorted_heights: array([165, 165, 178, 180])
    


```python
# The previous line wouldn't work with a normal list, but numpy arrays allow a
# list of indexes. The python list of people needs a list comprehension:
people_in_height_order = [people[i] for i in ids]
print('sorted_heights: ' + repr(sorted_heights))
print('people_in_height_order: ' + repr(people_in_height_order))
```

    sorted_heights: array([165, 165, 178, 180])
    people_in_height_order: ['alice', 'ali', 'bob', 'Jim']
    

### 矩阵操作 “向量化”

Given a mathematical expression like:
result = $\sum_{i=1}^I f_n(x_i, x_j) val(z_i)$
The results of $f_n$ could be put in an $I\times J$ matrix, and the results of val in a
length$-I$ vector. The sum is then a matrix-vector multiply:

result = dot(fn.T, val)

Sometimes a *newaxis* index expression is required to make a vector be a $D\times1$ or $1\times D$ matrix so that an elementwise operator can combine it with a matrix (using "broadcasting").

## Reference
* [http://www.inf.ed.ac.uk/teaching/courses/inf2b/learnSlides/numpy_intro.py](http://www.inf.ed.ac.uk/teaching/courses/inf2b/learnSlides/numpy_intro.py)
* [https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html](https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html)
* [http://mathesaurus.sourceforge.net/](http://mathesaurus.sourceforge.net/)
