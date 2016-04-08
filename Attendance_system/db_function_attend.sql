CREATE OR REPLACE FUNCTION update_attendancedb(userid INT, locktime TIMESTAMP WITHOUT TIME ZONE ) RETURNS VOID AS
$$
DECLARE
    temprec RECORD;
    tmpint  INTEGER := 0;
BEGIN

    select id FROM "Attend_attend" WHERE "userId_id"=userid and lock_time=locktime INTO temprec;
    GET DIAGNOSTICS tmpint = ROW_COUNT;
    
    IF tmpint = 0 Then 
         INSERT INTO "Attend_attend"(lock_time,comment,"userId_id") VALUES(locktime,'in',userid);
    END IF;

END;
$$
LANGUAGE plpgsql;
