package com.enterprise.Restaurant.repository;

import com.enterprise.Restaurant.dataobject.Coupon;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CouponRepository extends JpaRepository <Coupon,Integer> {

}
