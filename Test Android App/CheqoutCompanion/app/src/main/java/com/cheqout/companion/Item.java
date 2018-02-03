package com.cheqout.companion;

import java.util.Map;

/**
 * Created by angel on 2/3/2018.
 */

public class Item {
    String id, name;
    int qty;
    float weight, unit_price;

    public String getId() {
        return id;
    }

    public Item(Map<String, Object> map) {
        if(map.get("name")!=null) this.name = map.get("name").toString();
        if(map.get("id")!=null) this.id = map.get("id").toString();
        if(map.get("qty")!=null) this.qty = Integer.parseInt(map.get("qty").toString());
        if(map.get("weight")!=null) this.weight = Float.parseFloat(map.get("weight").toString());
        if(map.get("unit_price")!=null) this.unit_price = Float.parseFloat(map.get("unit_price").toString());
    }


    public Item() {
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getQty() {
        return qty;
    }

    public void setQty(int qty) {
        this.qty = qty;
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