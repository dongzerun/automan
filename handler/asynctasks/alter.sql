use gcrm;
ALTER TABLE service_clue_record ADD COLUMN is_biz INT(11) NOT NULL DEFAULT 0 COMMENT '0未知，1未付费，2付费';
