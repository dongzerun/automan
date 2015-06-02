ALTER TABLE `bi_marketing`.`marketing_detail` ADD COLUMN `puid` INT(15) DEFAULT -1 NOT NULL COMMENT '相关帖子id' AFTER `user_name`;
