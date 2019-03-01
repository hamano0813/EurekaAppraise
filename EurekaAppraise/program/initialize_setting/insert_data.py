#!/usr/bin/env python
# -*- coding: utf-8 -*-

ASSET_INSERT = {
    '表7': [
        '[_资产名称_]', [
            ('实收资本（或股本）',),
            ('  减：已归还投资',),
            ('实收资本净额（或股本）',),
            ('资本公积',),
            ('  其中：库存股',),
            ('盈余公积',),
            ('  其中：法定公益金',),
            ('未分配利润（未弥补亏损以“-”号表示）',),
            ('所有者权益（净资产）合计',)
        ]
    ],
    '表8': [
        '[_科目名称_],[_账面价值_],[评估价值_],[增值额_],[增值率_]', [
            ('一、应收坏账准备合计', 0, 0, 0, 0),
            ('    其中：应收票据', 0, 0, 0, 0),
            ('          应收帐款', 0, 0, 0, 0),
            ('          预付帐款', 0, 0, 0, 0),
            ('          其他应收款', 0, 0, 0, 0),
            ('二、存货跌价准备', 0, 0, 0, 0),
            ('三、可供出售金融资产减值准备合计', 0, 0, 0, 0),
            ('    其中：可供出售股票', 0, 0, 0, 0),
            ('          可供出售债券', 0, 0, 0, 0),
            ('          可供出售其他资产', 0, 0, 0, 0),
            ('四、持有至到期投资减值准备', 0, 0, 0, 0),
            ('五、长期应收款减值准备', 0, 0, 0, 0),
            ('六、长期股权投资减值准备', 0, 0, 0, 0),
            ('七、投资性房地产减值准备合计', 0, 0, 0, 0),
            ('    其中：房屋', 0, 0, 0, 0),
            ('          土地使用权', 0, 0, 0, 0),
            ('八、固定资产减值准备合计', 0, 0, 0, 0),
            ('    其中：房屋、建筑物', 0, 0, 0, 0),
            ('          构筑物及其他辅助设施', 0, 0, 0, 0),
            ('          管道和沟槽', 0, 0, 0, 0),
            ('          机器设备', 0, 0, 0, 0),
            ('          车辆', 0, 0, 0, 0),
            ('          电子设备', 0, 0, 0, 0),
            ('九、在建工程减值准备合计', 0, 0, 0, 0),
            ('    其中：在建土建工程', 0, 0, 0, 0),
            ('          在建设备安装', 0, 0, 0, 0),
            ('十、工程物质减值准备', 0, 0, 0, 0),
            ('十一、生产性生物资产减值准备', 0, 0, 0, 0),
            ('十二、油气资产减值准备', 0, 0, 0, 0),
            ('十三、无形资产减值准备', 0, 0, 0, 0),
            ('十四、商誉减值准备', 0, 0, 0, 0),
            ('资产减值合计', 0, 0, 0, 0)
        ]
    ],
    '公式': [
        '[表名], [强制], [等式]', [
            ('表3-1-1', False, '_账面价值_=_外币账面金额_*_评估基准日汇率_'),
            ('表3-1-1', False, '评估价值_=_账面价值_'),
            ('表3-1-1', True, '增减值_=评估价值_-_账面价值_'),
            ('表3-1-1', True, '增值率_=增减值_/_账面价值_'),

            ('表3-1-2', False, '_账面价值_=_外币账面金额_*_评估基准日汇率_'),
            ('表3-1-2', False, '评估价值_=_账面价值_'),
            ('表3-1-2', True, '增减值_=评估价值_-_账面价值_'),
            ('表3-1-2', True, '增值率_=增减值_/_账面价值_'),

            ('表3-1-3', False, '_账面价值_=_外币账面金额_*_评估基准日汇率_'),
            ('表3-1-3', False, '评估价值_=_账面价值_'),
            ('表3-1-3', True, '增减值_=评估价值_-_账面价值_'),
            ('表3-1-3', True, '增值率_=增减值_/_账面价值_'),

            ('表3-4', True, '_账龄_=self.aging("_发生日期_")'),
            ('表3-4', True, '增减值_=评估价值_-_账面价值_'),
            ('表3-4', True, '增值率_=增减值_/_账面价值_'),
        ]
    ]
}
