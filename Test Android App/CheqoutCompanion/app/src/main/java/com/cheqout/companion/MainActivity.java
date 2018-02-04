package com.cheqout.companion;

import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.SetOptions;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button bLoyalty = (Button) findViewById(R.id.bLoyalty);
        Button bVerify = (Button) findViewById(R.id.bVerify);
        Button bSimulate = (Button) findViewById(R.id.bSimulate);

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

        bSimulate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FirebaseFirestore db = FirebaseFirestore.getInstance();

                Map<String, Object> item = new HashMap<>();
                item.put("id", "100000004132");
                item.put("quantity", 3.28);
                Map<String, Object> collection = new HashMap<>();
                collection.put("items", item);

                db.collection("carts").document("ULtXMhOuqcRHPpa2aKy1")
                        .set(collection, SetOptions.merge())
                        .addOnSuccessListener(new OnSuccessListener<Void>() {
                            @Override
                            public void onSuccess(Void aVoid) {
                                Toast.makeText(MainActivity.this, "Changes saved", Toast.LENGTH_SHORT).show();
                            }
                        })
                        .addOnFailureListener(new OnFailureListener() {
                            @Override
                            public void onFailure(@NonNull Exception e) {
                                Toast.makeText(MainActivity.this, "Changes could not be saved", Toast.LENGTH_SHORT).show();
                            }
                        });
            }
        });

    }
}
