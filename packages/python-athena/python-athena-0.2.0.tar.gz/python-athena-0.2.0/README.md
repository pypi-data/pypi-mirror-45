
### PyAthena

A python client to query on Athena Database. Query results are formatted in pandas dataframe.


### Install
```bash
pip install git+https://github.com/yardstick17/PyAthena.git
```

### Usage

```python
In [9]: from athena import Athena

In [10]: query =    """SELECT col1, col2, col3, col3  
                        FROM "database"."table1"
                        WHERE col1 = 'PI912A0CV-O12'
                            AND col2 = '2019-03-04'
                            AND schema='best_model_ever'
                    """

In [11]: df = athena_client.execute_with_pandas(query=query)

In [12]: df.head()
Out[12]:
            col1           col2                   col3                      col3
0  PI912A0CV-O12            0                      0.0                      2.623155
1  PI912A0CV-O12            0                      0.0                      2.095256
2  PI912A0CV-O12            0                      0.0                      1.904961
3  PI912A0CV-O12            0                      0.0                      0.829332
4  PI912A0CV-O12            0                      0.0                      0.058469
```
