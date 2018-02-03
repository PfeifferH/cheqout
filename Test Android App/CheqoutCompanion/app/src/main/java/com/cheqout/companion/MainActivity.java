package com.cheqout.companion;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button bLoyalty = (Button) findViewById(R.id.bLoyalty);
        Button bVerify = (Button) findViewById(R.id.bVerify);
    }
}
