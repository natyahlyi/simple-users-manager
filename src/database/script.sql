# DROP DATABASE IF EXISTS Users;
CREATE DATABASE Users DEFAULT CHARACTER SET 'utf8';
--

DROP USER 'users_manager'@'localhost';
--
CREATE USER 'users_manager'@'localhost' IDENTIFIED BY 'users_super_secret_pass';
GRANT ALL PRIVILEGES ON Users.*  TO 'users_manager'@'localhost';

--
USE Users;
--

--
DROP TABLE IF EXISTS users;
--

CREATE TABLE `users` (
  `id` INTEGER UNSIGNED AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `status` ENUM('Active', 'Inactive') DEFAULT 'Inactive',
  `mobile` VARCHAR(20) DEFAULT NULL,
  `phone` VARCHAR(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--

--
DROP TABLE IF EXISTS courses;

--
CREATE TABLE `courses` (
  `id` INTEGER UNSIGNED AUTO_INCREMENT NOT NULL,
  `title` VARCHAR(64) NOT NULL,
  `code` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--

--
DROP TABLE IF EXISTS memberships;

--
CREATE TABLE `memberships` (
  `user_id` INT UNSIGNED NOT NULL,
  `course_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`user_id`, `course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
--


--
DROP PROCEDURE IF EXISTS `get_all_users`;
-- Procedure
CREATE PROCEDURE `get_all_users`()
BEGIN
   SELECT * FROM `users`;
END;
-- End


--
DROP PROCEDURE IF EXISTS `get_user`;
-- Procedure
CREATE PROCEDURE get_user(id INT)
BEGIN
    SELECT * FROM users WHERE users.id = id;
END;
-- End


--
DROP PROCEDURE IF EXISTS `delete_user`;
-- Procedure
CREATE PROCEDURE delete_user(id INT)
BEGIN
    DELETE FROM users WHERE users.id = id;
END;
-- End


--
DROP PROCEDURE IF EXISTS `create_user`;
-- Procedure
CREATE PROCEDURE `create_user`
     (
        IN  p_name       VARCHAR(64)                ,
        IN  p_email      VARCHAR(256)               ,
        IN  p_status     ENUM('Active', 'Inactive') ,
        IN  p_mobile     VARCHAR(20)                ,
        IN  p_phone      VARCHAR(20)
     )
BEGIN

    INSERT INTO `users`
         (
           name   ,
           email  ,
           status ,
           mobile ,
           phone

         )
    VALUES
         (
           p_name   ,
           p_email  ,
           p_status ,
           p_mobile ,
           p_phone
         ) ;
END;
-- End
DROP PROCEDURE IF EXISTS `update_user`;

-- Procedure
CREATE PROCEDURE `update_user`
     (
        IN  p_id       INT(15)                      ,
        IN  p_name     VARCHAR(64)                  ,
        IN  p_email    VARCHAR(256)                 ,
        IN  p_status   ENUM('Active', 'Inactive')   ,
        IN  p_mobile   VARCHAR(20)                  ,
        IN  p_phone    VARCHAR(20)
     )
BEGIN
    UPDATE `users`
    SET    name   = p_name    ,
           email  = p_email   ,
           status = p_status  ,
           mobile = p_mobile  ,
           phone  = p_phone
    WHERE users.id = p_id;
END;
-- End

--
DROP PROCEDURE IF EXISTS `create_course`;
-- Procedure
CREATE PROCEDURE `create_course`
     (
        IN  p_title  VARCHAR(64) ,
        IN  p_code   VARCHAR(32)
     )
BEGIN
    INSERT INTO `courses`
         (
           title    ,
           code
         )
    VALUES
         (
           p_title  ,
           p_code
         ) ;
END;
-- End


--
DROP PROCEDURE IF EXISTS `delete_course`;
-- Procedure
CREATE PROCEDURE delete_course(id INT)
BEGIN
    DELETE FROM courses WHERE courses.id = id;
END;
-- End


--
DROP PROCEDURE IF EXISTS `get_all_courses`;
-- Procedure
CREATE PROCEDURE `get_all_courses`()
BEGIN
   SELECT * FROM `courses`;
END;
-- End


--
DROP PROCEDURE IF EXISTS `create_memberships`;
-- Procedure
CREATE PROCEDURE `create_memberships`
     (
        IN  u_id    INTEGER(10) ,
        IN  c_id    INTEGER(10)
     )
BEGIN
    INSERT INTO memberships
      (
        user_id,
        course_id
      )
    VALUES
      (
        u_id ,
        c_id
      );
END;
-- End


--
DROP PROCEDURE IF EXISTS `delete_memberships`;
-- Procedure
CREATE PROCEDURE delete_memberships(u_id INT)
BEGIN
    DELETE FROM memberships WHERE memberships.user_id = u_id;
END;
-- End


--
DROP PROCEDURE IF EXISTS `get_memberships`;
-- Procedure
CREATE PROCEDURE get_memberships
     (
        IN  u_id    INTEGER
     )
BEGIN
    SELECT courses.id, courses.title, courses.code
    FROM   courses
    JOIN   memberships ON courses.id = memberships.course_id
    WHERE  memberships.user_id = u_id;
END;
-- End


--
DROP PROCEDURE IF EXISTS `get_all_memberships`;
-- Procedure
CREATE PROCEDURE get_all_memberships()
BEGIN
    SELECT * FROM  memberships;
END;
-- End
