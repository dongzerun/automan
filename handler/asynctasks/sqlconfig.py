#!/bin/env python
#coding=utf-8
import re


"""己知的主键名称"""
pknames = ['id','category_id','rule_id','feature_id','method_id','scope_id','strategy_id','task_id','house_id','OfferId','BidId','LogId','ComplainId','CommentId','BillId','MessageId','OperationId','log_id','config_id','job_id','depend_id','schedule_id','phone_id','user_id','deposit_id','bang_account_deposit_exten_id','op_id','post_id','advise_id','key_id','product_id','item_id','comment_id','recall_id','xiaoqu_audit_id','activity_id','department_id','AUTOID','cti_id','report_id','index_id','ApplicationBaseId','payment_id','ReportId','bak_id','BakId','account_id','geo_id','provider_id','city_id','result_id','region_id','region_city_id','monitor_id','todo_id','his_todo_id','OpportunityId','message_id','BookingId','ContractId','ContractExecutiveId','AdId','PositionId','PublishId','QuestionId','TemplateId','TypeId','PackageId','area_id','BangId','BangValueAddedServicesId','AgentId','AccountId','agent_cutomer_id','DepositId','service_id','ChannelChargesId','discount_rate_id','sub_id','fang_id','relation_id','fang_sub_id','ext_id','package_id','OrderId','product_line_id','mappting_id','rebate_id','rebate_rate_id','target_Id','clue_id','CompanyId','invoice_id','PaymentID','refund_id','refund_app_id','CustomerId','EventId','ContactId','RelationId','TransactionId','order_id','TaskId','content_id','visit_id','OpportunityProtectId','OpportunityProtectBakId','PermissionId','ResourcesId','sale_target_id','MsgId','company_id','position_id','tag_id']

pkpattern1 = re.compile(r'id|category_id|rule_id|feature_id|method_id|scope_id|strategy_id|task_id|house_id|OfferId|BidId|LogId|ComplainId|CommentId|BillId|MessageId|OperationId|log_id|config_id|job_id|depend_id|schedule_id|phone_id|user_id|deposit_id|bang_account_deposit_exten_id|op_id|post_id|advise_id|key_id|product_id|item_id|comment_id|recall_id|xiaoqu_audit_id|activity_id|department_id|AUTOID|cti_id|report_id|index_id|ApplicationBaseId|payment_id|ReportId|bak_id|BakId|account_id|geo_id|provider_id|city_id|result_id|region_id|region_city_id|monitor_id|todo_id|his_todo_id|OpportunityId|message_id|BookingId|ContractId|ContractExecutiveId|AdId|PositionId|PublishId|QuestionId|TemplateId|TypeId|PackageId|area_id|BangId|BangValueAddedServicesId|AgentId|AccountId|agent_cutomer_id|DepositId|service_id|ChannelChargesId|discount_rate_id|sub_id|fang_id|relation_id|fang_sub_id|ext_id|package_id|OrderId|product_line_id|mappting_id|rebate_id|rebate_rate_id|target_Id|clue_id|CompanyId|invoice_id|PaymentID|refund_id|refund_app_id|CustomerId|EventId|ContactId|RelationId|TransactionId|order_id|TaskId|content_id|visit_id|OpportunityProtectId|OpportunityProtectBakId|PermissionId|ResourcesId|sale_target_id|MsgId|company_id|position_id|tag_id|puid')
"""基于主键得出的python正则表达式"""
pkpattern = re.compile(r'\bid\b|\bcategory_id\b|\brule_id\b|\bfeature_id\b|\bmethod_id\b|\bscope_id\b|\bstrategy_id\b|\btask_id\b|\bhouse_id\b|\bOfferId\b|\bBidId\b|\bLogId\b|\bComplainId\b|\bCommentId\b|\bBillId\b|\bMessageId\b|\bOperationId\b|\blog_id\b|\bconfig_id\b|\bjob_id\b|\bdepend_id\b|\bschedule_id\b|\bphone_id\b|\buser_id\b|\bdeposit_id\b|\bbang_account_deposit_exten_id\b|\bop_id\b|\bpost_id\b|\badvise_id\b|\bkey_id\b|\bproduct_id\b|\bitem_id\b|\bcomment_id\b|\brecall_id\b|\bxiaoqu_audit_id\b|\bactivity_id\b|\bdepartment_id\b|\bAUTOID\b|\bcti_id\b|\breport_id\b|\bindex_id\b|\bApplicationBaseId\b|\bpayment_id\b|\bReportId\b|\bbak_id\b|\bBakId\b|\baccount_id\b|\bgeo_id\b|\bprovider_id\b|\bcity_id\b|\bresult_id\b|\bregion_id\b|\bregion_city_id\b|\bmonitor_id\b|\btodo_id\b|\bhis_todo_id\b|\bOpportunityId\b|\bmessage_id\b|\bBookingId\b|\bContractId\b|\bContractExecutiveId\b|\bAdId\b|\bPositionId\b|\bPublishId\b|\bQuestionId\b|\bTemplateId\b|\bTypeId\b|\bPackageId\b|\barea_id\b|\bBangId\b|\bBangValueAddedServicesId\b|\bAgentId\b|\bAccountId\b|\bagent_cutomer_id\b|\bDepositId\b|\bservice_id\b|\bChannelChargesId\b|\bdiscount_rate_id\b|\bsub_id\b|\bfang_id\b|\brelation_id\b|\bfang_sub_id\b|\bext_id\b|\bpackage_id\b|\bOrderId\b|\bproduct_line_id\b|\bmappting_id\b|\brebate_id\b|\brebate_rate_id\b|\btarget_Id\b|\bclue_id\b|\bCompanyId\b|\binvoice_id\b|\bPaymentID\b|\brefund_id\b|\brefund_app_id\b|\bCustomerId\b|\bEventId\b|\bContactId\b|\bRelationId\b|\bTransactionId\b|\border_id\b|\bTaskId\b|\bcontent_id\b|\bvisit_id\b|\bOpportunityProtectId\b|\bOpportunityProtectBakId\b|\bPermissionId\b|\bResourcesId\b|\bsale_target_id\b|\bMsgId\b|\bcompany_id\b|\bposition_id\b|\btag_id\b|\bpuid\b|\baccountId\b|\bfilter_idx\b|\bdeposit_id\b|\bcase_id\b|\baccountid\b|\bApplicationBaseId\b|\baccount\b|\baccount_id\b|\bagentId\b|\bAgentId\b|\banalysis_date\b|\bapplication_id\b|\bapp_type_name\b|\barea_id\b|\bassignment_id\b|\bautoid\b|\bbak_id\b|\bBidId\b|\bBillId\b|\bbiz_line_name\b|\bcall_id\b|\bcat\b|\bcategory\b|\bcategory_en\b|\bcategory_id\b|\bcategory_name\b|\bchart_id\b|\bchunk\b|\bcity\b|\bcity_id\b|\bcity_key\b|\bcity_name\b|\bclass\b|\bclassify_code\b|\bclick_type\b|\bclient_type\b|\bcode\b|\bcombine_id\b|\bCommentId\b|\bcommodity_code\b|\bcommodity_id\b|\bComplainId\b|\bconfig_id\b|\bconfig_name\b|\bconsume_token\b|\bcti_id\b|\bcti_location_id\b|\bcustomer_id\b|\bdaily_monthly_quarterly_type_name\b|\bday_id\b|\bdb\b|\bdb_id\b|\bdbname\b|\bdepartment_id\b|\bdepend_id\b|\bdistrict_id\b|\bdomain\b|\bdt\b|\bemail\b|\bfactor_name\b|\bfeature_id\b|\bfield_name\b|\bfilename\b|\bgroup_id\b|\bhid\b|\bhost\b|\bhostname\b|\bHouseId\b|\bhouse_source_list_id\b|\bid\b|\bId\b|\bID\b|\bincre_id\b|\bip_id\b|\bjira\b|\bjob_id\b|\bkeywords\b|\bleague_income_ad_type_name\b|\bleague_income_source_type_name\b|\bleague_us_income_name\b|\blink_id\b|\blog_id\b|\bLogId\b|\bmenu_id\b|\bmessage_id\b|\bMessageId\b|\bmethod_id\b|\bmobile\b|\bmonitor_id\b|\bmonth\b|\bname\b|\bOfferId\b|\bOperationId\b|\bowner_id\b|\bpermission_id\b|\bphone\b|\bPositionId\b|\bproduct_code\b|\bprovince_id\b|\bregion_city_id\b|\bregion_id\b|\bregion_name\b|\breport_id\b|\bResourcesId\b|\bresult_id\b|\brule_id\b|\bschedule_id\b|\bscope_id\b|\bstrategy_id\b|\bstreet_id\b|\bsubcategory_id\b|\btable_id\b|\btag_id\b|\btask_id\b|\buid\b|\buni_code\b|\buni_code_commodity\b|\buser_id\b|\buserId\b|\bsource_order_code\b|\bApplicationBaseId\b|\bbid_id\b|\bneeds_puid\b|\bsales_store_id\b|\btactic_id\b|\bsales_account_id\b|\bad_id\b|\bsales_unit_id\b|\bChannelChargesId\b|\bui_id\b|\bfilter_idx\b|\bmajor_idx\b|\bfilter_idx\b|\btemp_idx\b|\bcontractid\b|\bspecial_id\b|\bCreatorId\b|\bcompany_code\b|\bsp_name\b|\bfrc_order_id\b|\bicp_refund_id\b|\bicp_order_id\b|\bsales_snit_id\b')


"""所有主库虚IP host port"""
allclasses = {
'ppc' : [('192.168.64.154.dns.ganji.com', 3306)] ,
'q4medm' : [('yz-qe-ku-02.dns.ganji.com', 3319), ('yz-qe-ku-03.dns.ganji.com', 3319)] ,
'ana' : [('sd-stat-ku-201.dns.ganji.com', 3888)] ,
'zc' : [('yz-zc-ku-m00.dns.ganji.com', 3410)] ,
'edm' : [('yz-edm-ku-00.dns.ganji.com', 3331)] ,
'as' : [('yz-as-ku-m00.dns.ganji.com', 3306)] ,
'im' : [('yz-im-ku-m00.dns.ganji.com', 3306)] ,
'im2' : [('g1-im-ku-00.dns.ganji.com', 3306)] ,
'xs' : [('yz-xs-ku-m00.dns.ganji.com', 3306)] ,
'zp' : [('yz-zp-ku-m00.dns.ganji.com', 3306)] ,
'rp' : [('yz-rp-ku-m00.dns.ganji.com', 3306)] ,
'log' : [('yz-log-ku-m00.dns.ganji.com', 3306)] ,
'fang' : [('yz-fang-ku-m00.dns.ganji.com', 3833)] ,
'myad' : [('sd-myad-ku-m00.dns.ganji.com', 3401)] ,
'pay' : [('yz-pay-ku-m00.dns.ganji.com', 3930)] ,
'jybro' : [('yz-jybro-ku-m00.dns.ganji.com', 3306)] ,
'club' : [('yz-club-ku-00.dns.ganji.com', 3371)] ,
'msapi' : [('yz-msapi-ku-00.dns.ganji.com', 3499)] ,
'bbs' : [('yz-bbs-ku-00.dns.ganji.com', 3370)] ,
'price' : [('yz-ns-ku-pricem.dns.ganji.com', 3892)] ,
'stat' : [('sd-stat-ku-100.dns.ganji.com', 3306)] ,
'crash' : [('g1-qa-ku-00.dns.ganji.com', 3345)] ,
'jy' : [('yz-jy-ku-m00.dns.ganji.com', 3306)] ,
'aspost' : [('yz-asp-ku-m00.dns.ganji.com', 3306)] ,
'hp' : [('yz-hp-ku-m00.dns.ganji.com', 3306)] ,
'boss' : [('yz-boss-ku-m00.dns.ganji.com', 3306)] ,
'rpbg' : [('yz-rpbg-ku-m00.dns.ganji.com', 3306)] ,
'dz' : [('yz-dz-ku-m00.dns.ganji.com', 3306)] ,
'tg' : [('yz-tg-ku-00.dns.ganji.com', 3306)] ,
'mob' : [('yz-mob-ku-m00.dns.ganji.com', 3870)] ,
'sticky' : [('yz-sticky-ku-m00.dns.ganji.com', 3400)] ,
'arch' : [('yz-arch-ku-m00.dns.ganji.com', 3306)] ,
'erp' : [('yz-erp-ku-m00.dns.ganji.com', 3881)] ,
'cpc' : [('yz-biz-ku-00.dns.ganji.com', 3306)] ,
'3ms' : [('yz-ms-ku-m300.dns.ganji.com', 3306)] ,
'tc' : [('yz-tc-ku-m00.dns.ganji.com', 3321)] ,
'mana' : [('yz-mana-ku-m00.dns.ganji.com', 3311)] ,
'jymsg' : [('yz-jymsg-ku-m00.dns.ganji.com', 3802)] ,
'qe' : [('yz-qe-ku-02.dns.ganji.com', 3306), ('yz-qe-ku-03.dns.ganji.com', 3306)] ,
'emp' : [('yz-emp-ku-m00.dns.ganji.com', 3306)] ,
'ms' : [('yz-ms-ku-00.dns.ganji.com', 3306)] ,
'uc00' : [('yz-uc-ku-00.dns.ganji.com', 3306)] ,
'uc01' : [('yz-uc-ku-01.dns.ganji.com', 3306)] ,
'uc02' : [('yz-uc-ku-02.dns.ganji.com', 3306)] ,
'uc03' : [('yz-uc-ku-03.dns.ganji.com', 3306)] ,
'crmrp' : [('g1-crmrp-ku-m00.dns.ganji.com', 3871)] ,
'com' : [('yz-com-ku-00.dns.ganji.com', 3306)]}


"""real qa sim 主机名"""
realhost = "g1-off-ku-real.dns.ganji.com"
qahost = "jxq-off-ku-qa00.dns.ganji.com"
simhost = "yz-off-ku-sim00.dns.ganji.com"
binhost = "yz-off-ku-bin00.dns.ganji.com"


"""线上执行用户名密码,机密"""
dbuser = "dbwebm"
dbpwd = "RW01f1nTbqXJR5MsU8"
dbcfgtable = "dba_stats.class_port"

"""更新速度,每100条后sleep多少秒"""
exespeed = 0.5

"""可以忽略的mysql错误代码
1364  doesn't have a default value
"""
ignorecodes = (1364,)


"""延迟调度视产品线来决定
1.ms,tg,hp,tc,rp晚上0点允许上线
2.其它产品线晚上20点后即可上线
3.只果expect_time晚于当前,以expect_time为准"""
dangerclasses = ('ms','hp','rp','tg','tc')

"""DBA ADMIN"""
_admin  = ("lujiajun", "lirui2", "ligangxing", "luojian", "caifeng", "lvwei", "wanglei", "wangjun", "yangyu","jipengcheng","dongzerun","cuihua","mangweiqi","chenyifan","liujun2","shanzebing","zhaoshenju")

"""urllib2 open url"""
gateway="http://10.1.6.157:8080/delaytask"

"""leader"""

leaders = {
"dongzerun":"dongzerun (董泽润)",
"lujiajun":"lujiajun (卢加俊)",
"lirui2":"lirui2 (李瑞)",
"luojian":"luojian (罗剑)",
"ligangxing":"ligangxing (李罡星)",
"lvwei":"lvwei (吕威)",
"yangyu":"yangyu (杨羽)",
"caifeng":"caifeng (蔡峰)",
"chengjun":"chengjun (成军)",
"shanzebing" : "shanzebing (单泽兵)",
"jipengcheng" : "jipengcheng (纪鹏程)",
"liuyuanjun": "liuyuanjun (刘袁君)",
"wanghailong" : "wanghailong (王海龙)",
"zhangyi3":"zhangyi3 (张翼)",
"cuihua" : "cuihua (崔华)",
"duxiang" : "duxiang (杜翔)",
"libo":"libo (李柏)",
"liyao1":"liyao1 (李瑶)",
"longyin":"longyin (龙寅)",
"luyifeng":"luyifeng (鲁一锋)",
"tianrenjiang":"tianrenjiang (田仁江)",
"wanglei":"wanglei (王磊)",
"wangjun" :"wangjun (王君)",
"wangxufeng" :"wangxufeng (王绪峰)",
"zhangshaofei" :"zhangshaofei (张少飞)",
"haoyongjian" :"haoyongjian (郝永建)",
"tianrenjiang" : "tianrenjiang (田仁江)",
"yanweiping" : "yanweiping (颜维平)",
"zhaoshenju" : "zhaoshenju (赵慎举)",
"zhoufan":"zhoufan (周帆)"
}

dbas = {
"dongzerun",
"lirui2",
"lujiajun",
"zhaoshenju"
}

envtype = {
"sim":2,
"real":0,
"qa":1
}

envbynum = {
2:"sim",
0:"real",
1:"qa"
}

envhost= {
"real":"g1-off-ku-real.dns.ganji.com",
"qa":"jxq-off-ku-qa00.dns.ganji.com",
"sim":"yz-off-ku-sim00.dns.ganji.com",
"bin":"yz-off-ku-bin00.dns.ganji.com",
}

cities = ('lasa','xining','yinchuan','guilin','guiyang','weihai','haikou','huhehaote','lanzhou','wulumuqi','beijing','shanghai','nanchang','kunming','ningbo','taiyuan','wuxi','nanning','changsha','changchun','haerbin','hefei','xiamen','shenzhen','fuzhou','dalian','hangzhou','chongqing','suzhou','shijiazhuang','dongguan','shenyang','qingdao','nanjing','jinan','xian','chengdou','wuhan','tianjin','zhengzhou','guangzhou','others')
