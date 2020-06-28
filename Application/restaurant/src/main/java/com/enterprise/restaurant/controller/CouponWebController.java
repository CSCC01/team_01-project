package com.enterprise.restaurant.controller;

import com.enterprise.restaurant.dataobject.Coupon;
import com.enterprise.restaurant.repository.CouponRepository;
import java.math.BigDecimal;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping(value = "/coupons/*", method = RequestMethod.GET)
public class CouponWebController {
  @Autowired
  CouponRepository repository;

  @RequestMapping("/create")
  public String create(){
    return "html/createCoupon";
  }

  @PostMapping("/createCoupon")
  public String create(@RequestParam("fname") String name,
      @RequestParam("snum") String amount,
      @RequestParam("email") String date,
      @RequestParam("description") String description){
    Coupon coupon = new Coupon();
    coupon.setName(name);
    coupon.setDate(date);
    coupon.setAmount(new BigDecimal(amount));
    coupon.setDescription(description);
    repository.save(coupon);
    return "html/createCoupon";
  }

  @RequestMapping("/own")
  public String own(){
    return "html/ownersCoupon";
  }

  @GetMapping("/ownersCoupons")
  public List<Coupon> list_coupon(){
    return repository.findAll();
  }


}
