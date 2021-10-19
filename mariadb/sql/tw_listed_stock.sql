CREATE TABLE `tw_listed_stock` (
  `ts_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自動編號',
  `ts_date` date NOT NULL DEFAULT '1900-01-01' COMMENT '日期',
  `ts_stockno` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '股票編號',
  `ts_shares` bigint(20) NOT NULL DEFAULT 0 COMMENT '成交股數',
  `ts_amount` bigint(20) NOT NULL DEFAULT 0 COMMENT '成交金額',
  `ts_open` float NOT NULL DEFAULT 0 COMMENT '開盤價',
  `ts_close` float NOT NULL DEFAULT 0 COMMENT '收盤價',
  `ts_high` float NOT NULL DEFAULT 0 COMMENT '最高價',
  `ts_low` float NOT NULL DEFAULT 0 COMMENT '最低價',
  `ts_diff` float NOT NULL DEFAULT 0 COMMENT '漲跌價差',
  `ts_turnover` int(10) NOT NULL DEFAULT 0 COMMENT '成交筆數',
  PRIMARY KEY (`ts_id`) USING BTREE,
  UNIQUE KEY `ts_stockno` (`ts_stockno`,`ts_date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='上市股票價格列表';