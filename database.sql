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
    IN p_email VARCHAR(20),
    IN p_phone VARCHAR(20),
    IN p_city VARCHAR(20),
    IN p_country VARCHAR(20),
    IN p_disaster VARCHAR(20),
    IN p_need_relief VARCHAR(20),
    IN p_emergency VARCHAR(20),
    IN p_options VARCHAR(20),
    IN p_health VARCHAR(20),
    IN p_safety VARCHAR(20),
    IN p_description VARCHAR(20),
    IN p_donate VARCHAR(20)
)
BEGIN
    if (select exists (select 1 from tbl_user where user_username = p_username) = False) THEN select 'User does not exist!!';
    ELSE
      UPDATE tbl_user SET email=p_email WHERE user_username = p_username;
      UPDATE tbl_user SET phone=p_phone WHERE user_username = p_username;
      UPDATE tbl_user SET city=p_city WHERE user_username = p_username;
      UPDATE tbl_user SET country=p_country WHERE user_username = p_username;
      UPDATE tbl_user SET disaster=p_disaster WHERE user_username = p_username;
      UPDATE tbl_user SET need_relief=p_need_relief WHERE user_username = p_username;
      UPDATE tbl_user SET emergency=p_emergency WHERE user_username = p_username;
      UPDATE tbl_user SET options=p_options WHERE user_username = p_username;
      UPDATE tbl_user SET health=p_health WHERE user_username = p_username;
      UPDATE tbl_user SET safety=p_safety WHERE user_username = p_username;
      UPDATE tbl_user SET description=p_description WHERE user_username = p_username;
      UPDATE tbl_user SET donate=p_donate WHERE user_username = p_username;
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
name, username
ALTER TABLE tbl_user ADD email VARCHAR(20) AFTER user_password;
ALTER TABLE tbl_user ADD phone VARCHAR(20) AFTER email;
ALTER TABLE tbl_user ADD city VARCHAR(20) AFTER phone;
ALTER TABLE tbl_user ADD country VARCHAR(20) AFTER city;
ALTER TABLE tbl_user ADD disaster VARCHAR(20) AFTER country;
ALTER TABLE tbl_user ADD need_relief VARCHAR(20) AFTER disaster;
ALTER TABLE tbl_user ADD emergency VARCHAR(20) AFTER need_relief;
ALTER TABLE tbl_user ADD options VARCHAR(20) AFTER emergency;

ALTER TABLE tbl_user ADD health VARCHAR(20) AFTER options;
ALTER TABLE tbl_user ADD safety VARCHAR(20) AFTER health;
ALTER TABLE tbl_user ADD description VARCHAR(20) AFTER safety;
ALTER TABLE tbl_user ADD donate VARCHAR(20) AFTER description;

ALTER TABLE tbl_user MODIFY emergency VARCHAR(200);

ALTER TABLE tbl_user DROP setting1;
ALTER TABLE tbl_user DROP setting2;
ALTER TABLE tbl_user DROP setting3;
ALTER TABLE tbl_user DROP setting4;
ALTER TABLE tbl_user DROP setting5;
