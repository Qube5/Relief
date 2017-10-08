-- THIS FILE DOESN'T DO ANYTHING!

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN select 'Username Exists !!';
    ELSE
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;

-- BREAK

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_editUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20),
    IN p_setting1 VARCHAR(20),
    IN p_setting2 VARCHAR(20),
    IN p_setting3 VARCHAR(20),
    IN p_setting4 VARCHAR(20),
    IN p_setting5 VARCHAR(20)
)
BEGIN
    if (select exists (select 1 from tbl_user where user_username = p_username) = False) THEN select 'User does not exist!!';
    ELSE
      UPDATE tbl_user SET setting1=p_setting1 WHERE user_username = p_username;
      UPDATE tbl_user SET setting2=p_setting2 WHERE user_username = p_username;
      UPDATE tbl_user SET setting3=p_setting3 WHERE user_username = p_username;
      UPDATE tbl_user SET setting4=p_setting4 WHERE user_username = p_username;
      UPDATE tbl_user SET setting5=p_setting5 WHERE user_username = p_username;
    END IF;
END$$
DELIMITER ;

-- BREAK
DROP procedure sp_editUser;
SELECT * FROM tbl_user;
ALTER TABLE tbl_user ADD setting1 CHAR(1) AFTER user_password;
CALL sp_createUser('name','username','password');
CALL sp_editUser('name','username','password',1,2,3,4,5);

UPDATE tbl_user SET setting1='asd' WHERE user_username = 'asdasdads';

ALTER TABLE tbl_user ADD setting1 VARCHAR(20) AFTER user_password;
ALTER TABLE tbl_user ADD setting2 VARCHAR(20) AFTER setting1;
ALTER TABLE tbl_user ADD setting3 VARCHAR(20) AFTER setting2;
ALTER TABLE tbl_user ADD setting4 VARCHAR(20) AFTER setting3;
ALTER TABLE tbl_user ADD setting5 VARCHAR(20) AFTER setting4;

ALTER TABLE tbl_user MODIFY setting5 VARCHAR(20);
