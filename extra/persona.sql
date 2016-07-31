-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema persona_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema persona_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `persona_db` DEFAULT CHARACTER SET utf8 ;
USE `persona_db` ;

-- -----------------------------------------------------
-- Table `persona_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `username` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `helper` TINYINT(1) NULL DEFAULT NULL,
  `zipcode` VARCHAR(45) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `country_origin` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`connections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`connections` (
  `connection_id` INT(11) NOT NULL AUTO_INCREMENT,
  `helper_id` INT(11) NOT NULL,
  `newcomer_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`connection_id`),
  INDEX `fk_connections_users1_idx` (`helper_id` ASC),
  INDEX `fk_connections_users2_idx` (`newcomer_id` ASC),
  CONSTRAINT `fk_connections_users1`
    FOREIGN KEY (`helper_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_connections_users2`
    FOREIGN KEY (`newcomer_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`helper`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`helper` (
  `user_id` INT(11) NOT NULL,
  `realestate` TINYINT(1) NULL DEFAULT NULL,
  `finances` TINYINT(1) NULL DEFAULT NULL,
  `medicalcare` TINYINT(1) NULL DEFAULT NULL,
  `automobile` TINYINT(1) NULL DEFAULT NULL,
  `lang_tutor` TINYINT(1) NULL DEFAULT NULL,
  `lang_translator` TINYINT(1) NULL DEFAULT NULL,
  `social` TINYINT(1) NULL DEFAULT NULL,
  `previous_newcomer` TINYINT(1) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  INDEX `fk_helper_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_helper_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`invitations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`invitations` (
  `invitation_id` INT(11) NOT NULL,
  `invited_id` INT(11) NOT NULL,
  `inviter_id` INT(11) NOT NULL,
  PRIMARY KEY (`invitation_id`, `invited_id`, `inviter_id`),
  INDEX `fk_invitations_users1_idx` (`invited_id` ASC),
  INDEX `fk_invitations_users2_idx` (`inviter_id` ASC),
  CONSTRAINT `fk_invitations_users1`
    FOREIGN KEY (`invited_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_invitations_users2`
    FOREIGN KEY (`inviter_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`languages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`languages` (
  `language_id` INT(11) NOT NULL,
  `language_name` VARCHAR(45) NULL DEFAULT NULL,
  `iso_639-1` VARCHAR(2) NULL DEFAULT NULL,
  PRIMARY KEY (`language_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`newcomer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`newcomer` (
  `user_id` INT(11) NOT NULL,
  `date_entry` DATETIME NULL DEFAULT NULL,
  `created_at` TEXT NULL DEFAULT NULL,
  `updated_at` TEXT NULL DEFAULT NULL,
  INDEX `fk_refugee_users1` (`user_id` ASC),
  CONSTRAINT `fk_refugee_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `persona_db`.`spoken_languages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `persona_db`.`spoken_languages` (
  `spoken_language_id` INT(11) NOT NULL AUTO_INCREMENT,
  `users_id` INT(11) NOT NULL,
  `language_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`spoken_language_id`),
  INDEX `fk_spoken_languages_users1_idx` (`users_id` ASC),
  INDEX `fk_spoken_languages_languages1_idx` (`language_id` ASC),
  CONSTRAINT `fk_spoken_languages_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `persona_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_spoken_languages_languages1`
    FOREIGN KEY (`language_id`)
    REFERENCES `persona_db`.`languages` (`language_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
