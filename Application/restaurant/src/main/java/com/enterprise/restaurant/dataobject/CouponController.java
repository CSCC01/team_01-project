package com.enterprise.restaurant.dataobject;

import com.enterprise.restaurant.repository.CouponRepository;
import java.math.BigDecimal;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CouponController {
  @Autowired
  private CouponRepository repository;

  // show a list of all coupons in database
  @GetMapping("/coupons")
  public List<Coupon> list_coupon(){
    return repository.findAll();
  }

  // create coupon
  @PostMapping("/coupons")
  public Coupon create_coupon(@RequestParam("amount") BigDecimal amount,
                              @RequestParam("date") String date,
                              @RequestParam("description") String description){
    Coupon coupon = new Coupon();
    coupon.setAmount(amount);
    coupon.setDate(date);
    coupon.setDescription(description);
    return repository.save(coupon);
  }

  // get by id
  @GetMapping("/coupons/{id}")
  public Coupon findCouponById(@PathVariable("id") Integer id){
    return repository.findById(id).orElse(null);
  }

  // once the user part is done
  // this function can show a list of users who have the coupon with certain id

}
