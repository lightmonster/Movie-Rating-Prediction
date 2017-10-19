
----

# 数据读取

从 `txt / csv` 里读取 `df_user` `df_movie` `df_train` `df_test`

用 `piv_train` 记录 train 的个数

`labels` 记录所有 `rating`

`id_test` 记录 `df_test` 的 `id`

# 数据处理

`df_train` 的 `rating` 去掉之后，和 `df_test` 合并在一起，再与 `df_user` 和 `df_movie` 信息合并

去掉 `Id` `user_id` 和 `movie_id` 三个无用的信息

将空的部分填充 `-1`

用 `One-hot-encoding` 处理 `Gender` `Occupation` `Genre` `Age` `Year`

# 伯努利 Naive Bayes

将数据重新分为 `test` (`X`) 和 `test` (`X_test`)，建立模型并预测，得出每一行取每个 `rating` `(1,2,3,4,5)` 的概率 `predict_prob`

取概率最高的，就是要的 `rating`

# 结果导出

导出为 `csv` 文件
