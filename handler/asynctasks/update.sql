update kunming.service_store_post set is_auth_highrisk=1 where is_auth_highrisk>1 and id>0 and is_status = 0;
update kunming.service_store_post set is_auth_highrisk=1 where id>0;
