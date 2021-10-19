CREATE TABLE `tw_category` (
  `tc_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自動編號',
  `tc_publicdate` date NOT NULL DEFAULT '1900-01-01' COMMENT '上市日期',
  `tc_enddate` date NOT NULL DEFAULT '1900-01-01' COMMENT '下市日期',
  `tc_stockno` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '股票編號',
  `tc_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '股票名稱',
  `tc_isin_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '國際編碼',
  `tc_interest_rate` float NOT NULL DEFAULT 0 COMMENT '殖利率',
  `tc_market` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '市場別',
  `tc_industry` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '產業別',
  `tc_cfi_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `tc_note` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '備註',
  `tc_update_date` date NOT NULL DEFAULT '1900-01-01' COMMENT '股價更新日期',
  `tc_modify_date` date NOT NULL DEFAULT '1900-01-01' COMMENT '類別修改日期',
  PRIMARY KEY (`tc_id`) USING BTREE,
  UNIQUE KEY `tc_stockno` (`tc_stockno`,`tc_publicdate`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票代碼列表';