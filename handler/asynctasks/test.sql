UPDATE gcrm.company SET IsSubmitHouseBrandAd=1,Remarks=IFNULL(Remarks,'')+'系统更新品牌广告标识位' WHERE IsSubmitHouseBrandAd=0 and CompanyId=383746;  
