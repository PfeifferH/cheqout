package com.cheqout.companion;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button bLoyalty = (Button) findViewById(R.id.bLoyalty);
        Button bVerify = (Button) findViewById(R.id.bVerify);

        bLoyalty.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(MainActivity.this, LoyaltyActivity.class);
                MainActivity.this.startActivity(myIntent);
            }
        });

        bVerify.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(MainActivity.this, VerifyActivity.class);
                MainActivity.this.startActivity(myIntent);
            }
        });

    }
}
