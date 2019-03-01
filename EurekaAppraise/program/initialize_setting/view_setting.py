#!/usr/bin/env python
# -*- coding: utf-8 -*-

SUMMARY_VIEW = {
    '表3-1': '''
CREATE VIEW [表3-1-TEMP] AS
    SELECT
        "3-1-1" AS [_编号_],
        "现金" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-1-1]
    UNION ALL
    SELECT
        "3-1-2" AS [_编号_],
        "银行存款" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-1-2]
    UNION ALL
    SELECT
        "3-1-3" AS [_编号_],
        "其他货币资金" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-1-3];''',
    '表3-1 ': '''
CREATE VIEW [表3-1] AS
    SELECT
        [_编号_],
        [_科目名称_],
        [_账面价值_],
        [评估价值_],
        [增减值_],
        [增值率_]
    FROM [表3-1-TEMP]
    UNION ALL
    SELECT
    "3-1" AS [_编号_],
    "货币资金合计" AS [_科目名称_],
        sum([_账面价值_]) AS [_账面价值_],
        sum([评估价值_]) AS [评估价值_],
        sum([评估价值_]) - sum([_账面价值_]) AS [增减值_],
        (sum([评估价值_]) - sum([_账面价值_])) / sum([_账面价值_]) AS [增值率_]
    FROM [表3-1-TEMP];''',

    '表3-2': '''
CREATE VIEW [表3-2-TEMP] AS
    SELECT
        "3-2-1" AS [_编号_],
        "交易性金融资产—股票投资" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-2-1]
    UNION ALL
    SELECT
        "3-2-2" AS [_编号_],
        "交易性金融资产—债券投资" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-2-2]
    UNION ALL
    SELECT
        "3-2-3" AS [_编号_],
        "交易性金融资产—基金投资" AS [_科目名称_],
         CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [_账面价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END AS [评估价值_],
        CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_],
        (CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END - 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END) / 
        CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增值率_]
    FROM [表3-2-3];''',
    '表3-2 ': '''
CREATE VIEW [表3-2] AS
    SELECT
        [_编号_],
        [_科目名称_],
        [_账面价值_],
        [评估价值_],
        [增减值_],
        [增值率_]
    FROM [表3-2-TEMP]
    UNION ALL
    SELECT
        "3-2" AS [_编号_],
        "交易性金融资产合计" AS [_科目名称_],
        sum([_账面价值_]) AS [_账面价值_],
        sum([评估价值_]) AS [评估价值_],
        sum([评估价值_]) - sum([_账面价值_]) AS [增减值_],
        (sum([评估价值_]) - sum([_账面价值_])) / sum([_账面价值_]) AS [增值率_]
    FROM [表3-2-TEMP];''',

    '表3-9': '''
CREATE VIEW [表3-9-TEMP] AS
    SELECT
        "3-9-1" AS [_编号_],
        "存货—材料采购（在途物资）" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-1]
    UNION ALL
    SELECT
        "3-9-2" AS [_编号_],
        "存货—原材料" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-2]
    UNION ALL
    SELECT
        "3-9-3" AS [_编号_],
        "存货—在库周转材料" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-3]
    UNION ALL
    SELECT
        "3-9-4" AS [_编号_],
        "存货—委托外加工物资" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-4]
    UNION ALL
    SELECT
        "3-9-5" AS [_编号_],
        "存货—产成品（库存商品、开发产品、农产品）" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-5]
    UNION ALL
    SELECT
        "3-9-6" AS [_编号_],
        "存货—在产品（自制半成品）" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-6]
    UNION ALL
    SELECT
        "3-9-7" AS [_编号_],
        "存货—发出商品" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-7]
    UNION ALL
    SELECT
        "3-9-8" AS [_编号_],
        "存货—在用周转材料" AS [_科目名称_],
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-9-8];''',
    '表3-9 ': '''
CREATE VIEW [表3-9--TEMP] AS
    SELECT
        [_编号_],
        [_科目名称_],
        [_账面价值_],
        [评估价值_],
        [增减值_],
        [增值率_]
    FROM [表3-9-TEMP]
    UNION ALL
    SELECT
        "" AS [_编号_],
        "存货合计" AS [_科目名称_],
        sum([_账面价值_]) AS [_账面价值_],
        sum([评估价值_]) AS [评估价值_],
        sum([评估价值_]) - sum([_账面价值_]) AS [增减值_],
        (sum([评估价值_]) - sum([_账面价值_])) / sum([_账面价值_]) AS [增值率_]
    FROM [表3-9-TEMP]
    UNION ALL
    SELECT
        "" AS [_编号_],
        " 减：存货跌价准备" AS [_科目名称_],
        CASE WHEN [_账面价值_] IS NULL THEN 0 ELSE [_账面价值_] END AS [_账面价值_],
        CASE WHEN [评估价值_] IS NULL THEN 0 ELSE [评估价值_] END AS [评估价值_],
        CASE WHEN [增值额_] IS NULL THEN 0 ELSE [增值额_] END AS [增减值_],
        CASE WHEN [_账面价值_] IS NULL THEN NULL ELSE [增值率_] END AS [增值率_]
    FROM [表8]
        WHERE [_科目名称_] = "二、存货跌价准备";''',
    '表3-9  ': '''
CREATE VIEW [表3-9] AS
    SELECT
        [_编号_],
        [_科目名称_],
        [_账面价值_],
        [评估价值_],
        [增减值_],
        [增值率_]
    FROM [表3-9--TEMP]
    UNION ALL
    SELECT
        "" AS [_编号_],
        "存货净额" AS [_科目名称_],
        A.[_账面价值_] -
        CASE WHEN B.[_账面价值_] IS NULL THEN 0 ELSE B.[_账面价值_] END AS [_账面价值_],
        A.[评估价值_] -
        CASE WHEN B.[评估价值_] IS NULL THEN 0 ELSE B.[评估价值_] END AS [评估价值_],
        (A.[评估价值_] -
        CASE WHEN B.[评估价值_] IS NULL THEN 0 ELSE B.[评估价值_] END) - 
        (A.[_账面价值_] -
        CASE WHEN B.[_账面价值_] IS NULL THEN 0 ELSE B.[_账面价值_] END) AS [增减值_],
        (A.[评估价值_] - 
        CASE WHEN B.[评估价值_] IS NULL THEN 0 ELSE B.[评估价值_] END) - 
        (A.[_账面价值_] -
        CASE WHEN B.[_账面价值_] IS NULL THEN 0 ELSE B.[_账面价值_] END) / 
        (A.[_账面价值_] -
        CASE WHEN B.[_账面价值_] IS NULL THEN 0 ELSE B.[_账面价值_] END) AS [增值率_]
        FROM [表3-9--TEMP] A, [表8] AS B
            WHERE A.[_科目名称_] = "存货合计" AND B.[_科目名称_] = "二、存货跌价准备";''',
    '表3': '''
CREATE VIEW [表3-TEMP] AS
    SELECT
        "3-1" AS [_编号_],
        "货币资金" AS [_科目名称_],
         CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-1]
    UNION ALL
    SELECT
        "3-2" AS [_编号_],
        "交易性金融资产" AS [_科目名称_],
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [_账面价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END AS [评估价值_],
        CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_],
        (CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END - 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END) / 
        CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增值率_]
    FROM [表3-2]
    UNION ALL
    SELECT
        "3-3" AS [_编号_],
        "应收票据净额" AS [_科目名称_],
        CASE WHEN sum(A.[_账面金额_]) IS NULL THEN 0 ELSE sum(A.[_账面金额_]) END - 
        CASE WHEN B.[_账面价值] IS NULL THEN 0 ELSE sum(A.[_账面金额]AS [_账面价值_],
        CASE WHEN sum(A.[评估金额_]) IS NULL THEN 0 ELSE sum(A.[评估金额_]) END AS [评估价值_],
        CASE WHEN sum(A.[评估金额_]) IS NULL THEN 0 ELSE sum(A.[评估金额_]) END -
        CASE WHEN sum(A.[_账面金额_]) IS NULL THEN 0 ELSE sum(A.[_账面金额_]) END AS [增减值_],
        (CASE WHEN sum(A.[评估金额_]) IS NULL THEN 0 ELSE sum(A.[评估金额_]) END - 
        CASE WHEN sum(A.[_账面金额_]) IS NULL THEN 0 ELSE sum(A.[_账面金额_]) END) / 
        CASE WHEN sum(A.[_账面金额_]) IS NULL THEN 0 ELSE sum(A.[_账面金额_]) END AS [增值率_]
    FROM [表3-3] AS A, [表8] AS B
        WHERE A.[_科目名称_]="" AND B.[_科目名称_]="    其中：应收票据"
    '''

}
