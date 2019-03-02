#!/usr/bin/env python
# -*- coding: utf-8 -*-

SUMMARY_VIEW = {
    '表1': '''
CREATE VIEW [表1-tmp] AS 
SELECT
"流动资产" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="一、流动资产合计"
UNION ALL
SELECT
"非流动资产" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="二、非流动资产合计"
UNION ALL
SELECT
"　　其中：" || [_科目名称_] AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表4] WHERE [表4].[_编号_]="4-1"
UNION ALL
SELECT
"　　　　　" || [_科目名称_] AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表4] WHERE [表4].[_编号_] NOT IN ("4-1","4")
UNION ALL
SELECT
"资产总计" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="三、资产总计"
UNION ALL
SELECT
"流动负债" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="四、流动负债合计"
UNION ALL
SELECT
"非流动负债" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="五、非流动负债合计"
UNION ALL
SELECT
"负债总计" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="六、负债总计"
UNION ALL
SELECT
"净资产（所有者权益）" AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="七、净资产"
UNION ALL
SELECT NULL, NULL, NULL, NULL
UNION ALL
SELECT
[_科目名称_] AS [_项目_],
[_账面价值_],[评估价值_],[增减值_]
FROM [表2] WHERE [表2].[_科目名称_]="平衡：资产总计-负债总计-净资产";''',
    '表1 ': '''
CREATE VIEW [表1] AS
SELECT [_项目_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_]/10000 END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_]/10000 END AS [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_]/10000 END AS [增减值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_]/[_账面价值_] END AS [增值率_]
FROM [表1-tmp];''',

    '表2': '''
CREATE VIEW [表2-asset] AS
SELECT "三、资产总计" AS [_科目名称_],
CASE WHEN [表3].[_账面价值_] IS NULL THEN 0 ELSE [表3].[_账面价值_] END + 
CASE WHEN [表4].[_账面价值_] IS NULL THEN 0 ELSE [表4].[_账面价值_] END AS [_账面价值_],
CASE WHEN [表3].[评估价值_] IS NULL THEN 0 ELSE [表3].[评估价值_] END + 
CASE WHEN [表4].[评估价值_] IS NULL THEN 0 ELSE [表4].[评估价值_] END AS [评估价值_],
CASE WHEN [表3].[增减值_] IS NULL THEN 0 ELSE [表3].[增减值_] END + 
CASE WHEN [表4].[增减值_] IS NULL THEN 0 ELSE [表4].[增减值_] END AS [增减值_]
FROM [表3],[表4] WHERE [表3].[_编号_]="3" AND [表4].[_编号_]="4";''',
    '表2 ': '''
CREATE VIEW [表2-debt] AS
SELECT "六、负债总计" AS [_科目名称_],
CASE WHEN [表5].[_账面价值_] IS NULL THEN 0 ELSE [表5].[_账面价值_] END + 
CASE WHEN [表6].[_账面价值_] IS NULL THEN 0 ELSE [表6].[_账面价值_] END AS [_账面价值_],
CASE WHEN [表5].[评估价值_] IS NULL THEN 0 ELSE [表5].[评估价值_] END + 
CASE WHEN [表6].[评估价值_] IS NULL THEN 0 ELSE [表6].[评估价值_] END AS [评估价值_],
CASE WHEN [表5].[增减值_] IS NULL THEN 0 ELSE [表5].[增减值_] END + 
CASE WHEN [表6].[增减值_] IS NULL THEN 0 ELSE [表6].[增减值_] END AS [增减值_]
FROM [表5],[表6] WHERE [表5].[_编号_]="5" AND [表6].[_编号_]="6";''',

    '表2  ': '''
CREATE VIEW [表2-equity] AS
SELECT "七、净资产" AS [_科目名称_],[_账面价值_],[评估价值_],[增减值_]
FROM [表7] WHERE [表7].[_资产名称_]="所有者权益（净资产）合计";''',

    '表2   ': '''
CREATE VIEW [表2-balance] AS
SELECT "平衡：资产总计-负债总计-净资产" AS "_科目名称_",
[表2-asset].[_账面价值_]-[表2-debt].[_账面价值_]-
CASE WHEN [表2-equity].[_账面价值_] IS NULL THEN 0 ELSE [表2-equity].[_账面价值_] END AS [_账面价值_],
[表2-asset].[评估价值_]-[表2-debt].[评估价值_]-
CASE WHEN [表2-equity].[评估价值_] IS NULL THEN 0 ELSE [表2-equity].[评估价值_] END AS [评估价值_],
[表2-asset].[增减值_]-[表2-debt].[增减值_]-
CASE WHEN [表2-equity].[增减值_] IS NULL THEN 0 ELSE [表2-equity].[增减值_] END AS [增减值_]
FROM [表2-asset],[表2-debt],[表2-equity];''',
    '表2    ': '''
CREATE VIEW [表2] AS
SELECT "一、流动资产合计" AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3] WHERE [表3].[_编号_]="3"
UNION ALL
SELECT "　　"||[_科目名称_] AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3] WHERE [表3].[_编号_]!="3"
UNION ALL
SELECT "二、非流动资产合计" AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4] WHERE [表4].[_编号_]="4"
UNION ALL
SELECT "　　"||[_科目名称_] AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4] WHERE [表4].[_编号_]!="4"
UNION ALL
SELECT [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表2-asset]
UNION ALL
SELECT "四、流动负债合计" AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表5] WHERE [表5].[_编号_]="5"
UNION ALL
SELECT "　　"||[_科目名称_] AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表5] WHERE [表5].[_编号_]!="5"
UNION ALL
SELECT "五、非流动负债合计" AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表6] WHERE [表6].[_编号_]="6"
UNION ALL
SELECT "　　"||[_科目名称_] AS [_科目名称_],
[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表6] WHERE [表6].[_编号_]!="6"
UNION ALL
SELECT [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表2-debt]
UNION ALL
SELECT [_科目名称_],[_账面价值_],[评估价值_],[增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表2-equity]
UNION ALL
SELECT NULL, NULL, NULL, NULL, NULL
UNION ALL
SELECT [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
NULL AS [增减值_],NULL AS [增值率_]
FROM [表2-balance];''',
    '表3': '''
CREATE VIEW [表3-sum] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-1-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-2-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-3-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-4-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-5-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-6-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-7-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-8-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-9-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-10-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-11-tot];''',
    '表3 ': '''
CREATE VIEW [表3-tot] AS
SELECT "3" AS [_编号_], "流动资产合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-sum];''',
    '表3  ': '''
CREATE VIEW [表3] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-tot];''',

    '表3-1': '''
CREATE VIEW [表3-1-sum] AS
SELECT "3-1-1" AS [_编号_], "现金" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-1-1]
UNION ALL
SELECT "3-1-2" AS [_编号_], "银行存款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-1-2]
UNION ALL
SELECT "3-1-3" AS [_编号_], "其他货币资金" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-1-3];''',
    '表3-1 ': '''
CREATE VIEW [表3-1-tot] AS
SELECT "3-1" AS [_编号_], "货币资金合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-1-sum];''',
    '表3-1  ': '''
CREATE VIEW [表3-1] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-1-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-1-tot];''',

    '表3-2': '''
CREATE VIEW [表3-2-sum] AS
SELECT "3-2-1" AS [_编号_], "交易性金融资产—股票投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-2-1]
UNION ALL
SELECT "3-2-2" AS [_编号_], "交易性金融资产—债券投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-2-2]
UNION ALL
SELECT "3-2-3" AS [_编号_], "交易性金融资产—基金投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表3-2-3];''',
    '表3-2 ': '''
CREATE VIEW [表3-2-tot] AS
SELECT "3-2" AS [_编号_], "交易性金融资产合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-2-sum];''',
    '表3-2  ': '''
CREATE VIEW [表3-2] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-2-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-2-tot];''',

    '表3-3': '''
CREATE VIEW [表3-3-tot] AS
SELECT "" AS [_编号_], "应收票据合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-3];''',
    '表3-3 ': '''
CREATE VIEW [表3-3-tmp] AS
SELECT "3-3" AS [_编号_], "应收票据净额" AS [_科目名称_],
[表3-3-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表3-3-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表3-3-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表3-3-tot],[表8]
WHERE [表3-3-tot].[_科目名称_]="应收票据合计" AND [表8].[_科目名称_]="　　其中：应收票据";''',

    '表3-4': '''
CREATE VIEW [表3-4-tot] AS
SELECT "" AS [_编号_], "应收账款合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-4];''',
    '表3-4 ': '''
CREATE VIEW [表3-4-tmp] AS
SELECT "3-4" AS [_编号_], "应收账款净额" AS [_科目名称_],
[表3-4-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表3-4-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表3-4-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表3-4-tot],[表8]
WHERE [表3-4-tot].[_科目名称_]="应收账款合计" AND [表8].[_科目名称_]="　　　　　应收账款";''',

    '表3-5': '''
CREATE VIEW [表3-5-tot] AS
SELECT "" AS [_编号_], "预付账款合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-5];''',
    '表3-5 ': '''
CREATE VIEW [表3-5-tmp] AS
SELECT "3-5" AS [_编号_], "预付账款净额" AS [_科目名称_],
[表3-5-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表3-5-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表3-5-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表3-5-tot],[表8]
WHERE [表3-5-tot].[_科目名称_]="预付账款合计" AND [表8].[_科目名称_]="　　　　　预付账款";''',

    '表3-6': '''
CREATE VIEW [表3-6-tot] AS
SELECT "3-6" AS [_编号_], "应收利息" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-6];''',

    '表3-7': '''
CREATE VIEW [表3-7-tot] AS
SELECT "3-7" AS [_编号_], "应收股利" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-7];''',

    '表3-8': '''
CREATE VIEW [表3-8-tot] AS
SELECT "" AS [_编号_], "其他应收款合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-8];''',
    '表3-8 ': '''
CREATE VIEW [表3-8-tmp] AS
SELECT "3-8" AS [_编号_], "其他应收款净额" AS [_科目名称_],
[表3-8-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表3-8-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表3-8-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表3-8-tot],[表8]
WHERE [表3-8-tot].[_科目名称_]="其他应收款合计" AND [表8].[_科目名称_]="　　　　　预付账款";''',

    '表3-9': '''
CREATE VIEW [表3-9-sum] AS
SELECT "3-9-1" AS [_编号_], "存货—材料采购（在途物资）" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-1]
UNION ALL
SELECT "3-9-2" AS [_编号_], "存货—原材料" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-2]
UNION ALL
SELECT "3-9-3" AS [_编号_], "存货—在库周转材料" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-3]
UNION ALL
SELECT "3-9-4" AS [_编号_], "存货—委托外加工物资" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-4]
UNION ALL
SELECT "3-9-5" AS [_编号_], "存货—产成品（库存商品、开发产品、农产品）" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-5]
UNION ALL
SELECT "3-9-6" AS [_编号_], "存货—在产品（自制半成品）" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-6]
UNION ALL
SELECT "3-9-7" AS [_编号_], "存货—发出商品" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-7]
UNION ALL
SELECT "3-9-8" AS [_编号_], "存货—在用周转材料" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
CASE WHEN sum([评估金额_]) IS NULL THEN 0 ELSE sum([评估金额_]) END -
CASE WHEN sum([_账面金额_]) IS NULL THEN 0 ELSE sum([_账面金额_]) END AS [增减值_]
FROM [表3-9-8];''',
    '表3-9 ': '''
CREATE VIEW [表3-9-tot] AS
SELECT "" AS [_编号_], "存货合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-9-sum];''',
    '表3-9  ': '''
CREATE VIEW [表3-9-tmp] AS
SELECT "3-9" AS [_编号_], "存货净额" AS [_科目名称_],
[表3-9-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表3-9-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表3-9-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表3-9-tot],[表8]
WHERE [表3-9-tot].[_科目名称_]="存货合计" AND [表8].[_科目名称_]="二、存货跌价准备";''',
    '表3-9   ': '''
CREATE VIEW [表3-9] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-9-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-9-tot]
UNION ALL
SELECT "" AS [_编号_], "　　减：存货跌价准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表8]
WHERE [表8].[_科目名称_]="二、存货跌价准备"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表3-9-tmp];''',

    '表3-10': '''
CREATE VIEW [表3-10-tot] AS
SELECT "3-10" AS [_编号_], "一年内到期的非流动资产" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-10];''',

    '表3-11': '''
CREATE VIEW [表3-11-tot] AS
SELECT "3-11" AS [_编号_], "其他流动资产" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表3-11];''',

    '表4': '''
CREATE VIEW [表4-sum] AS
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-1-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-2-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-3-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-4-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-5-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面价值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估价值_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [增减值_],
[净值增值额_]/[_账面净值_] AS [增值率_]
FROM [表4-6-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-7-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-8-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-9-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-10-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-11-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-12-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-13-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-14-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-15-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-16-tot]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-17-tot];''',
    '表4 ': '''
CREATE VIEW [表4-tot] AS
SELECT "4" AS [_编号_], "非流动资产合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-sum];''',
    '表4  ': '''
CREATE VIEW [表4] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-tot];''',

    '表4-1': '''
CREATE VIEW [表4-1-1-tot] AS
SELECT "4-1-1" AS [_编号_], "可供出售金融资产—股票投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-1-1];''',
    '表4-1 ': '''
CREATE VIEW [表4-1-1-tmp] AS
SELECT "" AS [_编号_], "可供出售金融资产—股票投资净额" AS [_科目名称_],
[表4-1-1-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-1-1-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-1-1-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-1-1-tot],[表8]
WHERE [表4-1-1-tot].[_科目名称_]="可供出售金融资产—股票投资" AND [表8].[_科目名称_]="　　其中：可供出售股票";''',
    '表4-1  ': '''
CREATE VIEW [表4-1-2-tot] AS
SELECT "4-1-2" AS [_编号_], "可供出售金融资产—债券投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-1-2];''',
    '表4-1   ': '''
CREATE VIEW [表4-1-2-tmp] AS
SELECT "" AS [_编号_], "可供出售金融资产—债券投资净额" AS [_科目名称_],
[表4-1-2-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-1-2-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-1-2-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-1-2-tot],[表8]
WHERE [表4-1-2-tot].[_科目名称_]="可供出售金融资产—债券投资" AND [表8].[_科目名称_]="　　　　　可供出售债券";''',
    '表4-1    ': '''
CREATE VIEW [表4-1-3-tot] AS
SELECT "4-1-3" AS [_编号_], "可供出售金融资产—其他投资" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-1-3];''',
    '表4-1     ': '''
CREATE VIEW [表4-1-3-tmp] AS
SELECT "" AS [_编号_], "可供出售金融资产—其他投资净额" AS [_科目名称_],
[表4-1-3-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-1-3-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-1-3-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-1-3-tot],[表8]
WHERE [表4-1-3-tot].[_科目名称_]="可供出售金融资产—其他投资" AND [表8].[_科目名称_]="　　　　　可供出售其他资产";''',
    '表4-1      ': '''
CREATE VIEW [表4-1-tot] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-1-tot]
UNION ALL
SELECT "" AS [_编号_], "　　可供出售股票投资减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表8]
WHERE [表8].[_科目名称_]="　　其中：可供出售股票"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-1-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-2-tot]
UNION ALL
SELECT "" AS [_编号_], "　　可供出售债券投资减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表8]
WHERE [表8].[_科目名称_]="　　　　　可供出售债券"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-2-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-3-tot]
UNION ALL
SELECT "" AS [_编号_], "　　可供出售其他投资减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表8]
WHERE [表8].[_科目名称_]="　　　　　可供出售其他资产"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-1-3-tmp];''',
    '表4-1       ': '''
CREATE VIEW [表4-1-tmp] AS
SELECT "4-1" AS [_编号_], "可供出售金融资产净额" AS [_科目名称_],
CASE WHEN [表4-1-1-tmp].[_账面价值_] IS NULL THEN 0 ELSE [表4-1-1-tmp].[_账面价值_] END + 
CASE WHEN [表4-1-2-tmp].[_账面价值_] IS NULL THEN 0 ELSE [表4-1-2-tmp].[_账面价值_] END + 
CASE WHEN [表4-1-3-tmp].[_账面价值_] IS NULL THEN 0 ELSE [表4-1-3-tmp].[_账面价值_] END AS [_账面价值_],
CASE WHEN [表4-1-1-tmp].[评估价值_] IS NULL THEN 0 ELSE [表4-1-1-tmp].[评估价值_] END + 
CASE WHEN [表4-1-2-tmp].[评估价值_] IS NULL THEN 0 ELSE [表4-1-2-tmp].[评估价值_] END + 
CASE WHEN [表4-1-3-tmp].[评估价值_] IS NULL THEN 0 ELSE [表4-1-3-tmp].[评估价值_] END AS [评估价值_],
CASE WHEN [表4-1-1-tmp].[增减值_] IS NULL THEN 0 ELSE [表4-1-1-tmp].[增减值_] END + 
CASE WHEN [表4-1-2-tmp].[增减值_] IS NULL THEN 0 ELSE [表4-1-2-tmp].[增减值_] END + 
CASE WHEN [表4-1-3-tmp].[增减值_] IS NULL THEN 0 ELSE [表4-1-3-tmp].[增减值_] END AS [增减值_]
FROM [表4-1-1-tmp],[表4-1-2-tmp],[表4-1-3-tmp];''',
    '表4-1        ': '''
CREATE VIEW [表4-1] AS
SELECT 
[_编号_], [_科目名称_], [_账面价值_], [评估价值_], [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-1-tot]
UNION ALL
SELECT 
[_编号_], [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END,
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END,
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END,
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-1-tmp];''',

    '表4-2': '''
CREATE VIEW [表4-2-tot] AS
SELECT "" AS [_编号_], "持有至到期投资合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-2];''',
    '表4-2 ': '''
CREATE VIEW [表4-2-tmp] AS
SELECT "4-2" AS [_编号_], "持有至到期投资净额" AS [_科目名称_],
[表4-2-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-2-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-2-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-2-tot],[表8]
WHERE [表4-2-tot].[_科目名称_]="持有至到期投资合计" AND [表8].[_科目名称_]="四、持有至到期投资减值准备";''',

    '表4-3': '''
CREATE VIEW [表4-3-tot] AS
SELECT "" AS [_编号_], "长期应收款合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-3];''',
    '表4-3 ': '''
CREATE VIEW [表4-3-tmp] AS
SELECT "4-3" AS [_编号_], "长期应收款净额" AS [_科目名称_],
[表4-3-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-3-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-3-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-3-tot],[表8]
WHERE [表4-3-tot].[_科目名称_]="长期应收款合计" AND [表8].[_科目名称_]="五、长期应收款减值准备";''',

    '表4-4': '''
CREATE VIEW [表4-4-tot] AS
SELECT "" AS [_编号_], "长期股权投资合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-4];''',
    '表4-4 ': '''
CREATE VIEW [表4-4-tmp] AS
SELECT "4-4" AS [_编号_], "长期股权投资净额" AS [_科目名称_],
[表4-4-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-4-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-4-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-4-tot],[表8]
WHERE [表4-4-tot].[_科目名称_]="长期股权投资合计" AND [表8].[_科目名称_]="六、长期股权投资减值准备";''',

    '表4-5': '''
CREATE VIEW [表4-5-1-tot] AS
SELECT "4-5-1" AS [_编号_], "投资性房地产—房屋" AS [_科目名称_],
sum([_账面净值_]) AS [_账面价值_],
sum([评估净值_]) AS [评估价值_],
CASE WHEN sum([_账面净值_]) IS NULL AND sum([评估净值_]) IS NULL THEN NULL
WHEN sum([_账面净值_]) IS NULL THEN sum([评估净值_])
WHEN sum([评估净值_]) IS NULL THEN -sum([_账面净值_]) 
ELSE sum([评估净值_])-sum([_账面净值_]) END AS [增减值_]
FROM [表4-5-1];''',
    '表4-5 ': '''
CREATE VIEW [表4-5-1-tmp] AS
SELECT "" AS [_编号_], "投资性房地产—房屋净额" AS [_科目名称_],
[表4-5-1-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-5-1-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-5-1-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-5-1-tot],[表8]
WHERE [表4-5-1-tot].[_科目名称_]="投资性房地产—房屋" AND [表8].[_科目名称_]="　　其中：房屋";''',
    '表4-5  ': '''
CREATE VIEW [表4-5-2-tot] AS
SELECT "4-5-2" AS [_编号_], "投资性房地产—土地使用权" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-5-2];''',
    '表4-5   ': '''
CREATE VIEW [表4-5-2-tmp] AS
SELECT "" AS [_编号_], "投资性房地产—土地使用权净额" AS [_科目名称_],
[表4-5-2-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-5-2-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-5-2-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-5-2-tot],[表8]
WHERE [表4-5-2-tot].[_科目名称_]="投资性房地产—土地使用权" AND [表8].[_科目名称_]="　　　　　土地使用权";''',
    '表4-5    ': '''
CREATE VIEW [表4-5-tot] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-5-1-tot]
UNION ALL
SELECT "" AS [_编号_], "　　房屋减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表8]
WHERE [表8].[_科目名称_]="　　其中：房屋"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-5-1-tmp]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-5-2-tot]
UNION ALL
SELECT "" AS [_编号_], "　　土地使用权减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表8]
WHERE [表8].[_科目名称_]="　　　　　土地使用权"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_]
FROM [表4-5-2-tmp];''',
    '表4-5     ': '''
CREATE VIEW [表4-5-tmp] AS
SELECT "4-5" AS [_编号_], "投资性房地产净额" AS [_科目名称_],
CASE WHEN [表4-5-1-tmp].[_账面价值_] IS NULL THEN 0 ELSE [表4-5-1-tmp].[_账面价值_] END + 
CASE WHEN [表4-5-2-tmp].[_账面价值_] IS NULL THEN 0 ELSE [表4-5-2-tmp].[_账面价值_] END AS [_账面价值_],
CASE WHEN [表4-5-1-tmp].[评估价值_] IS NULL THEN 0 ELSE [表4-5-1-tmp].[评估价值_] END + 
CASE WHEN [表4-5-2-tmp].[评估价值_] IS NULL THEN 0 ELSE [表4-5-2-tmp].[评估价值_] END AS [评估价值_],
CASE WHEN [表4-5-1-tmp].[增减值_] IS NULL THEN 0 ELSE [表4-5-1-tmp].[增减值_] END + 
CASE WHEN [表4-5-2-tmp].[增减值_] IS NULL THEN 0 ELSE [表4-5-2-tmp].[增减值_] END AS [增减值_]
FROM [表4-5-1-tmp],[表4-5-2-tmp];''',
    '表4-5      ': '''
CREATE VIEW [表4-5] AS
SELECT 
[_编号_], [_科目名称_], [_账面价值_], [评估价值_], [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-5-tot]
UNION ALL
SELECT 
[_编号_], [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END,
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END,
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END,
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-5-tmp];''',

    '表4-6': '''
CREATE VIEW [表4-6-sum-b] AS
SELECT "4-6-1" AS [_编号_], "固定资产—房屋建筑物" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-1]
UNION ALL
SELECT "4-6-2" AS [_编号_], "固定资产—构筑物及其他辅助设施" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-2]
UNION ALL
SELECT "4-6-3" AS [_编号_], "固定资产—管道和沟槽" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-3];''',
    '表4-6 ': '''
CREATE VIEW [表4-6-tot-b] AS
SELECT "" AS [_编号_], "房屋建筑物类合计" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
sum([原值增值额_]) AS [原值增值额_],
sum([净值增值额_]) AS [净值增值额_]
FROM [表4-6-sum-b];''',

    '表4-6  ': '''
CREATE VIEW [表4-6-sum-e] AS
SELECT "4-6-4" AS [_编号_], "固定资产—机器设备" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-4]
UNION ALL
SELECT "4-6-5" AS [_编号_], "固定资产—车辆" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-5]
UNION ALL
SELECT "4-6-6" AS [_编号_], "固定资产—电子设备" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
CASE WHEN sum([评估原值_]) IS NULL THEN 0 ELSE sum([评估原值_]) END -
CASE WHEN sum([_账面原值_]) IS NULL THEN 0 ELSE sum([_账面原值_]) END AS [原值增值额_],
CASE WHEN sum([评估净值_]) IS NULL THEN 0 ELSE sum([评估净值_]) END -
CASE WHEN sum([_账面净值_]) IS NULL THEN 0 ELSE sum([_账面净值_]) END AS [净值增值额_]
FROM [表4-6-6];''',
    '表4-6   ': '''
CREATE VIEW [表4-6-tot-e] AS
SELECT "" AS [_编号_], "设备类合计" AS [_科目名称_],
sum([_账面原值_]) AS [_账面原值_],
sum([_账面净值_]) AS [_账面净值_],
sum([评估原值_]) AS [评估原值_],
sum([评估净值_]) AS [评估净值_],
sum([原值增值额_]) AS [原值增值额_],
sum([净值增值额_]) AS [净值增值额_]
FROM [表4-6-sum-e];''',

    '表4-6    ': '''
CREATE VIEW [表4-6-tot-l] AS
SELECT "4-6-7" AS [_编号_], "固定资产—土地" AS [_科目名称_],
sum([_账面价值_]) AS [_账面原值_],
sum([_账面价值_]) AS [_账面净值_],
sum([评估价值_]) AS [评估原值_],
sum([评估价值_]) AS [评估净值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [原值增值额_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [净值增值额_]
FROM [表4-6-7];''',

    '表4-6     ': '''
CREATE VIEW [表4-6-tot] AS
SELECT "" AS [_编号_], "固定资产合计" AS [_科目名称_],
CASE WHEN [表4-6-tot-b].[_账面原值_] IS NULL THEN 0 ELSE [表4-6-tot-b].[_账面原值_] END + 
CASE WHEN [表4-6-tot-e].[_账面原值_] IS NULL THEN 0 ELSE [表4-6-tot-e].[_账面原值_] END + 
CASE WHEN [表4-6-tot-l].[_账面原值_] IS NULL THEN 0 ELSE [表4-6-tot-l].[_账面原值_] END AS [_账面原值_],
CASE WHEN [表4-6-tot-b].[_账面净值_] IS NULL THEN 0 ELSE [表4-6-tot-b].[_账面净值_] END + 
CASE WHEN [表4-6-tot-e].[_账面净值_] IS NULL THEN 0 ELSE [表4-6-tot-e].[_账面净值_] END + 
CASE WHEN [表4-6-tot-l].[_账面净值_] IS NULL THEN 0 ELSE [表4-6-tot-l].[_账面净值_] END AS [_账面净值_],
CASE WHEN [表4-6-tot-b].[评估原值_] IS NULL THEN 0 ELSE [表4-6-tot-b].[评估原值_] END + 
CASE WHEN [表4-6-tot-e].[评估原值_] IS NULL THEN 0 ELSE [表4-6-tot-e].[评估原值_] END + 
CASE WHEN [表4-6-tot-l].[评估原值_] IS NULL THEN 0 ELSE [表4-6-tot-l].[评估原值_] END AS [评估原值_],
CASE WHEN [表4-6-tot-b].[评估净值_] IS NULL THEN 0 ELSE [表4-6-tot-b].[评估净值_] END + 
CASE WHEN [表4-6-tot-e].[评估净值_] IS NULL THEN 0 ELSE [表4-6-tot-e].[评估净值_] END + 
CASE WHEN [表4-6-tot-l].[评估净值_] IS NULL THEN 0 ELSE [表4-6-tot-l].[评估净值_] END AS [评估净值_],
CASE WHEN [表4-6-tot-b].[原值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-b].[原值增值额_] END + 
CASE WHEN [表4-6-tot-e].[原值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-e].[原值增值额_] END + 
CASE WHEN [表4-6-tot-l].[原值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-l].[原值增值额_] END AS [原值增值额_],
CASE WHEN [表4-6-tot-b].[净值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-b].[净值增值额_] END + 
CASE WHEN [表4-6-tot-e].[净值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-e].[净值增值额_] END + 
CASE WHEN [表4-6-tot-l].[净值增值额_] IS NULL THEN 0 ELSE [表4-6-tot-l].[净值增值额_] END AS [净值增值额_]
FROM [表4-6-tot-b],[表4-6-tot-e],[表4-6-tot-l];''',
    '表4-6      ': '''
CREATE VIEW [表4-6-tmp] AS
SELECT "4-6" AS [_编号_], "固定资产净额" AS [_科目名称_],
[表4-6-tot].[_账面原值_]-CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面原值_],
[表4-6-tot].[_账面净值_]-CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面净值_],
[表4-6-tot].[评估原值_]-CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [评估原值_],
[表4-6-tot].[评估净值_]-CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [评估净值_],
[表4-6-tot].[原值增值额_]-CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [原值增值额_],
[表4-6-tot].[净值增值额_]-CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [净值增值额_]
FROM [表4-6-tot],[表8]
WHERE [表4-6-tot].[_科目名称_]="固定资产合计" AND [表8].[_科目名称_]="八、固定资产减值准备合计";''',
    '表4-6       ': '''
CREATE VIEW [表4-6] AS
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-tot-b]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-sum-b]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-tot-e]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-sum-e]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-tot-l]
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-tot]
UNION ALL
SELECT "" AS [_编号_], "　　减：固定资产减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面原值_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面净值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估原值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估净值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [原值增值额_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [净值增值额_],
[增减值_]/[_账面价值_] AS [原值增值率_],
[增减值_]/[_账面价值_] AS [净值增值率_]
FROM [表8] WHERE [_科目名称_]="八、固定资产减值准备合计"
UNION ALL
SELECT [_编号_], [_科目名称_],
CASE WHEN [_账面原值_]=0 THEN NULL ELSE [_账面原值_] END AS [_账面原值_],
CASE WHEN [_账面净值_]=0 THEN NULL ELSE [_账面净值_] END AS [_账面净值_],
CASE WHEN [评估原值_]=0 THEN NULL ELSE [评估原值_] END AS [评估原值_],
CASE WHEN [评估净值_]=0 THEN NULL ELSE [评估净值_] END AS [评估净值_],
CASE WHEN [原值增值额_]=0 THEN NULL ELSE [原值增值额_] END AS [原值增值额_],
CASE WHEN [净值增值额_]=0 THEN NULL ELSE [净值增值额_] END AS [净值增值额_],
[原值增值额_]/[_账面原值_] AS [原值增值率_],
[净值增值额_]/[_账面净值_] AS [净值增值率_]
FROM [表4-6-tmp];''',

    '表4-7': '''
CREATE VIEW [表4-7-sum] AS
SELECT "4-7-1" AS [_编号_], "在建工程—土建工程" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表4-7-1]
UNION ALL
SELECT "4-7-2" AS [_编号_], "在建工程—设备安装工程" AS [_科目名称_],
sum([_合计_]) AS [_账面价值_],
sum([评估合计_]) AS [评估价值_],
CASE WHEN sum([评估合计_]) IS NULL THEN 0 ELSE sum([评估合计_]) END -
CASE WHEN sum([_合计_]) IS NULL THEN 0 ELSE sum([_合计_]) END AS [增减值_]
FROM [表4-7-2];''',
    '表4-7 ': '''
CREATE VIEW [表4-7-tot] AS
SELECT "" AS [_编号_], "在建工程合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-7-sum];''',
    '表4-7  ': '''
CREATE VIEW [表4-7-tmp] AS
SELECT "4-7" AS [_编号_], "在建工程净额" AS [_科目名称_],
[表4-7-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-7-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-7-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-7-tot],[表8]
WHERE [表4-7-tot].[_科目名称_]="在建工程合计" AND [表8].[_科目名称_]="九、在建工程减值准备合计";''',
    '表4-7   ': '''
CREATE VIEW [表4-7] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-7-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-7-tot]
UNION ALL
SELECT "" AS [_编号_], "　　减：在建工程减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表8]
WHERE [表8].[_科目名称_]="九、在建工程减值准备合计"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-7-tmp];''',

    '表4-8': '''
CREATE VIEW [表4-8-tot] AS
SELECT "" AS [_编号_], "工程物资合计" AS [_科目名称_],
sum([_账面金额_]) AS [_账面价值_],
sum([评估金额_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-8];''',
    '表4-8 ': '''
CREATE VIEW [表4-8-tmp] AS
SELECT "4-8" AS [_编号_], "工程物资净额" AS [_科目名称_],
[表4-8-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-8-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-8-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-8-tot],[表8]
WHERE [表4-8-tot].[_科目名称_]="工程物资合计" AND [表8].[_科目名称_]="十、工程物质减值准备";''',

    '表4-9': '''
CREATE VIEW [表4-9-tot] AS
SELECT "4-9" AS [_编号_], "固定资产清理" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-9];''',

    '表4-10': '''
CREATE VIEW [表4-10-tot] AS
SELECT "" AS [_编号_], "生产性生物资产合计" AS [_科目名称_],
sum([_账面净值_]) AS [_账面价值_],
sum([评估净值_]) AS [评估价值_],
CASE WHEN sum([_账面净值_]) IS NULL AND sum([评估净值_]) IS NULL THEN NULL
WHEN sum([_账面净值_]) IS NULL THEN sum([评估净值_])
WHEN sum([评估净值_]) IS NULL THEN -sum([_账面净值_])
ELSE sum([评估净值_])-sum([_账面净值_]) END AS [增减值_]
FROM [表4-10];''',
    '表4-10 ': '''
CREATE VIEW [表4-10-tmp] AS
SELECT "4-10" AS [_编号_], "生产性生物资产净额" AS [_科目名称_],
[表4-10-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-10-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-10-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-10-tot],[表8]
WHERE [表4-10-tot].[_科目名称_]="生产性生物资产合计" AND [表8].[_科目名称_]="十一、生产性生物资产减值准备";''',

    '表4-11': '''
CREATE VIEW [表4-11-tot] AS
SELECT "" AS [_编号_], "油气资产合计" AS [_科目名称_],
sum([_账面净值_]) AS [_账面价值_],
sum([评估净值_]) AS [评估价值_],
CASE WHEN sum([_账面净值_]) IS NULL AND sum([评估净值_]) IS NULL THEN NULL
WHEN sum([_账面净值_]) IS NULL THEN sum([评估净值_])
WHEN sum([评估净值_]) IS NULL THEN -sum([_账面净值_])
ELSE sum([评估净值_])-sum([_账面净值_]) END AS [增减值_]
FROM [表4-11];''',
    '表4-11 ': '''
CREATE VIEW [表4-11-tmp] AS
SELECT "4-11" AS [_编号_], "油气资产净额" AS [_科目名称_],
[表4-11-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-11-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-11-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-11-tot],[表8]
WHERE [表4-11-tot].[_科目名称_]="油气资产合计" AND [表8].[_科目名称_]="十二、油气资产减值准备";''',

    '表4-12': '''
CREATE VIEW [表4-12-sum] AS
SELECT "4-12-1" AS [_编号_], "无形资产—土地使用权" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表4-12-1]
UNION ALL
SELECT "4-12-2" AS [_编号_], "无形资产—矿业权" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表4-12-2]
UNION ALL
SELECT "4-12-3" AS [_编号_], "无形资产—其他无形资产" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END -
CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END AS [增减值_]
FROM [表4-12-3];''',
    '表4-12 ': '''
CREATE VIEW [表4-12-tot] AS
SELECT "" AS [_编号_], "无形资产合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-12-sum];''',
    '表4-12  ': '''
CREATE VIEW [表4-12-tmp] AS
SELECT "4-12" AS [_编号_], "无形资产净额" AS [_科目名称_],
[表4-12-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-12-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-12-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-12-tot],[表8]
WHERE [表4-12-tot].[_科目名称_]="无形资产合计" AND [表8].[_科目名称_]="十三、无形资产减值准备";''',
    '表4-12   ': '''
CREATE VIEW [表4-12] AS
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [增减值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-12-sum]
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-12-tot]
UNION ALL
SELECT "" AS [_编号_], "　　减：无形资产减值准备" AS [_科目名称_],
CASE WHEN [_账面价值_]=0 THEN NULL ELSE [_账面价值_] END AS [_账面价值_],
CASE WHEN [评估价值_]=0 THEN NULL ELSE [评估价值_] END AS [评估价值_],
CASE WHEN [_账面价值_]=0 AND [评估价值_]=0 THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表8]
WHERE [表8].[_科目名称_]="十三、无形资产减值准备"
UNION ALL
SELECT [_编号_], [_科目名称_], [_账面价值_], [评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL ELSE [增减值_] END AS [增减值_],
[增减值_]/[_账面价值_] AS [增值率_]
FROM [表4-12-tmp];''',

    '表4-13': '''
CREATE VIEW [表4-13-tot] AS
SELECT "4-13" AS [_编号_], "开发支出" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-13];''',

    '表4-14': '''
CREATE VIEW [表4-14-tot] AS
SELECT "" AS [_编号_], "商誉合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-14];''',
    '表4-14 ': '''
CREATE VIEW [表4-14-tmp] AS
SELECT "4-14" AS [_编号_], "商誉净额" AS [_科目名称_],
[表4-14-tot].[_账面价值_] - CASE WHEN [表8].[_账面价值_] IS NULL THEN 0 ELSE [表8].[_账面价值_] END AS [_账面价值_],
[表4-14-tot].[评估价值_] - CASE WHEN [表8].[评估价值_] IS NULL THEN 0 ELSE [表8].[评估价值_] END AS [评估价值_],
[表4-14-tot].[增减值_] - CASE WHEN [表8].[增减值_] IS NULL THEN 0 ELSE [表8].[增减值_] END AS [增减值_]
FROM [表4-14-tot],[表8]
WHERE [表4-14-tot].[_科目名称_]="商誉合计" AND [表8].[_科目名称_]="十四、商誉减值准备";''',

    '表4-15': '''
CREATE VIEW [表4-15-tot] AS
SELECT "4-15" AS [_编号_], "长期待摊费用" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-15];''',

    '表4-16': '''
CREATE VIEW [表4-16-tot] AS
SELECT "4-16" AS [_编号_], "递延所得税资产" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
CASE WHEN sum([_账面价值_]) IS NULL AND sum([评估价值_]) IS NULL THEN NULL
WHEN sum([_账面价值_]) IS NULL THEN sum([评估价值_])
WHEN sum([评估价值_]) IS NULL THEN -sum([_账面价值_])
ELSE sum([评估价值_])-sum([_账面价值_]) END AS [增减值_]
FROM [表4-16];''',

    '表4-17': '''
CREATE VIEW [表4-17-tot] AS
SELECT "4-17" AS [_编号_], "其他非流动资产" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_],
sum([增减值_]) AS [增减值_]
FROM [表4-17];''',

    '表5': '''
CREATE VIEW [表5-sum] AS
SELECT "5-1" AS [_编号_], "短期借款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-1]
UNION ALL
SELECT "5-2" AS [_编号_], "交易性金融负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-2]
UNION ALL
SELECT "5-3" AS [_编号_], "应付票据" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-3]
UNION ALL
SELECT "5-4" AS [_编号_], "应付账款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-4]
UNION ALL
SELECT "5-5" AS [_编号_], "预收账款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-5]
UNION ALL
SELECT "5-6" AS [_编号_], "应付职工薪酬" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-6]
UNION ALL
SELECT "5-7" AS [_编号_], "应交税费" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-7]
UNION ALL
SELECT "5-8" AS [_编号_], "应付利息" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-8]
UNION ALL
SELECT "5-9" AS [_编号_], "应付股利（应付利润）" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-9]
UNION ALL
SELECT "5-10" AS [_编号_], "其他应付款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-10]
UNION ALL
SELECT "5-11" AS [_编号_], "一年内到期的非流动负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-11]
UNION ALL
SELECT "5-12" AS [_编号_], "其他流动负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-12];''',
    '表5 ': '''
CREATE VIEW [表5-tot] AS
SELECT "5" AS [_编号_], "流动负债合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表5-sum];''',
    '表5  ': '''
CREATE VIEW [表5] AS
SELECT [_编号_],[_科目名称_],
[_账面价值_],
[评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL
WHEN [_账面价值_] IS NULL THEN [评估价值_]
WHEN [评估价值_] IS NULL THEN -[_账面价值_] END AS [增减值_],
CASE WHEN [_账面价值_] IS NULL THEN NULL
WHEN [评估价值_] IS NULL THEN -1
ELSE ([评估价值_]-[_账面价值_])/[_账面价值_] END AS [增值率_]
FROM [表5-sum]
UNION ALL
SELECT [_编号_],[_科目名称_],
[_账面价值_],
[评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL
WHEN [_账面价值_] IS NULL THEN [评估价值_]
WHEN [评估价值_] IS NULL THEN -[_账面价值_] END AS [增减值_],
CASE WHEN [_账面价值_] IS NULL THEN NULL
WHEN [评估价值_] IS NULL THEN -1
ELSE ([评估价值_]-[_账面价值_])/[_账面价值_] END AS [增值率_]
FROM [表5-tot];''',

    '表6': '''
CREATE VIEW [表6-sum] AS
SELECT "6-1" AS [_编号_], "长期借款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-1]
UNION ALL
SELECT "6-2" AS [_编号_], "应付债券" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-2]
UNION ALL
SELECT "6-3" AS [_编号_], "长期应付款" AS [_科目名称_],
sum([_账面价值合计_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-3]
UNION ALL
SELECT "6-4" AS [_编号_], "专项应付款" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-4]
UNION ALL
SELECT "6-5" AS [_编号_], "预计负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-5]
UNION ALL
SELECT "6-6" AS [_编号_], "递延所得税负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-6]
UNION ALL
SELECT "6-7" AS [_编号_], "其他非流动负债" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-7];''',
    '表6 ': '''
CREATE VIEW [表6-tot] AS
SELECT "6" AS [_编号_], "非流动负债合计" AS [_科目名称_],
sum([_账面价值_]) AS [_账面价值_],
sum([评估价值_]) AS [评估价值_]
FROM [表6-sum];''',
    '表6  ': '''
CREATE VIEW [表6] AS
SELECT [_编号_],[_科目名称_],
[_账面价值_],
[评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL
WHEN [_账面价值_] IS NULL THEN [评估价值_]
WHEN [评估价值_] IS NULL THEN -[_账面价值_] END AS [增减值_],
CASE WHEN [_账面价值_] IS NULL THEN NULL
WHEN [评估价值_] IS NULL THEN -1
ELSE ([评估价值_]-[_账面价值_])/[_账面价值_] END AS [增值率_]
FROM [表6-sum]
UNION ALL
SELECT [_编号_],[_科目名称_],
[_账面价值_],
[评估价值_],
CASE WHEN [_账面价值_] IS NULL AND [评估价值_] IS NULL THEN NULL
WHEN [_账面价值_] IS NULL THEN [评估价值_]
WHEN [评估价值_] IS NULL THEN -[_账面价值_] END AS [增减值_],
CASE WHEN [_账面价值_] IS NULL THEN NULL
WHEN [评估价值_] IS NULL THEN -1
ELSE ([评估价值_]-[_账面价值_])/[_账面价值_] END AS [增值率_]
FROM [表6-tot];''',
}
