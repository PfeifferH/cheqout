package com.cheqout.companion;

import java.util.List;

/**
 * Created by Angelo on 2/3/2018.
 */

public class Transaction {
    String auth_code, cart;
    int payment_type;
    float subtotal, tax, total;
    List<Item> items;

    public Transaction() {
    }

    public List<Item> getItems() {
        return items;
    }

    public void setItems(List<Item> items) {
        this.items = items;
    }

    public String getAuth_code() {
        return auth_code;
    }

    public void setAuth_code(String auth_code) {
        this.auth_code = auth_code;
    }

    public String getCart() {
        return cart;
    }

    public void setCart(String cart) {
        this.cart = cart;
    }

    public int getPayment_type() {
        return payment_type;
    }

    public void setPayment_type(int payment_type) {
        this.payment_type = payment_type;
    }

    public float getSubtotal() {
        return subtotal;
    }

    public void setSubtotal(float subtotal) {
        this.subtotal = subtotal;
    }

    public float getTax() {
        return tax;
    }

    public void setTax(float tax) {
        this.tax = tax;
    }

    public float getTotal() {
        return total;
    }

    public void setTotal(float total) {
        this.total = total;
    }

    public class Item {
        String id;
        int quantity;
        float weight, unit_price;

        public String getId() {
            return id;
        }

        public Item() {
        }

        public void setId(String id) {
            this.id = id;
        }

        public int getQuantity() {
            return quantity;
        }

        public void setQuantity(int quantity) {
            this.quantity = quantity;
        }

        public float getWeight() {
            return weight;
        }

        public void setWeight(float weight) {
            this.weight = weight;
        }

        public float getUnit_price() {
            return unit_price;
        }

        public void setUnit_price(float unit_price) {
            this.unit_price = unit_price;
        }
    }
}
