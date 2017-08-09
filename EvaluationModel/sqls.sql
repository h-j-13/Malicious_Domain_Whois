数据差异比对时用到的sql语句：

地理位置比对:
select count(*),web_judge_result from domain_index d,locate l,other_info o where d.ID=l.ID and d.ID=o.ID  and cmp=0 group by web_judge_result order by count(*);

域名注册商:
select count(*),sponsoring_registrar from whois w,other_info o where o.ID=w.ID and( web_judge_result=1) group by sponsoring_registrar order by count(*) desc

select count(*),sponsoring_registrar from whois w,other_info o where o.ID=w.ID and( web_judge_result=3 or web_judge_result=2) group by sponsoring_registrar order by count(*) desc  ;
