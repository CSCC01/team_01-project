CREATE TABLE IF NOT EXISTS `restaurant` (
  `rid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `address`      varchar(256)      NOT NULL DEFAULT '',
  `uid`          int               NOT NULL,
  PRIMARY KEY (`rid`)
);
CREATE TABLE IF NOT EXISTS `user` (
  `uid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `name`         varchar(64)       NOT NULL DEFAULT '',
  `email`        varchar(128)      NOT NULL DEFAULT '',
  `password`     varchar(64)       NOT NULL DEFAULT '',
  `type`         int               NOT NULL,
  PRIMARY KEY (`uid`)
);
CREATE TABLE IF NOT EXISTS `coupons` (
  `cid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `rid`          int               NOT NULL,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `points`       int unsigned      NOT NULL,
  `description`  varchar(1028)     NOT NULL DEFAULT '',
  `begin`        date,
  `expiration`   date,
  PRIMARY KEY (`cid`)
);
CREATE TABLE IF NOT EXISTS `employee` (
  `uid`          int               NOT NULL,
  `rid`          int               NOT NULL,
  PRIMARY KEY (`uid`)
);
CREATE TABLE IF NOT EXISTS `achievement` (
  `aid`          int unsigned      NOT NULL AUTO_INCREMENT,
  `rid`          int               NOT NULL,
  `name`         varchar(128)      NOT NULL DEFAULT '',
  `description`  varchar(1028)     NOT NULL DEFAULT '',
  `experience`   int unsigned      NOT NULL,
  `points`       int unsigned      NOT NULL,
  `requireItem`  int unsigned,
  `requireFee`   int unsigned,

  PRIMARY KEY (`aid`)
);