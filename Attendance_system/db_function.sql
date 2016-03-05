CREATE OR REPLACE FUNCTION update_userdb(key INT, ps character, issuper boolean,uname character,fname character ,lname character,umail character,isstaff boolean,isactive boolean, datejoined timestamp) RETURNS VOID AS
$$
DECLARE
    temprec RECORD;
    tmpint  INTEGER := 0;
BEGIN

    select id FROM auth_user WHERE id=key INTO temprec;
    GET DIAGNOSTICS tmpint = ROW_COUNT;
    
    IF tmpint = 0 Then 
         INSERT INTO auth_user(id,password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) values(key, ps, issuper,uname,fname,lname,umail,isstaff,isactive,datejoined);
    END IF;

END;
$$
LANGUAGE plpgsql;