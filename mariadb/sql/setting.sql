
DROP TABLE IF EXISTS `setting`;

CREATE TABLE `setting` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自動編號',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '參數名稱',
  `value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '參數值',
  `note` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '參數用途說明',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系統相關設定';

LOCK TABLES `setting` WRITE;
/*!40000 ALTER TABLE `setting` DISABLE KEYS */;

INSERT INTO `setting` (`id`, `name`, `value`, `note`)
VALUES
	(1,'DailySchedule','0','更新股票狀態，0:停止，1:啟動中'),
	(2,'OtcUpdateTime','1911-01-01','上櫃股市更新時間');

/*!40000 ALTER TABLE `setting` ENABLE KEYS */;
UNLOCK TABLES;
