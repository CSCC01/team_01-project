package com.enterprise.restaurant.repository;

import static org.junit.Assert.*;

import com.enterprise.restaurant.dataobject.Coupon;
import java.math.BigDecimal;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class CouponRepositoryTest {
  @Autowired
  private CouponRepository repository;

  @Test
  public void findOneTest(){
    Coupon coupon = repository.findById(1).orElse(null);
    System.out.println(coupon.toString());
  }

  @Test
  public void saveTest(){
    Coupon coupon = new Coupon();
    coupon.setAmount(new BigDecimal(100));
    coupon.setDate("1995-1-1");
    repository.save(coupon);

  }


}