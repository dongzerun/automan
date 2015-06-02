ALTER TABLE `gcrm`.`opportunity` ADD INDEX idx_salegroup_merchanttype_merchantid (SaleGroup,merchant_type,merchant_id);
ALTER TABLE `ganji_cr_channel`.`opportunity` ADD INDEX idx_salegroup_merchanttype_merchantid (SaleGroup,merchant_type,merchant_id);
