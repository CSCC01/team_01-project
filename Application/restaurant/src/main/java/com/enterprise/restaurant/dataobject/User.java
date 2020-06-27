package com.enterprise.restaurant.dataobject;

import java.util.Collection;
import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

@Entity
@Table(name = "user", uniqueConstraints = @UniqueConstraint(columnNames = "email"))
public class User {
  @Id
  @GeneratedValue
  private int id;

  private String address;

  private String email;

  private String name;

  private int user_type;

  private int res_id;

  private int experience;

  private String password;

  @OneToMany(targetEntity = Coupon.class, cascade = CascadeType.ALL)
  @JoinColumn(name = "user_coupons", referencedColumnName = "id")
  private Collection<Coupon> coupons;


  public User() {
  }

  public int getId() {
    return id;
  }

  public void setId(int id) {
    this.id = id;
  }

  public String getAddress() {
    return address;
  }

  public void setAddress(String address) {
    this.address = address;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public int getUser_type() {
    return user_type;
  }

  public void setUser_type(int user_type) {
    this.user_type = user_type;
  }

  public int getRes_id() {
    return res_id;
  }

  public void setRes_id(int res_id) {
    this.res_id = res_id;
  }

  public int getExperience() {
    return experience;
  }

  public void setExperience(int experience) {
    this.experience = experience;
  }

  public String getPassword() {
    return password;
  }

  public void setPassword(String password) {
    this.password = password;
  }

  public Collection<Coupon> getCoupons() {
    return coupons;
  }

  public void setCoupons(Collection<Coupon> coupons) {
    this.coupons = coupons;
  }
}
