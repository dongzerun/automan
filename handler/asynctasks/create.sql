CREATE TABLE IF NOT EXISTS `xiaoqu`.`xiaoqu_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `street_id` int(11) NOT NULL DEFAULT -1 COMMENT '街道script_index',
  `xiaoqu_id` int(11) NOT NULL DEFAULT -1 COMMENT '小区id',
  `huxing` tinyint(2) NOT NULL DEFAULT -1 COMMENT 'fang1:(1 2 3 4) fang3:(30:合租不限 31:合租单间 32:合租床位)',
  `mean_price` double(11,2) NOT NULL DEFAULT '0.00' COMMENT '均价',
) ENGINE=innodb DEFAULT CHARSET=utf8 COMMENT='xiaoqu均价表';
