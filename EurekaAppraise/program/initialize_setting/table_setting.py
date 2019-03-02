#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来设置默认新建表的设定
列名设置可通过前后下划线来规划属于哪级导出表
前有_       为清查上报表使用列
后有_       为评估明细表使用列
前后都无    为评估工作底稿使用列
数据类型：
Nchar       为unicode字符，括号内为字长，用于文本
Int         为整数，显示时不带小数，用于整数数量
Real        为浮点数，显示时保留2位小数，用于金额
Rate        为浮点数，显示时保留4位小数，用于汇率和数量单价等
Percent     为浮点数，显示时为带百分号的百分数，用于百分比
Date        为日期字符串，显示时保持YYYY-MM-DD形式，主动调用日期控件编辑
Bool        为布尔值，显示时为单选框，用于是否的切换
Switch      为文本，显示时为单选按钮，用于2项以上的单选
"""

BASIC_TABLE = {
    '基础信息': {
        '项目编号': 'Nchar(10)',
        '评估基准日': 'Date',
        '项目文号': 'Nchar(20)',
        '项目全称': 'Nchar(100)',
        '评估对象': 'Nchar(200)',
        '评估范围': 'Nchar(200)',
        '评估方法': 'Nchar(20)',
        '标准收费（万元）': 'Real',
        '实际收费（万元）': 'Real',
        '企业填表人': 'Nchar(10)',
        '项目备案': 'Switch',

    },
    '委托方信息': {
        '名称': 'Nchar(50)',
        '住所': 'Nchar(100)',
        '成立日期': 'Date',
        '经营期限开始': 'Date',
        '经营期限结束': 'Date',
        '注册资金': 'Nchar(20)',
        '实收资本': 'Nchar(20)',
        '经营范围': 'Nchar(500)',
        '联系人': 'Nchar(10)',
        '联系电话': 'Nchar(20)',
    },
    '资产占有方信息': {
        '名称': 'Nchar(50)',
        '住所': 'Nchar(100)',
        '成立日期': 'Date',
        '经营期限开始': 'Date',
        '经营期限结束': 'Date',
        '注册资金': 'Nchar(20)',
        '实收资本': 'Nchar(20)',
        '经营范围': 'Nchar(500)',
        '联系人': 'Nchar(10)',
        '联系电话': 'Nchar(20)',
    },
    '工作计划信息': {
        '项目负责人': 'Nchar(10)',
        '总评师': 'Nchar(10)',
        '资产评估师': 'Nchar(10)',
        '评估工作人员': 'Nchar(20)',
        '聘请专家': 'Nchar(20)',
    }
}

EDIT_TABLE = {
    '表3-1-1': {
        '_存放部门（单位）_': 'Nchar(40)',
        '_币种_': 'Nchar(10)',
        '_外币账面金额_': 'Real',
        '_评估基准日汇率_': 'Rate',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '盘点金额': 'Real',
        '盘点人员': 'Nchar(10)',
        '盘点日期': 'Date',
        '_备注_': 'Nchar(20)'
    },
    '表3-1-2': {
        '_开户银行_': 'Nchar(40)',
        '_账号_': 'Nchar(30)',
        '_币种_': 'Nchar(10)',
        '_外币账面金额_': 'Real',
        '_评估基准日汇率_': 'Rate',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '对账单金额': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-1-3': {
        '_名称或内容_': 'Nchar(40)',
        '_用途_': 'Nchar(20)',
        '_账号_': 'Nchar(30)',
        '_币种_': 'Nchar(10)',
        '_外币账面金额_': 'Real',
        '_评估基准日汇率_': 'Rate',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '对账单金额': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-2-1': {
        '_被投资单位名称_': 'Nchar(40)',
        '_股票名称_': 'Nchar(20)',
        '_投资日期_': 'Date',
        '_持股数量_': 'Int',
        '_成本_': 'Real',
        '_账面价值_': 'Real',
        '基准日收盘价/股_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '股票资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-2-2': {
        '_被投资单位名称_': 'Nchar(40)',
        '_债券名称_': 'Nchar(20)',
        '_发行日期_': 'Date',
        '_投资日期_': 'Date',
        '_票面利率_': 'Rate',
        '_成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '债券资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-2-3': {
        '_基金发行单位_': 'Nchar(40)',
        '_基金名称_': 'Nchar(20)',
        '_基金类型_': 'Nchar(20)',
        '_投资日期_': 'Date',
        '_成本_': 'Real',
        '_账面价值_': 'Real',
        '基准日净值/份_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '基金材料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-3': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_出票日期_': 'Date',
        '_到期日期_': 'Date',
        '_票面利率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '票据': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-4': {
        '_欠款单位名称（结算对象）_': 'Nchar(40)',
        '_业务内容_': 'Nchar(20)',
        '_发生日期_': 'Date',
        '_账龄_': 'Nchar(8)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-5': {
        '_收款单位名称（结算对象）_': 'Nchar(40)',
        '_业务内容_': 'Nchar(20)',
        '_发生日期_': 'Date',
        '_账龄_': 'Nchar(8)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-6': {
        '_欠款单位名称（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_本金_': 'Real',
        '_利息所属期间_': 'Nchar(20)',
        '_利息率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '借款协议': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-7': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_股利（利润）所属期间_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '分红决议': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-8': {
        '_欠款单位（人）名称（结算对象）_': 'Nchar(40)',
        '_业务内容_': 'Nchar(20)',
        '_发生日期_': 'Date',
        '_账龄_': 'Nchar(8)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-1': {
        '_名称及规格型号_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '评估数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '采购发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-2': {
        '_名称及规格型号_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_存放地点_': 'Nchar(20)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '评估基准日后数量变动': 'Rate',
        '评估基准日数量': 'Rate',
        '经盘点': 'Bool',
        '实盘数量': 'Rate',
        '采购发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-3': {
        '_名称及规格型号_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_存放地点_': 'Nchar(20)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '评估基准日后数量变动': 'Rate',
        '评估基准日数量': 'Rate',
        '经盘点': 'Bool',
        '实盘数量': 'Rate',
        '采购发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-4': {
        '_名称及规格型号_': 'Nchar(40)',
        '_加工单位名称_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '委托加工协议': 'Bool',
        '收发货凭证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-5': {
        '_名称_': 'Nchar(40)',
        '_规格型号_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '经盘点': 'Bool',
        '实盘数量': 'Rate',
        '购销发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-6': {
        '_名称及规格型号_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '经盘点': 'Bool',
        '实盘数量': 'Rate',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-7': {
        '_商品名称_': 'Nchar(40)',
        '_对方单位名称_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Rate',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '销售发票或协议': 'Bool',
        '发货凭证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-9-8': {
        '_名称及规格型号_': 'Nchar(40)',
        '_启用日期_': 'Date',
        '_原始入账价值_': 'Real',
        '_账面数量_': 'Rate',
        '_账面金额_': 'Real',
        '实际数量_': 'Rate',
        '评估原价_': 'Real',
        '成新率_': 'Percent',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '采购发票': 'Bool',
        '领用凭证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-10': {
        '_项目及内容_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_结算内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表3-11': {
        '_项目及内容_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_结算内容_': 'Nchar(20)',
        '_成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-1-1': {
        '_被投资单位名称_': 'Nchar(40)',
        '_股票性质_': 'Nchar(20)',
        '_投资日期_': 'Date',
        '_持股数量_': 'Int',
        '_基准日市价_': 'Real',
        '_取得成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '股票资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-1-2': {
        '_被投资单位名称_': 'Nchar(40)',
        '_债券种类_': 'Nchar(20)',
        '_发行日期_': 'Date',
        '_到期日_': 'Date',
        '_票面利率_': 'Percent',
        '_成本（面值）_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '债券资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-1-3': {
        '_被投资单位名称_': 'Nchar(40)',
        '_金融资产名称_': 'Nchar(20)',
        '_投资日期_': 'Date',
        '_持有数量_': 'Int',
        '_基准日市价_': 'Real',
        '_成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '金融资产资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-2': {
        '_被投资单位名称_': 'Nchar(40)',
        '_投资类别_': 'Nchar(20)',
        '_投资日期_': 'Date',
        '_到期日_': 'Date',
        '_票面利率_': 'Percent',
        '_投资成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '投资文件': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-3': {
        '_欠款单位名称（结算对象）_': 'Nchar(40)',
        '_业务内容_': 'Nchar(20)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-4': {
        '_被投资单位名称_': 'Nchar(40)',
        '_投资日期_': 'Date',
        '_投资协议期限_': 'Nchar(20)',
        '_持股比例_': 'Rate',
        '_投资成本_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '投资协议': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-5-1': {
        '_权证编号_': 'Nchar(20)',
        '_房屋名称_': 'Nchar(40)',
        '_来源_': 'Nchar(10)',
        '_结构_': 'Nchar(5)',
        '_建成年月_': 'Date',
        '_计量单位_': 'Nchar(5)',
        '_建筑面积_': 'Real',
        '_成本单价（元/㎡）_': 'Real',
        '_转入日公允价值_': 'Real',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '评估单价（元/㎡）_': 'Real',
        '房屋所有权证': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-5-2': {
        '_土地权证编号_': 'Nchar(20)',
        '_宗地名称_': 'Nchar(40)',
        '_来源_': 'Nchar(10)',
        '_土地位置_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_用地性质_': 'Nchar(10)',
        '_土地用途_': 'Nchar(10)',
        '_准用年限_': 'Int',
        '_开发程度_': 'Nchar(10)',
        '_面积（㎡）_': 'Real',
        '_原始入账价值_': 'Real',
        '_原始入账价值（转入日公允价值）_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '土地使用权证': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-1': {
        '_权证编号_': 'Nchar(20)',
        '_建筑物名称_': 'Nchar(40)',
        '_结构_': 'Nchar(20)',
        '_建成年月_': 'Date',
        '_计量单位_': 'Nchar(5)',
        '_建筑面积（㎡）_': 'Real',
        '_成本单价（元/㎡）_': 'Real',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '评估单价（元/㎡）_': 'Real',
        '房屋所有权证': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-2': {
        '_名称_': 'Nchar(40)',
        '_结构_': 'Nchar(20)',
        '_建成年月_': 'Date',
        '_计量单位_': 'Nchar(5)',
        '_长度（m）_': 'Real',
        '_宽度（m）_': 'Real',
        '_建筑面积（㎡）_': 'Real',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '评估单价（元/㎡）_': 'Real',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-3': {
        '_名称_': 'Nchar(40)',
        '_长度（m）_': 'Real',
        '_槽深（m）_': 'Real',
        '_宽*沟厚 径*壁厚_': 'Real',
        '_材质_': 'Nchar(20)',
        '_绝缘方式_': 'Nchar(20)',
        '_建成年月_': 'Date',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-4': {
        '_设备编号_': 'Nchar(20)',
        '_设备名称_': 'Nchar(40)',
        '_规格型号_': 'Nchar(20)',
        '_生产厂家_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_实际数量_': 'Int',
        '_购置日期_': 'Date',
        '_启用日期_': 'Date',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-5': {
        '_车辆牌号_': 'Nchar(20)',
        '_车辆名称及规格型号_': 'Nchar(20)',
        '_生产厂家_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_实际数量_': 'Int',
        '_购置日期_': 'Date',
        '_启用日期_': 'Date',
        '_已行驶里程（公里）_': 'Rate',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-6': {
        '_设备编号_': 'Nchar(20)',
        '_设备名称_': 'Nchar(40)',
        '_规格型号_': 'Nchar(20)',
        '_生产厂家_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_实际数量_': 'Int',
        '_购置日期_': 'Date',
        '_启用日期_': 'Date',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-6-7': {
        '_土地权证编号_': 'Nchar(20)',
        '_宗地名称_': 'Nchar(40)',
        '_土地位置_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_用地性质_': 'Nchar(10)',
        '_土地用途_': 'Nchar(10)',
        '_准用年限_': 'Int',
        '_开发程度_': 'Nchar(10)',
        '_面积（㎡）_': 'Real',
        '_原始入账价值_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '土地使用权证': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-7-1': {
        '_项目名称_': 'Nchar(40)',
        '_结构_': 'Nchar(10)',
        '_建筑面积/容积_': 'Real',
        '_开工日期_': 'Date',
        '_预计完工日期_': 'Date',
        '_形象进度_': 'Percent',
        '_付款比例_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '工程协议': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-7-2': {
        '_项目名称_': 'Nchar(40)',
        '_规格型号_': 'Nchar(20)',
        '_数量_': 'Int',
        '_计量单位_': 'Nchar(5)',
        '_开工日期_': 'Date',
        '_预计完工日期_': 'Date',
        '_设备费_': 'Real',
        '_资金成本_': 'Real',
        '_安装费及其他_': 'Real',
        '_合计_': 'Real',
        '评估设备费_': 'Real',
        '评估资金成本_': 'Real',
        '评估安装及其他_': 'Real',
        '评估合计_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '工程协议': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-8': {
        '_名称_': 'Nchar(40)',
        '_工程项目_': 'Nchar(40)',
        '_计量单位_': 'Nchar(5)',
        '_账面数量_': 'Real',
        '_账面单价_': 'Real',
        '_账面金额_': 'Real',
        '_实际数量_': 'Real',
        '评估单价_': 'Real',
        '评估金额_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '采购发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-9': {
        '_待处理资产名称_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-10': {
        '_种类_': 'Nchar(20)',
        '_群别_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_数量_': 'Rate',
        '_购置日期_': 'Date',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '入账凭证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-11': {
        '_类别_': 'Nchar(20)',
        '_矿区（或油田）_': 'Nchar(20)',
        '_计量单位_': 'Nchar(5)',
        '_数量_': 'Real',
        '_形成日期_': 'Date',
        '_来源_': 'Nchar(20)',
        '_账面原值_': 'Real',
        '_账面净值_': 'Real',
        '评估原值_': 'Real',
        '成新率_': 'Percent',
        '评估净值_': 'Real',
        '增值率_': 'Percent',
        '采矿许可证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)',
    },
    '表4-12-1': {
        '_土地权证编号_': 'Nchar(20)',
        '_宗地名称_': 'Nchar(40)',
        '_土地位置_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_用地性质_': 'Nchar(10)',
        '_土地用途_': 'Nchar(10)',
        '_准用年限_': 'Int',
        '_开发程度_': 'Nchar(10)',
        '_面积（㎡）_': 'Real',
        '_原始入账价值_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '土地使用权证': 'Bool',
        '评估方法': 'Nchar(10)',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-12-2': {
        '_名称、种类（探矿权/采矿权）_': 'Nchar(20)',
        '_勘察（采矿）许可证编号_': 'Nchar(20)',
        '_取得方式_': 'Nchar(20)',
        '_取得日期_': 'Date',
        '_剩余有效年限_': 'Real',
        '_勘察开发阶段_': 'Nchar(20)',
        '_核定（批准）生产规模_': 'Nchar(20)',
        '_原始入账价值_': 'Real',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '采矿许可证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-12-3': {
        '_无形资产名称和内容_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_法定/预计使用年限_': 'Int',
        '_原始入账价值_': 'Real',
        '_账面价值_': 'Real',
        '_尚可使用年限_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-13': {
        '_内容或名称_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-14': {
        '_内容或名称_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-15': {
        '_费用名称及内容_': 'Nchar(40)',
        '_形成日期_': 'Date',
        '_原始发生额_': 'Real',
        '_预计摊销月数_': 'Int',
        '_尚存受益月数_': 'Int',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '协议及发票': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-16': {
        '_内容或名称_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表4-17': {
        '_内容或者名称_': 'Nchar(40)',
        '_取得日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-1': {
        '_放款银行或机构名称_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_到期日_': 'Date',
        '_月利率_': 'Percent',
        '_币种_': 'Nchar(10)',
        '_外币金额_': 'Real',
        '_账面价值_': 'Real',
        '外币基准日汇率_': 'Rate',
        '评估价值_': 'Real',
        '贷款合同': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-2': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_业务内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '发行资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-3': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_到期日_': 'Date',
        '_票面利率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '票据存根': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-4': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_业务内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-5': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_业务内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-6': {
        '_结算内容_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '工资单': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)',
    },
    '表5-7': {
        '_征税机关_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_税费种类_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '完税凭证': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-8': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_本金_': 'Real',
        '_利息所属期间_': 'Nchar(20)',
        '_利息率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '计息依据': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-9': {
        '_投资单位名称（股东）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_利润所属期间_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '分红决议': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-10': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_业务内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-11': {
        '_结算项目_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_到期日_': 'Date',
        '_票面利率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表5-12': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_结算内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-1': {
        '_放款银行（或机构）名称_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_到期日_': 'Date',
        '_月利率_': 'Percent',
        '_币种_': 'Nchar(10)',
        '_外币金额_': 'Real',
        '_账面价值_': 'Real',
        '外币基准日汇率_': 'Rate',
        '评估价值_': 'Real',
        '贷款合同': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-2': {
        '_债券发行单位_': 'Nchar(40)',
        '_债券种类_': 'Nchar(20)',
        '__发生日期_': 'Date',
        '_到期日_': 'Date',
        '_票面月利率_': 'Percent',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '发行资料': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-3': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_业务内容_': 'Nchar(20)',
        '_账面价值初额_': 'Real',
        '_账面价值利息及汇率净损失_': 'Real',
        '_账面价值合计_': 'Real',
        '评估价值_': 'Real',
        '函证': 'Bool',
        '替代程序': 'Bool',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-4': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_款项内容_': 'Nchar(20)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-5': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_核算内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-6': {
        '_内容_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    },
    '表6-7': {
        '_户名（结算对象）_': 'Nchar(40)',
        '_发生日期_': 'Date',
        '_结算内容_': 'Nchar(20)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '底稿索引号': 'Nchar(10)',
        '_备注_': 'Nchar(20)'
    }
}

SPECIAL_TABLE = {
    '表7': {
        '_资产名称_': 'Nchar(50)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent'
    },
    '表8': {
        '_科目名称_': 'Nchar(50)',
        '_账面价值_': 'Real',
        '评估价值_': 'Real',
        '增减值_': 'Real',
        '增值率_': 'Percent',
        '_备注_': 'Nchar(20)'
    },
    '公式': {
        '表名': 'Nchar(10)',
        '强制': 'Bool',
        '等式': 'Nchar(100)',
    },
    '历史期资产负债表': {
        '科目名称': 'Nchar(50)',
        '三年余额': 'Real',
        '二年余额': 'Real',
        '去年余额': 'Real',
        '本年余额': 'Real',
    },
    '历史期利润表': {
        '科目名称': 'Nchar(50)',
        '三年发生额': 'Real',
        '二年发生额': 'Real',
        '去年发生额': 'Real',
        '本年发生额': 'Real',
    }
}

DRAFT_TABLE = {

}
