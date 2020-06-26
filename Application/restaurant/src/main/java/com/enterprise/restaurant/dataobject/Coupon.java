package com.enterprise.restaurant.dataobject;

import java.math.BigDecimal;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class Coupon {
  @Id
  @GeneratedValue
  private Integer id;

  private BigDecimal amount;
  // amount which will be reduced when using the coupon
  // can have another field using %(percent)

  private String date;
  //expire date

  private String description;

  public Coupon() {
  }

  public Integer getId() {
    return id;
  }

  public void setId(Integer id) {
    this.id = id;
  }

  public BigDecimal getAmount() {
    return amount;
  }

  public void setAmount(BigDecimal amount) {
    this.amount = amount;
  }

  public String getDate() {
    return date;
  }

  public void setDate(String date) {
    this.date = date;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  @Override
  public String toString() {
    return "Coupon{" +
        "id=" + id +
        ", amount=" + amount +
        ", date='" + date + '\'' +
        ", description='" + description + '\'' +
        '}';
  }
}
