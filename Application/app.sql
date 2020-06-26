create table `restaurant`(
	`restaurant_id` int not null auto_increment,
	`restaurant_name` varchar(64) not null comment 'restaurant name',
	`owner_id` varchar(32) not null

	primary key (`restaurant_id`)
)

create table `user`(
	`user_id` varchar(32) not null,
	`user_name` varchar(32) not null,
	`user_email` varchar(64),
	`user_address` varchar(128),
	`user_type` tinyint(3) not null default '0',
	`coupon_id` varchar(32) not null

	primary key(`user_id`)
)

create table `coupon`(
	`coupon_id` varchar(32) not null,
	`coupon_name` varchar(64) not null,
	`coupon_discription` varchar(128) not null,
	`coupon_discount_num` int default 0,
	`coupon_discount_percent` int default 0,
	`coupon_require_amount` int default 0

	primary key(`coupon_id`)
)