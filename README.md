# gmt_trng_assess - GMT0005的一种参考实现

实现标准：GMT0005-2012

## 功能实现

1. 单比特频数检测
2. 块内频数检测
3. 游程总数检测
4. 块内“1”的最大游程检测
5. 矩阵秩检测
6. 离散傅里叶变换检测
7. Maurer通用统计检测
8. 线性复杂度检测
9. 重叠子序列检测
10. 近似熵检测
11. 累加和检测
12. 扑克检测
13.	游程分布检测
14. 二元推导检测
15. 自相关检测

## 1. 使用方法

显著性水平a = 0.01

1. 默认参数输入120MB文件。进行1000轮评估，通过的下界为980轮，每轮评估使用1000000bit数据。
```
python3 ./assess.py <file-name>
```

2. 通过参数传入评估参数
```
python3 ./assess.py <file-name> <rounds> <bits-of-round> <pass-threshold>
```

## 2. 修改配置参数

修改config.json来修改每种检测的参数


## 3. 结果

结果如下面例子:
进行2轮测试，第一列为测试项，第二列为通过的测试轮数，第三列为是否大于阈值。

```
assess report(total 2 rounds):
<TEST>                                <PROPORTION>      <PASS>    
------------------------------------------------------------------
monobit_frequency_test                2                 True
frequency_test_within_a_block_test    2                 True
poker_test                            2,2               True,True
serial_test                           2,2               True,True
runs_test                             2                 True
runs_distribution_test                2                 True
longest_run_of_ones_in_a_block_test   2                 True
binary_derivative_test                2,2               True,True
autocorrelation_test                  2,2,2,2           True,True,True,True
binary_matrix_rank_test               2                 True
cumulative_sums_test                  2                 True
approximate_entropy_test              2,2               True,True
linear_complexity_test                2                 True
maurer_universal_statistical_test     2                 True
discrete_fourier_transform_test       2                 True
------------------------------------------------------------------
```

## 4. 实现参考

1. [NIST-statistical-test](https://github.com/GINARTeam/NIST-statistical-test)
