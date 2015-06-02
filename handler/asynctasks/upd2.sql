ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `clue_source` varchar(100) NOT NULL  DEFAULT '""'  COMMENT '线索来源(所抓取数据的域名)';
ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `is_biz` int(11) NOT NULL DEFAULT '0' COMMENT '0未知，1未付费，2付费';
ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `merchant_type` int(11) NOT NULL DEFAULT '0' COMMENT '房产商户类型，决定merchant_id对应哪张表';
ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `merchant_id`   int(11) NOT NULL DEFAULT '0' COMMENT '房产商户id';
ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `area_id`       int(11) NOT NULL DEFAULT '0' COMMENT '房产门店区域id';
ALTER TABLE `gcrm`.`opportunity` ADD COLUMN `area_name`     varchar(50)   NOT NULL  DEFAULT '""'  COMMENT '房产门店区域名字';
