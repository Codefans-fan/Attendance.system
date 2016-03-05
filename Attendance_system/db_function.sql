CREATE FUNCTION update_userdb(key INT, ps text, issuper boolean,uname text,fname text ,lname text,umail text,isstaff text,isactive text, datejoined timestamp) RETURNS VOID AS
$$
BEGIN
    LOOP
        -- first try to update the key
        select id from auth_user WHERE id = key;
        IF found THEN
            RETURN;
        END IF;
        -- not there, so try to insert the key
        -- if someone else inserts the same key concurrently,
        -- we could get a unique-key failure
        BEGIN
            INSERT INTO auth_user(id,password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) values(key, ps, issuper,uname,fname,lname,umail,isstaff,isactive,datejoined);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
            -- Do nothing, and loop to try the UPDATE again.
        END;
    END LOOP;
END;
$$
LANGUAGE plpgsql;